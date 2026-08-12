# Modelagem de dados — Atlas

> **Entregável do Módulo 03.**
>
> Preencha com **suas** decisões e justificativas. Um modelo de dados sem
> documentação é um modelo que ninguém ousa mudar daqui a seis meses.

---

## 1. A dor que originou este trabalho

> *"Os dados estão em 14 planilhas diferentes. A do comercial tem 'Campinas',
> a do financeiro tem 'campinas/SP', a do estoque tem 'CPS'. Quando alguém
> corrige o preço de um produto, corrige em uma planilha só. Ontem descobrimos
> que o mesmo cliente aparece 4 vezes com e-mails diferentes."*

### As anomalias do arquivo plano

Descreva, com um exemplo concreto **dos dados da Aurora**, cada uma:

| Anomalia | Exemplo real no CSV do M01 |
|----------|----------------------------|
| De atualização | <!-- TODO --> |
| De inserção | <!-- TODO --> |
| De remoção | <!-- TODO --> |

---

## 2. Entidades identificadas

Liste os substantivos do negócio que viraram tabelas, e por quê.

| Entidade | O que representa | Por que é uma tabela separada |
|----------|------------------|-------------------------------|
| `categorias` | | |
| `produtos` | | |
| `clientes` | | |
| `pedidos` | | |
| `itens_pedido` | | |

**Entidades que você considerou e decidiu NÃO criar** (e por quê):

<!-- TODO: ex.: 'enderecos', 'fornecedores', 'vendedores'... -->

---

## 3. Diagrama ER

<!--
TODO: desenhe em ASCII. Marque:
  🔑 chave primária
  🔗 chave estrangeira
  as cardinalidades (1─N, N─N)
  as ações referenciais em cada FK

Use o diagrama da aula 03_01 como referência de formato, mas
DESENHE O SEU — inclusive as tabelas que você adicionou.
-->

```
(seu diagrama aqui)
```

---

## 4. Decisões de chave

### 4.1 Chave primária: artificial ou natural?

| Tabela | PK escolhida | Chave natural protegida com UNIQUE | Justificativa |
|--------|--------------|-------------------------------------|---------------|
| `categorias` | | | |
| `produtos` | | | |
| `clientes` | | | |
| `pedidos` | | | |
| `itens_pedido` | | | |

**Pergunta a responder:** em `clientes`, por que `email` é `UNIQUE` mas **não** é a chave primária? O que aconteceria com a tabela `pedidos` se um cliente trocasse de e-mail?

<!-- TODO -->

### 4.2 A tabela de junção

`pedidos` e `produtos` têm relação **N para N**. Bancos relacionais não representam isso diretamente.

**Como você resolveu:**

<!-- TODO -->

**Por que `itens_pedido` tem atributos próprios (`quantidade`, `preco_unitario`)?** A quem eles pertencem — ao pedido, ao produto, ou à combinação?

<!-- TODO -->

---

## 5. 🔴 A pergunta central do módulo

**Por que `itens_pedido` guarda `preco_unitario`, se `produtos` já tem `preco`?**

Isso parece redundância — exatamente o que a normalização deveria eliminar. Explique por que **não é**.

*Dica para pensar: imagine que hoje é 12/08. Alguém reajusta o catálogo em 10%. Amanhã a diretora pede de novo o relatório de julho. O que acontece se o cálculo usar `produtos.preco`?*

<!-- TODO -->

**Como se chama esse padrão?** Onde mais ele aparece em sistemas transacionais?

<!-- TODO -->

---

## 6. Constraints

Para cada constraint que você criou, registre a **regra de negócio** que ela protege.

| Tabela | Constraint | Regra de negócio protegida |
|--------|-----------|----------------------------|
| `produtos` | `CHECK (preco >= custo)` | <!-- TODO --> |
| `produtos` | `CHECK (estoque >= 0)` | <!-- TODO --> |
| `clientes` | `CHECK (length(uf) = 2 AND uf = upper(uf))` | <!-- TODO --> |
| `pedidos` | `CHECK (status IN (...))` | <!-- TODO --> |
| `itens_pedido` | `UNIQUE (pedido_id, produto_id)` | <!-- TODO --> |
| <!-- TODO: as suas --> | | |

**Regras de negócio que o banco NÃO consegue garantir sozinho** (e onde elas ficam então):

<!-- TODO: ex.: "a quantidade devolvida não pode exceder a comprada" -->

---

## 7. Ações referenciais

