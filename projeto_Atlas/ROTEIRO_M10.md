# Roteiro — Módulo 10 · Engenharia de Dados

> **Objetivo:** fechar o círculo. A pergunta do Módulo 01 — *"quanto
> vendemos por cidade?"* — passa a ser respondida com o dado de ontem
> à noite, calculado sozinho, conferido, e sem tocar no banco que
> atende o cliente.

Este é o último roteiro do manual.

---

## A situação

A API do Atlas está no ar (M06–M09). E agora:

> *"O relatório de faturamento por cidade demora 40 segundos e, quando
> alguém abre, o site fica lento."*
>
> *"O parceiro manda um CSV todo dia. Alguém baixa e roda um script na
> própria máquina."*
>
> *"O número do painel não bate com o do financeiro. Ninguém sabe
> qual está certo."*

Três frases, três problemas com nome:

| O que acontece | Problema | Etapa |
|----------------|----------|-------|
| Relatório pesado no banco do cliente | OLTP fazendo trabalho de OLAP | 1 |
| Script na máquina de alguém | Sem pipeline, sem rastro | 3 |
| Reprocessar = mexer no código | Data embutida | 5 |
| Dado ruim derruba ou some | Sem quarentena | 4 |
| Números não batem | Sem dicionário de métricas | 7 |
| `cron` por horário | Sem dependência entre etapas | 6 |

---

## Ordem de trabalho

```
1. Separar OLTP de OLAP     ← a decisão que sustenta o resto
2. Extração + bronze        ← marca d'água e manifesto
3. Contratos + quarentena   ← o que é dado válido
4. Portão de qualidade      ← 🔴 ANTES do ouro
5. Transformação → ouro     ← determinística
6. Orquestração             ← DAG, trava, retry
7. Documentação             ← PIPELINE.md e METRICAS.md
8. Prova                    ← 🔑 quebre de propósito
```

> 🔴 **Repare que o portão (4) vem antes do ouro (5).**
>
> É contra-intuitivo — dá vontade de ver o número na tela primeiro e
> "depois adicionar as verificações". Só que "depois" nunca chega: o
> número aparece, alguém vê, vira painel, e o portão fica no backlog
> para sempre.
>
> Construa o portão enquanto ele ainda é barato: antes de existir um
> painel que dependa do ouro.

---

## Etapa 1 — Separar OLTP de OLAP

### O que fazer

Nada de código. Uma decisão e uma linha de configuração.

1. Aponte a extração para uma **réplica de leitura**, através de uma
   variável de ambiente **separada**:

   ```
   ATLAS_BANCO_URL=postgresql://...primario...
   ATLAS_BANCO_REPLICA_URL=postgresql://...replica...
   ```

2. Se `ATLAS_BANCO_REPLICA_URL` não estiver definida, o pipeline
   **falha com mensagem clara**. Não caia no primário em silêncio.

### Por que essa é a primeira etapa

Porque é a única que não dá para retroagir barato. Um pipeline
escrito assumindo que "é tudo o mesmo banco" espalha essa suposição
por vinte arquivos.

### 🔴 Se você não tem réplica

Tudo bem — a maioria dos projetos pequenos não tem. Duas saídas
honestas:

- Rode a extração no **horário morto** e limite o impacto (paginação,
  `statement_timeout`).
- Documente que é o mesmo banco, em `docs/PIPELINE.md`, com a frase
  "quando o volume crescer, isto vira gargalo". Assim, quando virar,
  a resposta já está escrita.

### ✅ Pronto quando

- [ ] `ATLAS_BANCO_REPLICA_URL` existe no `.env.example`
- [ ] A ausência dela produz erro claro, não *fallback* silencioso
- [ ] A decisão está em `docs/PIPELINE.md`

---

## Etapa 2 — Extração e camada bronze

**Arquivo:** `src/atlas/dados/extracao.py`

### O que fazer

1. Marca d'água por fonte (`ler_marca`, `salvar_marca`, `janela`)
2. As três extrações (`extrair_banco`, `extrair_csv`, `extrair_api`)
3. `gravar_bronze` com manifesto e `sha256`

### 🔴 As duas armadilhas

**A marca d'água ingênua perde dado.** Um pedido gravado às 22:59:58
cuja transação faz COMMIT às 23:00:01 tem `atualizado_em` **antes** da
marca nova e nunca mais é visto. Por isso: margem de segurança + marca
= maior valor visto no lote (não `agora()`).

**A marca é commit, e commit vem por último.** Salve a marca **só
depois** de `gravar_bronze` retornar com sucesso. Salvar antes faz o
dado sumir para sempre numa falha de disco.

### ⚠️ O CSV brasileiro

`sep=";"`, `decimal=","`, `thousands="."`, `dayfirst=True`, e o
encoding descoberto por tentativa — com `latin-1` **por último**,
porque ele nunca levanta erro e transforma "Ação" em "AÃ§Ã£o" em
silêncio.

Depois de ler: **confira os dtypes**. Coluna que devia ser `float` e
veio `object` é o erro que produz número errado sem erro nenhum.

