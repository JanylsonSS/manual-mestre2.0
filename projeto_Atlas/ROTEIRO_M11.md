# Roteiro — Módulo 11 · Arquitetura e Decisões

> **Objetivo:** tornar explícito o que hoje só existe na sua cabeça —
> e transformar a arquitetura de intenção em regra verificada.

Este módulo **não tem notebooks**. Ele é só projeto: o currículo de
notebooks encerrou no M10, e daqui em diante o trabalho é sobre o
Atlas que você construiu.

---

## A situação

> *"Entrou gente nova no time. A primeira pergunta foi 'por que tem
> dois bancos?'. Eu levei vinte minutos explicando. Semana que vem
> entra mais alguém."*
>
> *"E ontem eu abri uma rota e tinha um SELECT dentro. Ninguém sabe
> quem escreveu nem quando."*

Duas frases, dois problemas que parecem diferentes e são o mesmo:

| O que acontece | Problema | Etapa |
|----------------|----------|-------|
| Explicar a mesma decisão toda vez | O **porquê** não está escrito | 2 |
| Alguém propõe desfazer uma decisão boa | O contexto se perdeu | 2 |
| SQL dentro de uma rota | A camada não é **verificada** | 3 |
| "Onde eu coloco esta função?" | O mapa não existe | 1 |

> 💭 Os dois se resumem a: **o sistema sabe coisas que os documentos
> não sabem.** Enquanto isso for verdade, todo conhecimento depende de
> você estar disponível — e isso não escala nem para duas pessoas.

---

## Ordem de trabalho

```
1. Desenhar as camadas     ← o mapa do que existe hoje
2. Escrever os ADRs        ← o porquê, antes que evapore
3. Verificar as camadas    ← 🔑 a regra que se prova sozinha
4. Ligar ao CI             ← a regra que ninguém pode ignorar
5. Consertar o que achar   ← ou declarar a exceção, com motivo
```

> 🔴 **Repare que "consertar" vem por último.** É contra-intuitivo —
> dá vontade de sair movendo função assim que o verificador acusar.
>
> Não faça. Primeiro descubra **tudo** que está errado, depois decida
> o que é violação de verdade e o que é regra mal desenhada. Metade
> das "violações" do primeiro relatório costuma ser o seu mapa que
> está errado, não o código.

---

## Etapa 1 — Desenhar as camadas

**Arquivo:** `docs/ARQUITETURA.md` (já existe, como gabarito)

### O que fazer

Abra o documento e confira se o desenho bate com o seu projeto. Ele
foi montado a partir dos módulos 01–10 — se você fez escolhas
diferentes, o desenho é seu, não meu.

Depois responda a pergunta difícil: **em que camada ficam
`apresentacao`, `relatorios`, `migracao` e `integracoes`?**

### 🔑 `integracoes/` é o caso interessante

Ele é **ENTRADA** (o mundo lá fora, como a API) ou **ACESSO** (é só
outra fonte de dado, como o repositório)?

Os dois argumentos são bons:

| "É entrada" | "É acesso" |
|---|---|
| Fala com sistemas que você não controla | Do ponto de vista do serviço, é só "de onde vem o frete" |
| Falha de formas que o banco não falha | Trocar transportadora não deveria mexer no serviço |

Não existe resposta certa. Existe **decisão registrada**. Escolha,
escreva um ADR, e deixe o verificador te manter honesto.

### ✅ Pronto quando

- [ ] Todo módulo de `src/atlas/` está classificado
- [ ] Nenhum `_(preencha)_` sobrou no documento
- [ ] Você consegue explicar a regra em uma frase

---

## Etapa 2 — Escrever os ADRs

**Pasta:** `docs/adr/` (template + quatro esqueletos já lá)

### O que fazer

Preencha os quatro ADRs que já existem. Eles cobrem decisões que você
**viveu**, nos módulos 05, 06 e 10:

| # | Decisão | Módulo |
|---|---------|--------|
| 0001 | Persistência poliglota | M05 |
| 0002 | Autenticação por token | M06 |
| 0003 | Quarentena em vez de abortar | M10 |
| 0004 | Lago em arquivos, não em tabelas | M10 |

