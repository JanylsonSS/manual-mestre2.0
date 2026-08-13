# Arquitetura de dados — Atlas

> **Entregável do Módulo 05.**
>
> Este é um documento de **decisão arquitetural**. Ele não descreve o que o
> código faz — descreve **por que** ele é assim, e o que foi descartado.
>
> Daqui a um ano, alguém (talvez você) vai perguntar "por que diabos temos dois
> bancos?". Este arquivo é a resposta.

---

## 1. O problema

> *"O SQLite não aguenta mais. Quando o financeiro roda o fechamento e alguém
> tenta gravar um pedido, dá `database is locked`. E o catálogo mudou de novo:
> agora tem cadeira gamer, com altura regulável e peso suportado."*

### As duas dores, separadas

| Dor | Natureza | Solução avaliada |
|-----|----------|------------------|
| Concorrência de escrita | | |
| Estrutura variável do catálogo | | |

<!-- TODO: preencha. Repare que são problemas INDEPENDENTES —
     e é possível que exijam soluções independentes. -->

---

## 2. A decisão

| Dado | Banco | Justificativa |
|------|-------|---------------|
| Clientes | | |
| Pedidos | | |
| Itens de pedido | | |
| Catálogo de produtos | | |
| Log de execuções | | |

<!-- TODO -->

---

## 3. 🎯 Alternativas descartadas

Esta é a seção mais importante do documento. Uma decisão sem alternativas
consideradas não é uma decisão — é um acidente.

### 3.1 Só PostgreSQL, com JSONB para o catálogo

| A favor | Contra |
|---------|--------|
| | |

**Por que não escolhemos (ou escolhemos):**

<!-- TODO. Seja honesto: o JSONB resolveria o problema do catálogo?
     Na aula 05_01 você viu que sim, em boa medida. O que exatamente
     o MongoDB oferece a mais que justifique um segundo banco? -->

### 3.2 Só MongoDB, para tudo

| A favor | Contra |
|---------|--------|
| | |

<!-- TODO. Pense em: transação entre pedido e estoque; relatórios do
     time de BI; integridade referencial; quem sabe pipeline de
     agregação na empresa. -->

### 3.3 Continuar no SQLite

<!-- TODO. Existe uma configuração de SQLite (WAL, timeout maior,
     fila de escrita na aplicação) que resolveria o `database is
     locked` da Aurora? Qual o volume real de escrita concorrente? -->

### 3.4 A alternativa que você NÃO considerou antes de escrever isto

<!-- TODO: pesquise uma. Exemplos: DuckDB para o analítico,
     Postgres com particionamento, um cache Redis na frente. -->

---

## 4. 💰 Custo operacional assumido

Toda arquitetura tem um custo recorrente. Liste o seu.

| Item | Antes (SQLite) | Depois (Postgres + Mongo) |
|------|----------------|---------------------------|
| Serviços a manter no ar | 0 | |
| Backups a configurar | 1 arquivo | |
| Monitoramento | — | |
| Conhecimento exigido da equipe | | |
| Tempo de setup de um dev novo | | |
| Custo de infraestrutura/mês | R$ 0 | |

**A pergunta:** o ganho justifica esse custo **hoje**, com o volume atual da
Aurora?

<!-- TODO -->

---

## 5. 🔴 Integridade entre os bancos

O `itens_pedido` (PostgreSQL) referencia produtos que vivem no MongoDB. **Não
há chave estrangeira possível.**

### O que pode dar errado

| Cenário | Consequência | Detecção |
|---------|--------------|----------|
| Produto removido do catálogo | | |
| SKU digitado errado no pedido | | |
| Catálogo restaurado de backup antigo | | |
| Migração parcial (Postgres ok, Mongo falhou) | | |

<!-- TODO -->

### Como mitigamos

<!-- TODO. Opções a considerar:
     • soft delete no catálogo (nunca remover de verdade)
     • job de reconciliação periódico
     • espelho dos campos estáveis no Postgres
     • validação na escrita (a aplicação confere antes de gravar)

     Qual você escolheu? Qual o custo? -->

### A consulta de reconciliação

```python
# TODO: cole aqui a consulta que encontra pedidos referenciando
#       produtos inexistentes. Ela deve rodar periodicamente.
```

---

## 6. O que a modelagem perdeu

Coisas que eram triviais no M03/M04 e ficaram mais difíceis:

| Antes | Agora | Impacto |
|-------|-------|---------|
| `LEFT JOIN produtos ... IS NULL` (produtos sem giro) | | |
| `JOIN` para margem por categoria | | |
| Transação cobrindo pedido + baixa de estoque | | |
| Um único backup | | |

