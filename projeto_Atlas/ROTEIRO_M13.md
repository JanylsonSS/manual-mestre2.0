# Roteiro — Módulo 13 · Atlas 1.0

> **Objetivo:** transformar treze entregas separadas numa coisa só, com
> nome, número de versão e um caminho de volta.

O último. Sem notebooks, sem funcionalidade nova.

---

## A situação

Você tem um sistema que funciona. E tem, espalhados por doze módulos:

- treze portões de qualidade, cada um construído e depois esquecido
- documentos com `_(preencha)_` que você ia terminar depois
- uma versão `0.7.0` no `pyproject.toml` que ficou parada no M07
- nenhum changelog
- nenhum jeito de dizer, com uma palavra, "isto aqui está pronto"

> 💭 Nada disso impede o sistema de rodar. É justamente por isso que
> fica para depois — e "depois" chega no dia em que alguém pergunta
> "que versão está em produção?" e a resposta honesta é "não sei".

---

## Ordem de trabalho

```
1. Fechar as pontas       ← os (preencha) que sobraram
2. Versionar              ← uma fonte de verdade
3. Changelog              ← o que mudou, para quem usa
4. O portão de release    ← 🔑 todos os portões, juntos
5. Provar                 ← 🔑🔑 quebre, e veja ficar vermelho
6. Publicar e apresentar
```

---

## Etapa 1 — Fechar as pontas

### O que fazer

```bash
grep -rn "(preencha)" docs/ *.md
```

Cada ocorrência é uma promessa que você fez a si mesmo.

### 🔴 Priorize por quem vai ler, e quando

| Documento | Prioridade | Por quê |
|-----------|-----------|---------|
| `RUNBOOK.md` | 🔴 crítica | alguém vai ler às 3h, com o site fora |
| `PIPELINE.md` § 5 | 🔴 crítica | idem, com o pipeline quebrado |
| `METRICAS.md` | 🔴 crítica | encerra a discussão do fechamento mensal |
| `adr/*.md` | alta | é o porquê, e ele evapora |
| `ARQUITETURA.md` | alta | é a regra que o CI aplica |
| `REFATORACAO.md`, `CSV_VS_SQL.md` | média | histórico, não operação |

> ⚠️ Um documento com o gabarito intacto é **pior que nenhum**: dá a
> impressão de que existe documentação, e alguém vai contar com ela na
> pior hora possível. Se você não vai preencher, **apague a seção** —
> é mais honesto.

### ✅ Pronto quando

- [ ] Nenhum `_(preencha)_` nos três documentos críticos
- [ ] Os quatro ADRs estão completos e datados
- [ ] O índice de `docs/adr/README.md` está atualizado

---

## Etapa 2 — Versionar

### O que fazer

1. `pyproject.toml` → `version = "1.0.0"`
2. Uma **fonte de verdade** para o número:

```python
# src/atlas/__init__.py
from importlib.metadata import version
__version__ = version("atlas")
```

3. Exponha na API (`GET /saude` devolvendo a versão) e no log de
   inicialização.

> 🔴 Duas fontes de verdade para a mesma informação sempre divergem. A
> única dúvida é quando. Se `__init__.py` repetir o número à mão,
> algum dia o pacote vai dizer 1.0.0 e o log vai dizer 0.9.3 — e você
> vai depurar a versão errada do código.

### 💭 O que 1.0 significa

Não é "está pronto". Software não fica pronto. É um **compromisso**:

- a API v1 é estável — o que está em `docs/API.md` não muda sem
  incremento MAIOR;
- existe caminho de volta (rollback em um comando);
- existe caminho de diagnóstico (runbook);
- as decisões estão registradas (ADRs).

Se você não pode assumir os quatro, chame de `0.13.0` e siga. Um 1.0
prematuro é uma promessa que você vai quebrar na semana seguinte.

### ✅ Pronto quando

- [ ] A versão aparece em **um** lugar e é lida de lá
- [ ] `GET /saude` devolve a versão
- [ ] O log de inicialização registra a versão

---

## Etapa 3 — Changelog

**Arquivo:** `CHANGELOG.md` (já criado, com gabarito)

### A distinção que faz o documento valer

`git log` diz o que mudou **no código**. O changelog diz o que mudou
**para quem usa**. Por isso ele é escrito para humanos e omite as
duzentas linhas de refatoração que ninguém de fora percebe.

> 🔑 O teste: alguém que consome a API consegue decidir, lendo só o
> changelog, se precisa mexer em algo antes de atualizar?

### ⚠️ A regra de SemVer que quase todo mundo erra

Acrescentar um campo **obrigatório** num corpo de requisição é mudança
**MAIOR**, não menor. Todo cliente que não manda o campo passa a
receber 422.

Campo opcional com padrão é menor. A diferença é "código de terceiros
que funcionava para de funcionar" — e é essa a definição de quebra,
não o tamanho do diff.

### ✅ Pronto quando

- [ ] Há uma seção `[1.0.0]` com data
- [ ] As entradas descrevem o efeito para quem usa, não o commit
- [ ] Há uma seção `[Não publicado]` para o que vier depois

---

## Etapa 4 — 🔑 O portão de release

**Arquivo:** `scripts/verificar_release.py` (esqueleto)

### O que fazer

Implemente o agregador: ele roda todos os portões dos doze módulos e
dá um veredito.

### Ordene do mais barato ao mais caro

Se as camadas estão quebradas, não faz sentido esperar quatro minutos
de mutação para descobrir isso.

```
segundos     camadas · segredos · .env · versão · changelog
dezenas      suíte rápida · cobertura · containers · transação
minutos      isolamento · idempotência · portão de qualidade · mutação
```

### ⚠️ Nem todo portão bloqueia