### ✅ Pronto quando

- [ ] Rodar duas vezes seguidas não reextrai o que já veio
- [ ] Matar o processo no meio não corrompe a marca (escrita atômica)
- [ ] Todo parquet do bronze tem `_manifesto.json` ao lado
- [ ] O manifesto **não** contém chave de API na URL

---

## Etapa 3 — Contratos e quarentena

**Arquivo:** `src/atlas/dados/contratos.py`

### O que fazer

1. `PedidoBruto` em Pydantic, com `Enum` para status e canal
2. `validar_lote` → `(aprovadas, rejeitadas)`
3. `gravar_quarentena` e `resumir_quarentena`

### 🔴 A decisão que define este arquivo

Uma linha inválida **não derruba o lote** e **não é descartada**. Vai
para a quarentena, com o motivo, e o lote segue.

Derrubar o lote: 1 linha ruim em 2 milhões e você fica sem relatório.
Descartar a linha: o número sai errado e ninguém sabe.

A quarentena preserva as duas coisas — o relatório sai hoje, e o dado
ruim continua existindo.

### ⚠️ LGPD

A quarentena guarda a linha original inteira, e a linha original tem
nome, e-mail, às vezes CPF. Mascare antes de gravar, ou grave só as
colunas necessárias ao diagnóstico. E confira que o `.gitignore`
ignora `dados/lago/quarentena/` — **já está lá**, não remova.

### ✅ Pronto quando

- [ ] Uma linha ruim vai para a quarentena e o lote termina
- [ ] O arquivo de quarentena diz **qual campo** e **qual valor**
- [ ] `sku` com espaço e minúscula é normalizado (`mode="before"`!)
- [ ] `datetime` sem fuso é **rejeitado**

---

## Etapa 4 — 🔴 O portão de qualidade

**Arquivo:** `src/atlas/dados/qualidade.py`

### O que fazer

As seis verificações, e `publicar_se_aprovado`.

### A sexta é a que importa

As cinco primeiras olham para **dentro** do lote — pegam dado
malformado. A sexta compara com o **histórico**, e é a única que pega
um lote perfeitamente válido e completamente errado:

> A origem mudou um `WHERE`. Vieram 30 mil pedidos em vez de 2
> milhões. Todos válidos. As cinco primeiras aprovam. O relatório sai
> com 1,5% do faturamento e ninguém percebe até o fechamento do mês.

### 🔴 Erro ≠ aviso

Se tudo for erro, o pipeline vive quebrado por motivo besta e a equipe
aprende a rodar com `--forcar`. Aí o portão deixou de existir — e você
nem vai saber o dia em que isso aconteceu.

### 🔑 E o portão precisa ser inescapável

Se `construir_ouro` puder ser chamado direto, de qualquer lugar, o
portão é decorativo. Uma verificação que dá para contornar não é uma
verificação — é uma sugestão.

### ✅ Pronto quando

- [ ] Existe um teste **por verificação** provando que ela reprova
- [ ] Existe um teste com lote bom provando que tudo passa
- [ ] Reprovar **não apaga** o ouro anterior
- [ ] `--forcar` pula a trava, **nunca** o portão

---

## Etapa 5 — Transformação e ouro

**Arquivo:** `src/atlas/dados/transformacao.py`

### 🔴 A regra de ouro do ouro

Rodar duas vezes para o mesmo dia produz **exatamente** o mesmo ouro.
Mesmo SHA-256.

Isso proíbe, aqui dentro: `datetime.now()`, `random`, `uuid4`, INSERT
sem chave, e ordem de linhas não definida.

Para conseguir: ordene linhas e colunas antes de gravar,
`reset_index(drop=True)`, e ponha `gerado_em` num `_manifesto.json` ao
lado — **nunca dentro** do parquet, porque muda o hash a cada rodada.

### ⚠️ As três armadilhas silenciosas do pandas

| Armadilha | O que acontece |
|-----------|----------------|
| `groupby` sem `dropna=False` | linhas com chave nula somem, total fica menor, nada avisa |
| dedup antes do portão | esconde origem quebrada — **conte** o que removeu |
| `drop_duplicates` sem ordenar | mantém a primeira, e você fatura pedido cancelado |

### ✅ Pronto quando

- [ ] Duas rodadas do mesmo dia → hashes idênticos
- [ ] Publicação atômica (escreve em temp, `os.replace`)
- [ ] `groupby` trata o grupo nulo explicitamente
- [ ] Dedup devolve **quantas** duplicatas removeu

---

## Etapa 6 — Orquestração

**Arquivo:** `src/atlas/dados/orquestracao.py`
**Entrada:** `scripts/rodar_pipeline.py`

### Por que não `cron`

O `cron` sabe que horas são. Ele não sabe se a etapa anterior
terminou. Na noite em que a extração demorar 40 minutos, a
transformação roda às 03:30 com o dado de ontem, publica, e o
relatório está errado — sem erro, sem alerta.

### O que fazer