| FK | Ação escolhida | Justificativa |
|----|----------------|---------------|
| `produtos.categoria_id` | | |
| `pedidos.cliente_id` | | |
| `itens_pedido.pedido_id` | | |
| `itens_pedido.produto_id` | | |

**Por que `CASCADE` em `itens_pedido.pedido_id` e `RESTRICT` em `itens_pedido.produto_id`?** As duas são FKs da mesma tabela — o que as torna diferentes?

<!-- TODO -->

**Em que situação `CASCADE` seria perigoso?**

<!-- TODO -->

---

## 8. Índices

Para **cada** índice criado, o `EXPLAIN QUERY PLAN` antes e depois.

### Índice 1: `<nome>`

**Consulta que ele acelera:**

```sql
-- TODO
```

**Antes:**
```
-- TODO: cole a saída do EXPLAIN QUERY PLAN
```

**Depois:**
```
-- TODO
```

<!-- TODO: repita para cada índice -->

### Índices que você decidiu NÃO criar

| Índice descartado | Por quê |
|-------------------|---------|
| `produtos(ativo)` | <!-- TODO: pense em cardinalidade --> |
| | |

### O índice composto

Você criou um índice em `pedidos(status, data_pedido)`. Teste as três consultas e registre qual usa o índice:

| Consulta | Usa o índice? | Por quê |
|----------|---------------|---------|
| `WHERE status = 'pago'` | | |
| `WHERE status = 'pago' AND data_pedido > '...'` | | |
| `WHERE data_pedido > '...'` | | |

**Como se chama essa regra?**

<!-- TODO -->

---

## 9. Tipos de dados

O SQLite não tem `BOOLEAN`, `DATE` nem `DECIMAL`. Como você resolveu cada caso:

| Precisava de | Guardei como | Convenção adotada |
|--------------|--------------|-------------------|
| Booleano (`ativo`) | | |
| Data (`data_pedido`) | | |
| Dinheiro (`preco`) | | |

**Sobre dinheiro em `REAL`:** qual o risco? (Revise `0.1 + 0.2 != 0.3` na aula 01_01.) Você considerou guardar centavos como `INTEGER`? Por que escolheu o que escolheu?

<!-- TODO -->

**Sobre datas:** por que ISO 8601 (`AAAA-MM-DD`) e não `DD/MM/AAAA`?

<!-- TODO -->

---

## 10. Normalização

Em que forma normal seu modelo está? Justifique verificando cada uma:

| Forma | Atendida? | Verificação |
|-------|-----------|-------------|
| 1FN — valores atômicos, sem grupos repetidos | | |
| 2FN — dependência da chave inteira | | |
| 3FN — sem dependência transitiva | | |

**Violação deliberada:** `clientes` guarda `cidade` **e** `uf`. Como `uf` é determinada por `cidade`, isso viola a 3FN. Por que você aceitou (ou não) essa violação?

<!-- TODO -->

---

## 11. Verificação: os números batem?

O critério final de aceitação da migração.

| Métrica | Módulo 01 (CSV) | Módulo 03 (SQL) | Diferença |
|---------|-----------------|-----------------|-----------|
| Faturamento total | | | |
| Pedidos pagos | | | |
| Itens vendidos | | | |
| Clientes distintos | | | |
| Cidade nº 1 | | | |
| Faturamento da cidade nº 1 | | | |

**Se houve diferença, qual foi a causa?**

<!-- TODO -->

---

## 12. O que eu faria diferente

<!--
TODO: escreva depois de terminar o projeto, não antes.
Que decisão de modelagem você tomou no começo e se arrependeu?
O que só ficou claro quando você foi escrever as consultas?
-->

---

## 13. Preparando o Módulo 05

No M05 este schema migra para PostgreSQL. Anote o que vai precisar mudar:

| Aqui (SQLite) | Lá (PostgreSQL) |
|---------------|-----------------|
| `INTEGER PRIMARY KEY` autoincrementa | <!-- TODO: pesquise SERIAL / IDENTITY --> |
| `REAL` para dinheiro | <!-- TODO: pesquise NUMERIC --> |
| `TEXT` para datas | <!-- TODO: DATE / TIMESTAMP --> |
| `INTEGER` 0/1 para booleano | <!-- TODO --> |
| `PRAGMA foreign_keys = ON` | <!-- TODO: precisa? --> |
| Afinidade de tipo permissiva | <!-- TODO --> |
| `GROUP BY` permissivo | <!-- TODO --> |