| Peso | Para o quê |
|------|-----------|
| 🔴 `BLOQUEIA` | o que é objetivamente errado (camada quebrada, segredo no código, teste falhando) |
| ⚠️ `AVISA` | o que oscila por motivo legítimo (escore de mutação, doc secundário incompleto) |

> 💭 A mutação é `AVISA` de propósito. O escore varia com refatoração
> honesta, e um bloqueio que reprova por motivo justo com frequência
> ensina a equipe a contornar — e aí ele deixou de existir. Você já
> viu esse mecanismo no M10, com o `--forcar` do pipeline.

### 🔴 E o que este script não é

Ele **não** é garantia de que o sistema funciona. É a verificação de
que as suas verificações continuam passando.

> Um agregador de portões herda a qualidade dos portões que agrega. Se
> um portão foi mal escrito no M09, ele continua mal escrito aqui — só
> que agora com um ✅ verde ao lado, o que é pior que não ter portão.

### ✅ Pronto quando

- [ ] Roda todos os portões e mostra o tempo de cada um
- [ ] Distingue `BLOQUEIA` de `AVISA`
- [ ] Cada falha diz **onde consertar** (roteiro e etapa)
- [ ] Devolve código de saída 1 quando bloqueado

---

## Etapa 5 — 🔑🔑 Provar

A última etapa do manual, e a mais importante.

### Quebre uma coisa de cada vez, e exija vermelho

| Quebre | Portão que deve pegar |
|--------|----------------------|
| `from atlas.repositorio import ...` numa rota | M11 camadas |
| `ATLAS_SECRET_KEY = "abc123"` no código | M09 segredos |
| Troque `>` por `>=` numa regra de preço | M12 mutação/testes |
| Apague uma asserção de um teste | M12 mutação |
| `datetime.now()` dentro de `construir_ouro` | M10 idempotência |
| Duplique 10 linhas na prata | M10 portão de qualidade |
| `USER root` no Dockerfile | M08 containers |
| Comente o `rollback` da transação | M06 transação parcial |

**Oito quebras, oito vermelhos.** Se alguma passar verde, você
encontrou um portão decorativo — e encontrou barato.

> 🔑 Esta tabela é o manual inteiro em oito linhas. Cada uma dessas
> quebras é indetectável a olho nu, funciona perfeitamente, e produz
> ou um número errado ou uma porta aberta.

### ✅ Pronto quando

- [ ] As oito quebras foram testadas
- [ ] As oito ficaram vermelhas
- [ ] Você consertou qualquer portão que passou verde

---

## Etapa 6 — Publicar e apresentar

### Publicar

```bash
# 1. tudo verde
python scripts/verificar_release.py

# 2. tag anotada (não leve — a anotada guarda autor, data e mensagem)
git tag -a v1.0.0 -m "Atlas 1.0"
git push origin v1.0.0
```

> 💡 `git tag v1.0.0` (leve) cria só um ponteiro. `git tag -a` cria um
> objeto com metadados — e é o que ferramentas de release esperam
> encontrar.

### Apresentar

**`docs/APRESENTACAO.md`** tem o roteiro de 10 minutos.

O resumo dele: comece pela dor, mostre o sistema, e **reserve três
minutos para quebrar alguma coisa ao vivo**. É a parte que diferencia
— qualquer demonstração mostra o caminho feliz.

### ✅ Pronto quando

- [ ] `v1.0.0` está publicada
- [ ] A demonstração de falha foi ensaiada **duas vezes**
- [ ] Existe um plano B com a saída gravada, caso a demo trave

---

## O que você tem no fim

```
projeto_Atlas/                      Atlas 1.0
├── src/atlas/
│   ├── api/          ← responde em milissegundos
│   └── dados/        ← roda uma vez por noite
├── tests/            ← unidade + integração
├── docs/
│   ├── adr/          ← o porquê de cada decisão
│   ├── RUNBOOK.md    ← para as 3h da manhã
│   ├── PIPELINE.md   ← idem, para o pipeline
│   ├── METRICAS.md   ← qual número é o certo
│   └── APRESENTACAO.md
├── scripts/
│   ├── verificar_camadas.py
│   ├── testar_os_testes.py
│   └── verificar_release.py   ← 🔑 todos os portões
└── CHANGELOG.md
```

---

## O fecho do projeto

No Módulo 01 você escreveu um laço de `for` sobre um CSV para
responder *"quanto vendemos por cidade?"*.

A pergunta continua a mesma. O que mudou é tudo que acontece em volta
dela: o dado vem de três origens sem derrubar o banco do cliente; o
que não presta vai para a quarentena em vez de sumir; seis
verificações rodam antes de publicar; nada é publicado se não houver
confiança; rodar de novo dá o mesmo resultado; subir versão é um
`push`; voltar atrás é um comando; cada decisão tem um documento; e o
CI não deixa a arquitetura apodrecer.

> 🔑 Nenhuma dessas coisas é sobre fazer o programa funcionar. Todas
> são sobre o que acontece **quando algo dá errado** — que é, no fim,
> a única diferença entre um script e um sistema.

E se houver uma ideia para levar daqui, é a que apareceu em oito
módulos diferentes, sempre do mesmo jeito e sempre por acidente:

> **Toda salvaguarda precisa ser vista falhando pelo menos uma vez.**
> Até lá, ela é uma esperança com aparência de garantia.

O portão de segredos que passou porque a palavra estava no arquivo. A
bateria de idempotência que aprovou um pipeline vazio. A regra de
camadas que aprovou SQL dentro de uma rota. A suíte de 70% que deixou
passar o erro de uma letra. Nenhum desses defeitos apareceu lendo o
código — todos apareceram ao atacar a própria verificação.

Faça isso com o que você construir depois daqui.

---

*Atlas 1.0 · Aurora Comércio · fim do projeto*