### 🔑 A seção que quase todo mundo escreve mal

**"Alternativas consideradas."**

É tentador escrever *"consideramos X, mas era pior"*. Isso não vale
nada. O que vale é o **argumento real da alternativa** — o mais forte
que você conseguir formular — seguido do motivo específico pelo qual
ele perdeu **naquele contexto**.

Teste: se alguém ler o seu ADR e ainda assim propuser a mesma
alternativa daqui a seis meses, a seção falhou.

### ⚠️ E a seção que quase todo mundo omite

**"Consequências negativas."**

Um ADR que só lista benefícios é propaganda. Escreva o que a decisão
**custou** — porque é isso que, no dia do problema, permite reconhecer
"isto é o preço que a gente aceitou pagar" em vez de "isto é um bug".

### 💭 Sobre escrever ADR de decisão antiga

Você está documentando decisões de meses atrás. Isso tem um risco: a
tentação de escrever a versão **esperta** — a que você contaria hoje,
sabendo o que sabe agora.

Resista. Escreva o que você sabia **na época**, inclusive o que você
não sabia. Um ADR honesto sobre uma decisão tomada com informação
incompleta ensina muito mais que uma reconstrução impecável.

### ✅ Pronto quando

- [ ] Os quatro ADRs estão preenchidos e datados
- [ ] Cada um tem pelo menos duas alternativas com argumento real
- [ ] Cada um tem consequências **negativas** listadas
- [ ] Cada um tem um gatilho concreto de "quando revisitar"
- [ ] O índice em `docs/adr/README.md` está atualizado

---

## Etapa 3 — 🔑 Verificar as camadas

**Arquivo:** `scripts/verificar_camadas.py` (esqueleto)

### O que fazer

Implemente o verificador: ele lê os imports com `ast`, monta o grafo e
reprova quem importa para cima.

### Por que `ast` e não `import`

Importar para analisar **executa** o módulo. Um módulo que abre
conexão no topo faria o seu verificador de arquitetura precisar de um
Postgres no ar para rodar. Análise estática lê o texto.

### ⚠️ As três armadilhas do leitor de imports

| Caso | O que acontece se você não tratar |
|------|-----------------------------------|
| `from atlas import modelos` | O nome está em `names`, não em `node.module` — passa batido |
| `from .modelos import Pedido` | Import **relativo**: `node.level == 1`. Ignorá-lo cega o verificador para metade do projeto |
| Módulo fora de `CAMADAS` | 🔴 Se você ignorar o desconhecido, todo arquivo novo é aprovado por omissão |

> 🔑 A terceira é a pior, e é a mais fácil de escrever sem perceber.
> Um `if modulo not in CAMADAS: continue` transforma o seu verificador
> num carimbo: basta criar um módulo novo para ficar fora da regra.
> Trate o desconhecido como **erro**, não como "tudo bem".

### ✅ Pronto quando

- [ ] `python scripts/verificar_camadas.py --mapa` imprime o grafo
- [ ] Ele detecta ciclos, não só violações de camada
- [ ] Violações saem no formato `arquivo:linha:`
- [ ] Módulo não classificado **reprova**, não é ignorado
- [ ] 🔑 Você **plantou uma violação** e viu o script reprovar

---

## Etapa 4 — Ligar ao CI

**Arquivo:** `.github/workflows/ci.yml`

### O que fazer

Acrescente um passo que roda `verificar_camadas.py`. Se ele devolver
1, o PR não passa.

```yaml
# TODO: acrescente ao job de qualidade
- name: Verificar camadas
  run: python scripts/verificar_camadas.py
```

### 🔴 E depois quebre de propósito

Você aprendeu isto no M09, do jeito difícil: **um portão que você
nunca viu reprovar não é um portão.**

