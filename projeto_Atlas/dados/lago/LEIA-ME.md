# `dados/lago/` — o lago de dados do Atlas

Este diretório é criado pelo pipeline (Módulo 10). Ele **não vai para
o Git** — só a estrutura vai, através dos `.gitkeep`.

```
lago/
├── bronze/       cru, como chegou       ← NUNCA se apaga
│   └── origem=<fonte>/data_ingestao=<AAAA-MM-DD>/
│       ├── dados.parquet
│       └── _manifesto.json
├── prata/        limpo, tipado, validado    ← derivável do bronze
├── ouro/         agregado, pronto           ← derivável da prata
├── quarentena/   o que não passou           ← evidência, não lixo
└── estado/       marcas d'água              ← onde a última rodada parou
```

## A regra que organiza tudo

**Toda camada é derivável da anterior.**

Apagar `prata/`, `ouro/` e rodar de novo tem que reconstruir tudo
igual. Apagar `bronze/` é perda permanente — ele é a única cópia do
que a origem realmente mandou naquele dia.

Por isso o `.gitignore` ignora o conteúdo, mas o `bronze/` de produção
precisa de backup de verdade. O resto, não.

## Por que `origem=` e `data_ingestao=` com sinal de igual

É o layout de partição Hive. Spark, DuckDB, Polars e Athena leem a
pasta **como coluna**:

```sql
SELECT * FROM 'lago/bronze/**/*.parquet'
WHERE data_ingestao = '2026-08-13'
```

Isso lê **uma pasta** em vez de varrer o lago inteiro. É a diferença
entre 2 segundos e 4 minutos quando o histórico crescer.

## Quarentena não é lixo

O que está em `quarentena/` é **evidência**. Uma linha rejeitada
significa que alguém — a origem, o parceiro, ou o seu contrato — está
errado. Se a taxa de rejeição saltar de 0,02% para 14% de um dia para
o outro, isso é um incidente, e a quarentena é onde está a explicação.

Olhe para ela toda semana. Uma quarentena que ninguém abre é um dado
perdido com passos extras.