1. `ordenar` (topológica, com detecção de ciclo **e** de dependência
   inexistente)
2. `executar_dag` com retry exponencial e estado `PULADA`
3. Trava com TTL (`SET ... NX EX`) e liberação que confere o dono
4. `rodar_pipeline.py` com data como parâmetro e **códigos de saída**

### 🔑 Retry só é seguro se a tarefa for idempotente

Antes de pôr `tentativas=3` numa tarefa, prove que rodá-la duas vezes
não duplica nada.

### ⚠️ Códigos de saída

Cron, systemd e Airflow não leem sua saída bonita. Leem **um número**.
Um script que imprime "❌ ERRO" e devolve `0` é um pipeline que falha
em silêncio para sempre.

### ✅ Pronto quando

- [ ] Falha em `extrair_banco` deixa `construir_prata` como `PULADA`
- [ ] Duas execuções simultâneas: a segunda sai com código 2
- [ ] `kill -9` no meio não deixa a trava presa (TTL)
- [ ] `rodar_pipeline.py 2026-03-12` reprocessa março sem tocar código

---

## Etapa 7 — Documentação

**Arquivos:** `docs/PIPELINE.md`, `docs/METRICAS.md`

Os dois já existem, como **gabaritos**, com seções `_(preencha)_`.

> ⚠️ Um documento com o gabarito intacto é **pior que nenhum**: dá a
> impressão de que existe documentação.

### `PIPELINE.md` — para quem for acordado às 3h

O que mais importa: a tabela "pode apagar?" (numa emergência de disco
cheio, ela é o que impede alguém de apagar o bronze) e a seção
"quando quebra".

### `METRICAS.md` — para a reunião de fechamento

O campo **NÃO inclui** é o que encerra a discussão. "Faturamento é a
soma das vendas" não diz se frete entra. "NÃO inclui frete, impostos
nem descontos posteriores" diz.

### ✅ Pronto quando

- [ ] Nenhum `_(preencha)_` sobrou
- [ ] Cada métrica do painel tem entrada em `METRICAS.md`
- [ ] Cada entrada tem **NÃO inclui** e **fuso horário**
- [ ] As decisões da seção 3 do `PIPELINE.md` estão respondidas

---

## Etapa 8 — 🔑 Prove que funciona

A etapa que quase todo mundo pula, e a única que prova as outras sete.

### 8.1 Quebre o dado de propósito

| Estrague | Deve pegar |
|----------|-----------|
| duplique 10 linhas na prata | unicidade |
| zere um preço | faixa |
| corte o lote para 5% | volume 🔑 |
| ponha custo > preço | coerência |
| apague coluna obrigatória | obrigatórias |
| entregue lote vazio | completude |

Se alguma **não** pegar, você tem uma verificação decorativa.

### 8.2 Quebre o pipeline de propósito

- Mate o processo no meio → a marca d'água ficou consistente?
- Rode duas instâncias → a segunda saiu com código 2?
- Derrube a API do parceiro → o pipeline terminou mesmo assim?
- Rode o mesmo dia 2× → os hashes do ouro bateram?

### 8.3 Rode as baterias

Abra `Modulo_10_Engenharia_de_Dados/10_99_Lista_Exercicios.ipynb`,
aponte `PROJETO` para este diretório e execute as quatro baterias.

> ⚠️ As baterias 1, 2 e 4 leem **arquivos**. Só a bateria 3 **executa**
> o pipeline. Um verificador que lê texto pode ser enganado por um
> nome de variável — comportamento só se prova executando. Essa
> limitação está impressa na saída da própria bateria 2, de propósito.

### ✅ Pronto quando

- [ ] As seis quebras foram testadas e as seis foram pegas
- [ ] As quatro baterias passam
- [ ] Você viu o portão reprovar **com os próprios olhos**

---

## O que você tem no fim

```
projeto_Atlas/
├── src/atlas/
│   ├── api/          ← M06–M07 · responde em milissegundos
│   └── dados/        ← M10 · roda uma vez por noite
├── dados/lago/       ← bronze · prata · ouro · quarentena · estado
├── scripts/rodar_pipeline.py
├── docs/PIPELINE.md  ← para as 3h da manhã
└── docs/METRICAS.md  ← para a reunião de fechamento
```

Os dois lados do mesmo sistema, que não se atrapalham.

---

## O fecho

No Módulo 01 você respondeu *"quanto vendemos por cidade?"* com um
laço de `for` sobre um CSV, rodando na sua máquina, quando você
lembrava de rodar.

Agora a mesma pergunta é respondida por um pipeline que roda sozinho
de madrugada, lê de três origens, guarda o dado como chegou, separa o
que não presta sem jogar fora, confere seis coisas antes de publicar,
não publica se não confiar, produz o mesmo resultado se rodar de novo,
avisa quando quebra, e explica o que cada número significa.

A pergunta é a mesma. O que mudou é o que acontece quando algo dá
errado — que é, no fim, a única coisa que separa um script de um
sistema.

---

*Atlas · Aurora Comércio · Módulo 10 — fim do manual*