```bash
# 1. plante a violação
#    em src/atlas/api/rotas/produtos.py, acrescente:
#    from atlas.repositorio import buscar_produto
# 2. commite numa branch e abra o PR
# 3. o CI DEVE ficar vermelho
# 4. remova, e confirme que fica verde
```

> ⚠️ Se o CI passou com a violação plantada, o problema pode não ser o
> script: confira se o passo foi adicionado ao job **certo**, se ele
> roda antes de algum `continue-on-error`, e se o `run` está usando o
> Python do ambiente onde `src/` é visível.

### ✅ Pronto quando

- [ ] O passo está no `ci.yml`
- [ ] Violação plantada deixa o CI **vermelho**
- [ ] Removida, o CI volta ao verde

---

## Etapa 5 — Consertar (ou declarar)

### 🔧 A violação que o seu projeto tem hoje

Se você classificou os módulos como sugerido, o verificador vai
acusar exatamente uma coisa no Atlas como ele está:

```
cli.py:22: 🔴 cli → ACESSO 'leitura' (pulando SERVIÇO)
```

**É uma violação real, e ela tem história.** No Módulo 01 não existia
camada de serviço — a CLI lia o CSV direto porque não havia mais nada.
Isso ficou, atravessou o M04, o M05 e o M06, e ninguém notou porque
funciona.

É o retrato do problema deste módulo inteiro: **o código carrega
decisões de uma época que já passou, e nada avisa.**

Três respostas possíveis, em ordem de qualidade:

| Resposta | Quando é a certa |
|----------|------------------|
| Mover a leitura para trás de um serviço | 🥇 quase sempre — é a correção de verdade |
| Reclassificar `leitura` como APOIO | 🥈 se ela for mesmo só "ler arquivo", sem regra |
| Declarar exceção com motivo | 🥉 se você decidir que a CLI legada fica como está |

> 💡 Escolha uma, execute, e **escreva um ADR sobre a escolha**. Esta
> é a sua primeira decisão de arquitetura registrada no momento em que
> foi tomada, e não meses depois — que é o ponto do módulo.

### O caso geral

Para cada violação que sobrou, uma de duas decisões:

**Consertar** — a função está na camada errada. Mova.

> 💡 O sintoma mais comum: uma função em `servicos.py` que monta HTML,
> ou uma em `repositorio.py` que aplica regra de negócio. As duas se
> resolvem movendo, não com exceção.

**Declarar a exceção** — a violação é legítima. Acrescente em
`EXCECOES` **com o motivo e o número do ADR**.

> 🔴 O critério para a segunda opção: você consegue escrever o motivo
> numa frase que convença outra pessoa? Se o motivo for "senão dá
> trabalho", é a primeira opção.
>
> E um alerta: se `EXCECOES` passar de três ou quatro entradas, o
> problema provavelmente não são as exceções — é o **mapa de camadas**
> que não corresponde ao sistema real. Volte à etapa 1.

### ✅ Pronto quando

- [ ] `python scripts/verificar_camadas.py` sai com código 0
- [ ] Toda entrada em `EXCECOES` tem motivo escrito
- [ ] O mapa gerado está colado em `docs/ARQUITETURA.md`

---

## O que você tem no fim

```
projeto_Atlas/
├── docs/
│   ├── ARQUITETURA.md          ← o mapa, e a regra
│   └── adr/
│       ├── README.md           ← índice e convenções
│       ├── 0000-template.md
│       └── 0001..0004-*.md     ← o porquê, preservado
└── scripts/
    └── verificar_camadas.py    ← 🔑 a regra que se prova sozinha
```

E, no CI, um portão a mais: agora o sistema **não deixa** a
arquitetura apodrecer em silêncio.

---

## O fecho

Arquitetura não é o desenho bonito no início do projeto. É o conjunto
de decisões que sobreviveram ao contato com o código — e a única
diferença entre um sistema com arquitetura e um sem é se essas
decisões estão **escritas** e **verificadas**.

Antes deste módulo, o Atlas tinha camadas porque você lembrava delas.
Agora tem camadas porque o CI não deixa ser diferente.

---

*Atlas · Aurora Comércio · Módulo 11*
