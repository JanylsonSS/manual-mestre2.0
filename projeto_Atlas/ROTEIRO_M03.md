# Roteiro de implementação — Módulo 03 (SQL)

> **Pré-requisitos:** M01 funcionando (CLI gera relatórios do CSV) e M02 feito
> (projeto versionado no Git). Você vai comparar os números dos dois módulos —
> se o M01 não estiver correto, não há com o que comparar.

---

## A dor

> *"Os dados estão em 14 planilhas diferentes. A do comercial tem 'Campinas',
> a do financeiro tem 'campinas/SP', a do estoque tem 'CPS'. O mesmo cliente
> aparece 4 vezes com e-mails diferentes."*

## A entrega

Atlas lendo de um banco relacional SQLite, com schema modelado, migração
idempotente a partir dos CSVs, e relatórios escritos em SQL.

**Regra de ouro do módulo:** ao final, os números do relatório SQL devem bater
**exatamente** com os do Módulo 01. Se não baterem, um dos dois está errado —
e descobrir qual é parte do aprendizado.

---

## Etapa 0 — Branch e ferramenta (20 min)

```bash
git switch main && git pull
git switch -c feature/m03-banco-relacional
```

Instale um cliente visual para inspecionar o banco enquanto desenvolve:

- **VS Code:** extensão *SQLite Viewer* ou *SQLTools*
- **Desktop:** [DB Browser for SQLite](https://sqlitebrowser.org/) — recomendado

Poder abrir o `.db` e clicar nas tabelas acelera muito a depuração.

**Pronto quando:** você consegue abrir um `.db` de teste e ver as tabelas.

---

## Etapa 1 — Modelagem no papel (45 min)

**Antes de escrever uma linha de SQL**, preencha as seções 2, 3 e 4 de
`docs/MODELAGEM.md`:

- Liste as entidades
- Desenhe o ER com cardinalidades
- Decida as chaves

Responda especialmente a **seção 5**: por que `itens_pedido` guarda
`preco_unitario` se `produtos` já tem `preco`?

> 💭 Se você não consegue responder isso, não escreva o schema ainda. Essa
> pergunta é o coração da modelagem transacional.

**Pronto quando:** o diagrama está desenhado e você consegue explicar cada FK.

---

## Etapa 2 — Schema (60 min)

Complete `dados/schema.sql`.

Ordem sugerida — **das folhas para a raiz**, respeitando as dependências:

1. `categorias` (não depende de ninguém)
2. `produtos` (depende de categorias)
3. `clientes` (não depende de ninguém)
4. `pedidos` (depende de clientes)
5. `itens_pedido` (depende de pedidos e produtos)
6. Views

Aplique e confira:

```bash
sqlite3 dados/atlas.db < dados/schema.sql
sqlite3 dados/atlas.db "SELECT type, name FROM sqlite_master ORDER BY type, name;"
sqlite3 dados/atlas.db "PRAGMA foreign_key_list('itens_pedido');"
```

**Teste cada constraint tentando violá-la.** Um `CHECK` que você não testou é
um `CHECK` que talvez não funcione:

```bash
sqlite3 dados/atlas.db "INSERT INTO produtos (sku,nome,categoria_id,preco,custo) VALUES ('X','T',1,-10,5);"
# esperado: CHECK constraint failed
```

**Pronto quando:** todas as tabelas existem, e você conseguiu provocar erro em
cada constraint que criou.

---

## Etapa 3 — Camada de repositório (90 min)

Complete `src/atlas/repositorio.py`.

Ordem sugerida:

1. `conectar()` — o mais importante. Sem `PRAGMA foreign_keys = ON`, nada
   funciona de verdade.
2. `transacao()` — 10 linhas, protege todo o resto.
3. `criar_schema()` / `criar_indices()`
4. Os `upsert_*`
5. `executar_consulta()` e `executar_arquivo_sql()`
6. `estatisticas_banco()`

### 🔴 Autoauditoria de segurança

Antes de seguir, rode:

```bash
grep -n 'f"' src/atlas/repositorio.py
grep -n "'''" src/atlas/repositorio.py | grep -i select
grep -n '% (' src/atlas/repositorio.py
```

**Qualquer f-string que contenha um valor de variável dentro de SQL é uma
falha.** A única exceção legítima é nome de tabela validado contra lista branca
— e ela precisa estar explicitamente comentada como tal.

**Pronto quando:** `python src/atlas/repositorio.py` cria o schema e imprime as
contagens.

---

## Etapa 4 — Migração (90 min)

Complete `src/atlas/migracao.py`.

Ordem:

1. Os normalizadores (`normalizar_email`, `normalizar_cidade`, ...) — são
   funções puras, fáceis de testar mentalmente
2. `derivar_sku` e `inferir_categoria`
3. `migrar_csv` — o coração
4. `gravar_rejeitados`
5. `conferir_com_csv`
6. `testar_idempotencia`

### O teste que define a etapa

```bash
python main.py schema --recriar
python main.py migrar dados/brutos/vendas_jul2026.csv
python main.py status          # anote as contagens

python main.py migrar dados/brutos/vendas_jul2026.csv
python main.py status          # DEVE ser idêntico

python main.py migrar dados/brutos/vendas_jul2026.csv
python main.py status          # ainda idêntico
```

Depois, o teste de sujeira:

```bash
python main.py migrar dados/brutos/vendas_sujas.csv
# Não pode quebrar. Deve rejeitar as linhas ruins e relatar o motivo.
```

**Pronto quando:** três execuções seguidas produzem contagens idênticas, e o
CSV sujo é processado sem exceção.

---

## Etapa 5 — Consultas (120 min)

Complete os arquivos em `dados/consultas/`.

**Ordem sugerida** (da mais simples à mais elaborada):

1. `faturamento_por_cidade.sql` ← comece por esta, é a que compara com o M01
2. `faturamento_por_categoria.sql`
3. `top_produtos.sql`
4. `top_clientes.sql`
5. `alerta_estoque.sql`
6. `evolucao_mensal.sql`
7. `curva_abc.sql`
8. `qualidade_dados.sql`

### Método de trabalho

Não escreva a consulta inteira de uma vez. **Construa por camadas:**

```sql
-- 1. Comece pelo JOIN base e confira a contagem
SELECT COUNT(*) FROM itens_pedido i JOIN pedidos p ON p.id = i.pedido_id;

-- 2. Adicione o filtro
SELECT COUNT(*) FROM ... WHERE p.status = 'pago';

-- 3. Adicione o agrupamento
SELECT c.cidade, COUNT(*) FROM ... GROUP BY c.cidade;

-- 4. Só então as métricas calculadas
```

Rodar a consulta no DB Browser enquanto constrói é muito mais rápido que pelo
Python.

### ✅ A verificação obrigatória

```bash
python main.py relatorio faturamento_por_cidade    # via SQL
python main.py relatorio-csv                       # via M01, do CSV
```

**Os números precisam bater.** Se não baterem, os suspeitos habituais são:

| Sintoma | Causa provável |
|---------|----------------|
| SQL maior que CSV | JOIN multiplicando linhas (some `frete` depois do join?) |
| SQL menor que CSV | Filtro a mais, ou linhas rejeitadas na migração |
| Diferença de centavos | Arredondamento — aceitável, documente |
| Cidade a mais/menos | Normalização diferente entre os dois caminhos |

**Pronto quando:** os 8 relatórios rodam e o de cidade bate com o M01.

---

## Etapa 6 — Índices (45 min)

Complete `dados/indices.sql`.

Para **cada** índice:

1. Rode `EXPLAIN QUERY PLAN` da consulta relevante **antes**
2. Crie o índice
3. Rode de novo
4. Cole os dois na seção 8 de `docs/MODELAGEM.md`

```bash
sqlite3 dados/atlas.db "EXPLAIN QUERY PLAN SELECT * FROM pedidos WHERE cliente_id = 5;"
```

Procure por: `SCAN` (ruim) → `SEARCH ... USING INDEX` (bom).

**Faça também o teste negativo:** encontre uma consulta em que o índice **não**
é usado (função sobre a coluna, `LIKE '%x'`, aritmética) e registre.

**Pronto quando:** cada índice tem um antes/depois documentado, e você
justificou pelo menos dois índices que decidiu **não** criar.

---

## Etapa 7 — CLI (45 min)

Estenda `src/atlas/cli.py`:

```bash
python main.py schema --recriar
python main.py migrar <csv>
python main.py migrar --pasta dados/brutos/
python main.py status
python main.py relatorio --listar
python main.py relatorio <nome>
python main.py relatorio --todos
python main.py relatorio <nome> --formato json|csv|texto
python main.py verificar          # qualidade dos dados
```

> ⚠️ `schema --recriar` **apaga tudo**. Exija confirmação explícita (`--sim`
> ou uma pergunta interativa). Um comando destrutivo sem trava é um acidente
> esperando acontecer.

**Pronto quando:** todos os comandos funcionam e `--help` explica cada um.

---

## Etapa 8 — Documentação (60 min)

Termine `docs/MODELAGEM.md` e `docs/CSV_VS_SQL.md`.

Para o CSV_VS_SQL, **meça de verdade**:

```python
import time
inicio = time.perf_counter()
# ... roda o relatório ...
print(f"{(time.perf_counter() - inicio) * 1000:.1f} ms")
```

Gere um CSV sintético de 100.000 linhas para a comparação de escala. (Você já
sabe fazer isso — `random` com `seed` fixa, como no M01.)

**Pronto quando:** as tabelas dos dois documentos estão preenchidas com
números, não com adjetivos.

---

## Etapa 9 — Commits e PR (30 min)

Construa o histórico em commits atômicos:

```bash
git add dados/schema.sql docs/MODELAGEM.md
git commit -m "feat(banco): adiciona schema relacional e documentação de modelagem"

git add src/atlas/repositorio.py
git commit -m "feat(repositorio): adiciona camada de acesso a dados"

git add src/atlas/migracao.py
git commit -m "feat(migracao): adiciona carga idempotente de CSV para SQLite"

git add dados/consultas/
git commit -m "feat(consultas): adiciona relatórios em SQL"

git add dados/indices.sql
git commit -m "perf(banco): adiciona índices para as consultas de relatório"

git add src/atlas/relatorios_sql.py src/atlas/cli.py main.py
git commit -m "feat(cli): adiciona comandos de migração e relatório"

git add docs/CSV_VS_SQL.md
git commit -m "docs: compara implementação CSV e SQL com medições"

git push -u origin feature/m03-banco-relacional
```

Abra o PR e faça a **autorrevisão** lendo o diff no GitHub. Você vai achar coisa.

---

## Checklist de entrega

**Modelagem**

- [ ] Diagrama ER desenhado em `docs/MODELAGEM.md`
- [ ] Toda FK com ação referencial escolhida e justificada
- [ ] `CHECK` em todo domínio fechado
- [ ] Respondi por que `itens_pedido.preco_unitario` existe

**Migração**

- [ ] Três execuções seguidas produzem contagens idênticas
- [ ] CSV sujo é processado sem exceção
- [ ] `saida/rejeitados.csv` lista as linhas descartadas com motivo
- [ ] `conferir_com_csv` reporta diferença zero

**Segurança**

- [ ] 🔴 Zero SQL montado por concatenação com dado externo
- [ ] Nome de tabela/relatório validado contra lista branca
- [ ] `grep -n 'f"' src/atlas/repositorio.py` não revela nenhuma consulta

**Consultas**

- [ ] Os 8 relatórios rodam
- [ ] `faturamento_por_cidade` bate exatamente com o M01
- [ ] Consultas usam CTEs, não subconsultas aninhadas de 3 níveis
- [ ] `COUNT(DISTINCT ...)` onde o JOIN multiplicaria

**Desempenho**

- [ ] Cada índice tem `EXPLAIN QUERY PLAN` antes/depois documentado
- [ ] Justifiquei ao menos dois índices que **não** criei

**Documentação**

- [ ] `MODELAGEM.md` completo
- [ ] `CSV_VS_SQL.md` com números medidos, não impressões

---

## Desafios extras

| Desafio | Onde |
|---------|------|
| ⭐ View `vw_vendas` usada por todos os relatórios | `schema.sql` |
| ⭐ Trigger que dá baixa no estoque ao inserir item | `schema.sql` |
| ⭐ Tabela `auditoria` alimentada por trigger em UPDATE/DELETE | `schema.sql` |
| ⭐ Window functions (`ROW_NUMBER`, `LAG`, `SUM OVER`) nas consultas | `consultas/` |
| ⭐⭐ Migrações versionadas (`001_inicial.sql`, `002_devolucoes.sql`) com tabela de controle | novo `migracoes/` |
| ⭐⭐ Tabela `historico_precos` com PK composta, alimentada por trigger | `schema.sql` |
| ⭐⭐ Comando `python main.py sql "<consulta>"` para consulta livre — **com** proteção contra comandos de escrita | `cli.py` |

---

## Tempo total estimado

**8 a 10 horas.** As consultas da Etapa 5 são a parte mais longa e a mais
valiosa — não corra por elas.

---

## ➡️ O que vem depois

No **Módulo 04**, o Atlas ganha orientação a objetos e logging. A dor será:
*"O script virou um monstro de 800 linhas."*

No **Módulo 05**, este mesmo schema migra para PostgreSQL com SQLAlchemy e
Alembic. Anote na seção 13 de `MODELAGEM.md` tudo que você suspeita que vai
precisar mudar — você vai conferir lá.
