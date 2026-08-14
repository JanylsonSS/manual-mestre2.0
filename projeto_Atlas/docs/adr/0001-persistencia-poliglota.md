# 0001 · Adotar persistência poliglota (PostgreSQL + MongoDB)

- **Estado:** _(preencha — provavelmente `Aceito`)_
- **Data:** _(preencha — a data em que você fez o M05)_
- **Decidido por:** _(preencha)_

---

## Contexto

> 🔧 Você viveu esta decisão no **Módulo 05**. Reconstrua o momento.

O que estava doendo, nas palavras da Aurora:

> *"O SQLite não aguenta mais. Quando o financeiro roda o fechamento e
> alguém tenta gravar um pedido, dá `database is locked`. E o catálogo
> mudou de novo: agora tem cadeira gamer, com altura regulável e peso
> suportado. Vou criar 40 colunas nulas?"*

Repare que são **dois** problemas diferentes numa frase só.
_(preencha: quais são, e por que exigem respostas diferentes)_

_(preencha o resto do contexto: volume na época, tamanho do time,
o que já existia do M03/M04)_

---

## Decisão

_(preencha em voz ativa, uma ou duas frases)_

---

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| Continuar no SQLite | _(preencha)_ |
| Só PostgreSQL, catálogo em `JSONB` | _(preencha — 🔑 esta é a alternativa forte, e a que mais gente propõe depois. Trate-a com seriedade: o Postgres **tem** JSONB e indexação GIN. Por que não bastou?)_ |
| Só MongoDB, tudo dentro | _(preencha — pense no pedido com três itens e no estoque)_ |

---

## Consequências

**Positivas**

- _(preencha)_

**Negativas / custos aceitos**

- _(preencha — 🔴 comece por esta: não há chave estrangeira entre os
  dois bancos. Um pedido pode referenciar um produto que não existe.
  O que o Atlas faz a respeito? Onde mora essa reconciliação?)_
- _(preencha: dois bancos para subir, monitorar, versionar, restaurar)_

**O que passa a ser proibido**

- _(preencha — pense em `JOIN` entre pedido e produto)_

---

## Quando revisitar

_(preencha um gatilho concreto)_
