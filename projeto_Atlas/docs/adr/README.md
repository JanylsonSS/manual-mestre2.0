# Registros de Decisão de Arquitetura (ADR)

> *"Ninguém sabe por que o sistema é assim."*

---

## O problema que os ADRs resolvem

Daqui a oito meses, alguém — provavelmente você — vai abrir
`repositorio.py`, ver que o Atlas usa **dois bancos** e pensar:

> *"Que exagero. Dá para fazer tudo no Postgres. Vou simplificar."*

E vai começar a simplificar. Até descobrir, três dias depois, que o
catálogo tem estrutura diferente por categoria e que foi exatamente
por isso que o Mongo entrou.

Três dias perdidos por causa de uma decisão de vinte minutos que
ninguém escreveu.

> 🔑 **O ADR não existe para justificar a decisão. Existe para
> preservar o CONTEXTO em que ela foi tomada** — as restrições, as
> alternativas e o que se sabia na época.
>
> Isso é o que permite **rever** a decisão com honestidade mais tarde:
> se as restrições mudaram, a decisão pode mudar. Se não mudaram, não
> perca os três dias.

---

## O que é (e o que não é)

| É | Não é |
|---|---|
| Uma decisão **significativa**, com contexto | Documentação de API |
| Curto: uma página, no máximo | Um manual de uso |
| **Imutável** depois de aceito | Um documento vivo que se edita |
| Datado e numerado | Um wiki |

> 🔴 **ADR aceito não se edita.** Se a decisão mudou, você escreve um
> **novo** ADR que substitui o anterior, e marca o antigo como
> `Substituído por 0009`.
>
> Editar o antigo apaga a única coisa que o tornava valioso: o
> registro de que, naquele momento, com aquelas informações, aquela
> era a decisão certa. Um ADR reescrito vira profecia — e profecia
> não ensina ninguém.

---

## O que merece um ADR

O teste: **alguém vai questionar isso depois?**

| Merece | Não merece |
|---|---|
| Escolher PostgreSQL + MongoDB | Nome de variável |
| Usar JWT em vez de sessão | Formatação do código |
| Rejeitar linha ruim vs. abortar o lote | Qual biblioteca de datas |
| Não ter réplica de leitura (ainda) | Ordem dos imports |
| Adotar `Decimal` para dinheiro | Adicionar um endpoint novo |

> 💭 Se você está em dúvida se algo merece ADR, provavelmente merece.
> O custo de escrever um a mais é quinze minutos. O custo de não ter
> escrito o que faltava são os três dias lá de cima.

---

## Como usar

```bash
# 1. copie o template
cp docs/adr/0000-template.md docs/adr/0009-titulo-curto.md

# 2. preencha, commite junto com a mudança que ele descreve
git add docs/adr/0009-titulo-curto.md src/atlas/...
git commit -m "docs(adr): registra decisão sobre X"
```

> 🔑 **Commite o ADR junto com o código.** Não depois. O ADR que fica
> "para escrever na sexta" nunca é escrito, porque na sexta o contexto
> já evaporou — e o contexto era o produto.

**Numeração:** sequencial, quatro dígitos, nunca reaproveitada. Se um
ADR for rejeitado, o número morre com ele.

---

## Estados

| Estado | Significa |
|--------|-----------|
| `Proposto` | Em discussão |
| `Aceito` | Vale agora |
| `Rejeitado` | Foi considerado e descartado — 🔑 **mantenha o arquivo** |
| `Substituído por NNNN` | Outro ADR tomou o lugar |
| `Obsoleto` | Não se aplica mais (o componente sumiu) |

> ⚠️ ADR **rejeitado se guarda**. "Já pensamos em Kafka e decidimos
> que não, porque X" economiza a próxima discussão inteira. Apagar o
> rejeitado é garantir que a ideia volte a cada seis meses.

---

## Índice

_(mantenha esta tabela atualizada — é por ela que alguém acha o que
procura)_

| # | Título | Estado | Data |
|---|--------|--------|------|
| [0001](0001-persistencia-poliglota.md) | Persistência poliglota: PostgreSQL + MongoDB | _(preencha)_ | |
| [0002](0002-autenticacao-por-token.md) | Autenticação por token JWT | _(preencha)_ | |
| [0003](0003-quarentena-em-vez-de-abortar.md) | Quarentena em vez de abortar o lote | _(preencha)_ | |
| [0004](0004-lago-em-arquivos.md) | Lago em arquivos Parquet, não em tabelas | _(preencha)_ | |

---

*Atlas · Aurora Comércio · Módulo 11*
