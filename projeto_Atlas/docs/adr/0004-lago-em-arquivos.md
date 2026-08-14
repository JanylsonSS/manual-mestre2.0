# 0004 · Manter o lago em arquivos Parquet, não em tabelas

- **Estado:** _(preencha)_
- **Data:** _(preencha — Módulo 10)_
- **Decidido por:** _(preencha)_

---

## Contexto

> 🔧 Módulo 10.

O Atlas já tem um PostgreSQL rodando. Seria natural criar um schema
`analitico` e gravar bronze/prata/ouro em tabelas. Em vez disso, o
pipeline grava arquivos `.parquet` particionados em disco.

_(preencha: por que a pergunta "por que não tabelas?" é legítima, e
quais restrições você tinha)_

---

## Decisão

_(preencha)_

---

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| Schema `analitico` no mesmo Postgres | _(preencha — 🔑 pense em quem mais está usando aquele banco às 3h da manhã, e no custo de um `VACUUM` sobre 200 milhões de linhas)_ |
| Um Postgres separado só para análise | _(preencha — custo, e quem administra)_ |
| Data warehouse gerenciado (BigQuery, Redshift) | _(preencha — considere o tamanho da Aurora hoje)_ |

---

## Consequências

**Positivas**

- _(preencha — leitura colunar, partição vira filtro, custo zero de
  servidor, e o formato é lido por pandas, Polars, DuckDB e Spark sem
  conversão)_

**Negativas / custos aceitos**

- _(preencha — 🔴 arquivo não tem transação. O que acontece se alguém
  ler o ouro no meio da escrita? Qual é a defesa do Atlas?)_
- _(preencha — não há `UPDATE`. Corrigir uma linha significa
  reescrever a partição inteira.)_
- _(preencha — quem faz backup de uma pasta? O `bronze/` não é
  derivável de nada.)_

**O que passa a ser proibido**

- _(preencha)_

---

## Quando revisitar

_(preencha — sugestão: um volume, ou o dia em que mais de N pessoas
precisarem consultar o ouro ao mesmo tempo)_