<!-- TODO -->

---

## 7. Modelagem do catálogo

### O que ficou na raiz e o que ficou em `specs`

| Campo | Onde | Critério |
|-------|------|----------|
| `sku` | raiz | |
| `preco` | raiz | |
| `categoria` | raiz | |
| `ram_gb` | specs | |
| `peso_max_kg` | specs | |
| `cor` | ? | <!-- 🤔 todo produto tem cor? --> |

**A regra que você aplicou:**

<!-- TODO -->

### Embutir × referenciar

| Dado | Decisão | Justificativa (com o critério de crescimento) |
|------|---------|-----------------------------------------------|
| `specs` no produto | | |
| `tags` no produto | | |
| Itens no pedido | | |
| Snapshot do cliente no pedido | | |
| Avaliações do produto | | |

---

## 8. Migrações

### Estratégia

<!-- TODO: como você lida com o fato de que o Postgres tem migração
     versionada (Alembic) e o Mongo não tem nada equivalente?

     O Mongo precisa de migração? Quando? Como você versiona uma
     mudança de formato de documento? -->

### As quatro migrações criadas

| # | O quê | Reversível? | Observação |
|---|-------|:-----------:|------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

---

## 9. Medições

### 9.1 Equivalência com o M04

```
TODO: cole a saída de scripts/comparar_m04_m05.py
```

**Divergências e suas causas:**

| Relatório | Diferença | Causa | Qual está correto? |
|-----------|-----------|-------|--------------------|
| | | | |

<!-- 💡 Espere diferenças de centavos: float (M04) vs NUMERIC (M05).
     Agora o valor CORRETO é o do M05. -->

### 9.2 Desempenho

Rode 5 vezes, use a mediana.

| Operação | SQLite (M04) | PostgreSQL | MongoDB |
|----------|--------------|------------|---------|
| Buscar 1 pedido completo | | | — |
| Faturamento por cidade | | | |
| Inserir 1.000 pedidos | | | |
| Buscar produto por atributo | | | |
| 10 escritas concorrentes | | | |

<!-- 💭 A última linha é a que justifica a migração. Meça de verdade:
     dispare 10 threads escrevendo e veja o que acontece nos dois. -->

### 9.3 Contagem de consultas

| Operação | Consultas SQL | Consultas Mongo |
|----------|:-------------:|:---------------:|
| Listar 50 pedidos | | |
| Relatório por cidade | | |
| Página de produto | | |

<!-- 🔴 Se listar 50 pedidos faz mais de ~5 consultas, há N+1.
     Inclusive entre bancos. -->

---

## 10. 🎯 O teste do desenho do M04

Quantas linhas de cada arquivo precisaram mudar?

| Arquivo | Linhas alteradas | Esperado? |
|---------|:----------------:|-----------|
| `modelos.py` (domínio) | | |
| `servicos.py` | | |
| `apresentacao.py` | | |
| `regras.py` | | |
| `observabilidade.py` | | |
| `cli.py` | | |
| `repositorio.py` | | |

**Conclusão:**

<!-- TODO. Se só o repositório mudou, você separou domínio de
     persistência corretamente no M04.

     Se `servicos.py` mudou muito, houve vazamento — e vale identificar
     exatamente qual acoplamento causou isso. Essa é a lição mais
     valiosa deste módulo. -->

---

## 11. Rollback

Se esta arquitetura se mostrar errada, como voltar?

<!-- TODO: um plano concreto, não "restaurar backup".
     • Os dados do Mongo cabem de volta numa coluna JSONB?
     • Quanto tempo levaria?
     • O que se perderia?
     • Existe um caminho de volta parcial (só o catálogo)? -->

---

## 12. Se a equipe fosse menor

Você é a **primeira** pessoa de engenharia da Aurora. Amanhã contratam mais um.

**Com 2 pessoas, você manteria esta arquitetura?**

<!-- TODO. Seja honesto.

     💭 "Não, eu usaria só Postgres com JSONB" é uma resposta
        perfeitamente válida — e mais madura que a alternativa de
        defender uma decisão por orgulho.

     A pergunta de verdade é: quanta complexidade operacional a
     equipe consegue sustentar? -->

---

## 13. Revisão

| Data | Quem | O que mudou |
|------|------|-------------|
| | | |

<!-- 💡 Documento de arquitetura que nunca é revisado vira ficção.
     Marque uma data para reler isto: depois do M09, quando você
     tiver operado essa arquitetura em CI/CD, as respostas podem
     ser bem diferentes. -->
