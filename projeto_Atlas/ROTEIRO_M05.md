# Roteiro de implementação — Módulo 05 (PostgreSQL e MongoDB)

> **Pré-requisito:** M04 concluído. Você vai comparar a saída da versão nova
> com a do M04 — se aquela não estiver correta, não há referência.

---

## A dor

> *"O SQLite não aguenta mais. Quando o financeiro roda o fechamento e alguém
> tenta gravar um pedido, dá `database is locked`. E o catálogo mudou de novo:
> agora tem cadeira gamer, com altura regulável e peso suportado. Vou criar 40
> colunas nulas?"*

## A entrega

Atlas em **persistência poliglota**: PostgreSQL para o transacional, MongoDB
para o catálogo, SQLAlchemy como ORM e Alembic para as migrações.

---

## 🎯 As duas regras do módulo

> **1. Os números precisam continuar batendo com os do M04.**
>
> **2. Se `servicos.py` e `apresentacao.py` precisarem mudar, o desenho do M04
> estava errado.** Só a camada de persistência deveria ser afetada.

A segunda regra é o teste real. Anote agora, antes de começar, quanto você
**acha** que vai precisar mudar em cada arquivo — e confira no fim.

---

## Etapa 0 — Rede de segurança (30 min)

```bash
git switch -c feature/m05-poliglota

mkdir -p tests/referencia
python main.py relatorio --todos --formato json > tests/referencia/m04_relatorios.json
python main.py status > tests/referencia/m04_status.txt

git add tests/referencia && git commit -m "test: congela a saída do M04"
```

**Pronto quando:** os arquivos de referência estão versionados.

---

## Etapa 1 — Infraestrutura (45 min)

Complete o `docker-compose.yml`:

1. Mova as senhas para o `.env` (use `${VAR:-padrao}`)
2. Adicione os **healthchecks** — sem eles, `up -d` reporta "started" antes de
   o banco aceitar conexão
3. Crie `scripts/subir.sh` e `scripts/derrubar.sh`

```bash
cp .env.example .env       # e edite
docker compose up -d
docker compose ps          # ambos devem estar "healthy"

docker compose exec postgres psql -U atlas -d atlas -c "SELECT version();"
docker compose exec mongo mongosh -u atlas -p atlas --eval "db.adminCommand('ping')"
```

**Sem Docker?** Instale os dois localmente (as instruções estão no notebook
05_01) ou siga com o modo fallback dos notebooks. **Mas o projeto exige os
bancos reais** — é aqui que você aprende a operá-los.

**Pronto quando:** `docker compose ps` mostra ambos saudáveis e você conecta
nos dois pelo terminal.

---

## Etapa 2 — Modelos ORM (90 min)

Complete `src/atlas/orm/modelos.py`.

Ordem: `Cliente` → `Pedido` → `ItemPedido`.

**Traduzindo do M04:**

| M04 | M05 |
|-----|-----|
| `@dataclass(frozen=True, slots=True)` | `class X(Base)` |
| `preco: Decimal` | `mapped_column(Numeric(12, 2))` |
| `status: Status` (Enum) | `String(20)` + `CheckConstraint` |
| `itens: list[ItemVenda]` | `relationship(cascade="all, delete-orphan")` |
| `@property total` | `@property total` (idêntico!) |
| `__post_init__` valida | `CheckConstraint` no banco |

🎯 **A decisão que este arquivo força:** `itens_pedido` não tem FK para
produtos — eles estão no Mongo. Você guarda o `produto_sku` como texto e
**perde a garantia de integridade referencial**. Escreva isso em
`docs/ARQUITETURA_DADOS.md` antes de seguir.

```bash
python src/atlas/orm/modelos.py     # imprime o DDL gerado
```

**Pronto quando:** o DDL sai correto e você consegue justificar cada `cascade`.

---

## Etapa 3 — Sessão e pool (45 min)

Complete `src/atlas/orm/sessao.py`.

1. `url_do_banco()` — 🔴 senha **só** de variável de ambiente
2. `criar_engine()` — com `pool_pre_ping=True`
3. `obter_sessao()` — commit/rollback
4. `verificar_conexao()`
5. `contar_consultas()` — você já escreveu na aula 05_02

**Pronto quando:** `python src/atlas/orm/sessao.py` conecta e reporta o dialeto.

---

## Etapa 4 — Migrações (60 min)

```bash
alembic init migracoes
```

Configure `alembic.ini` (URL) e `env.py` (`target_metadata`).

> ⚠️ **Não fixe a URL no `alembic.ini` versionado.** Leia do ambiente no
> `env.py`:
> ```python
> config.set_main_option("sqlalchemy.url", url_do_banco())
> ```

Crie quatro migrações:

| # | O quê | Aprende |
|---|-------|---------|
| 1 | Schema inicial (autogenerate) | O básico |
| 2 | Adicionar `codigo_ncm` obrigatório | **Padrão de três passos** |
| 3 | Índices de desempenho | Migração de estrutura |
| 4 | Normalizar UFs para maiúsculas | **Migração de dados** |

```bash
alembic upgrade head
alembic downgrade base    # tem que desfazer tudo
alembic upgrade head
```

🔴 **Revise cada migração gerada antes de aplicar.** O autogenerate não
detecta rename — ele gera drop+create e **perde os dados**.

**Pronto quando:** `downgrade base` → `upgrade head` funciona sem erro.

---

## Etapa 5 — Catálogo no MongoDB (90 min)

Complete `src/atlas/mongo/catalogo.py`.

Ordem sugerida:

1. `__init__`, `criar_colecao` (com `$jsonSchema`), `criar_indices`
2. `upsert` e `upsert_muitos`
3. `buscar_por_sku` e **`buscar_muitos_por_sku`** ← o anti-N+1
4. `buscar` com lista branca de filtros
5. Agregações: `facetas`, `inventario_atributos`, `resumo_por_categoria`
6. `verificar_integridade`

🔴 **Duas armadilhas de segurança nesta etapa:**

- **NoSQL injection:** filtro vindo do usuário pode conter `$where`. Valide as
  chaves contra lista branca e rejeite qualquer uma começando com `$`.
- **Race condition no estoque:** `find` → checar → `update` permite estoque
  negativo. Use `$inc` com o filtro `{"estoque": {"$gte": -delta}}`.

**Pronto quando:** você insere um produto de categoria inédita, com specs que
nunca existiram, sem tocar em nada.

---

## Etapa 6 — Migração dos dados (60 min)

`scripts/migrar_para_poliglota.py`:

1. Lê o SQLite do M03/M04
2. Clientes, pedidos e itens → PostgreSQL
3. Produtos → MongoDB
4. Confere as contagens dos dois lados
5. **Idempotente**

```bash
python scripts/migrar_para_poliglota.py
python scripts/migrar_para_poliglota.py   # 2ª vez: nada duplica
python scripts/migrar_para_poliglota.py   # 3ª vez: idem
```

**Pronto quando:** três execuções produzem contagens idênticas.

---

## Etapa 7 — Fachada (60 min)

`src/atlas/repositorio_atlas.py` — a classe que **esconde os dois bancos**.

```python
class RepositorioAtlas:
    def __init__(self, sessao_sql, catalogo_mongo): ...
    def buscar_pedido_completo(self, id: int) -> dict: ...
    def listar_pedidos(self, filtros) -> list[dict]: ...
    def relatorio_por_cidade(self) -> list[dict]: ...
```

🎯 **O teste do desenho:** abra `servicos.py` e `apresentacao.py` do M04.
Quantas linhas precisaram mudar?

- **Zero ou quase:** o desenho estava certo
- **Muitas:** houve vazamento de persistência para a camada de negócio — e é
  ótimo descobrir isso agora

⚠️ **A armadilha desta etapa:** montar um relatório que junta pedidos (SQL) e
produtos (Mongo) sem cuidado gera **N+1 entre bancos** — uma consulta ao Mongo
por item. Use `buscar_muitos_por_sku`.

---

## Etapa 8 — Verificação (45 min)

`scripts/comparar_m04_m05.py`, no mesmo espírito do script do M04.

```bash
python scripts/comparar_m04_m05.py
```

⚠️ **Espere diferenças de centavos.** O M04 usava `float`, o Postgres usa
`NUMERIC`. **Agora o valor correto é o do M05** — documente cada divergência e
diga qual está certa.

Rode também o detector de N+1:

```python
with contar_consultas(engine) as c:
    repositorio.listar_pedidos({"status": "pago"})
assert c.n <= 5, f"N+1: {c.n} consultas"
```

---

## Etapa 9 — Documentação (60 min)

`docs/ARQUITETURA_DADOS.md` — o entregável mais importante do módulo.

| Seção | Pergunta a responder |
|-------|----------------------|
| Decisão | Qual dado vai onde? |
| Alternativas descartadas | Por que não JSONB puro? Por que não Mongo para tudo? |
| Custo operacional | O que passou a ser necessário manter, monitorar e backupear |
| Integridade | Como garantir consistência sem FK entre bancos? |
| Rollback | Como voltar ao SQLite se der errado? |
| Medições | Números do antes e do depois |
| Com equipe menor | O que você faria diferente com 2 pessoas em vez de 10? |

💭 **A última pergunta é a mais honesta.** Persistência poliglota é uma decisão
que custa caro em operação. Se a resposta for *"com 2 pessoas eu usaria só
Postgres com JSONB"*, escreva isso — é uma conclusão legítima e madura.

---

## Checklist de entrega

**Infraestrutura**

- [ ] `docker compose up -d` sobe ambos saudáveis
- [ ] Senhas no `.env`, não no compose nem no código
- [ ] Volumes nomeados; dados sobrevivem ao `down`

**Relacional**

- [ ] Modelos ORM com `Mapped[]` e relacionamentos
- [ ] `Numeric` para todo valor monetário
- [ ] `CheckConstraint` nos domínios fechados
- [ ] `pool_pre_ping=True`
- [ ] 4 migrações, e `downgrade base` funciona

**Documento**

- [ ] Modelagem híbrida (raiz estável + `specs` livre)
- [ ] `$jsonSchema` validando o mínimo
- [ ] Índices justificados, incluindo um composto
- [ ] Upsert idempotente
- [ ] Baixa de estoque atômica

**Integração**

- [ ] Fachada esconde os dois bancos
- [ ] `servicos.py` e `apresentacao.py` praticamente intactos
- [ ] 🔴 **Zero N+1** — inclusive entre bancos
- [ ] `comparar_m04_m05.py` reporta tudo idêntico (ou explicado)

**Segurança**

- [ ] Zero SQL por concatenação
- [ ] Filtros do Mongo validados contra lista branca
- [ ] Nenhuma senha versionada
- [ ] Roles com privilégio mínimo criados

---

## Desafios extras

| Desafio | Onde |
|---------|------|
| ⭐ Coluna JSONB com índice GIN para metadados do pedido | `orm/modelos.py` |
| ⭐ Índice curinga `specs.$**` no Mongo | `mongo/catalogo.py` |
| ⭐ `naming_convention` no metadata (evita ruído no autogenerate) | `orm/modelos.py` |
| ⭐ Log de consultas lentas | `orm/sessao.py` |
| ⭐⭐ Replica set + transação multi-documento | `docker-compose.yml` |
| ⭐⭐ Change Stream sincronizando catálogo → espelho no Postgres | novo módulo |
| ⭐⭐ Escrita dupla para migração sem downtime | `repositorio_atlas.py` |

---

## Tempo total estimado

**10 a 12 horas.** A Etapa 5 (MongoDB) e a Etapa 7 (fachada) são as mais
longas — e a 9 (documentação) é a que mais ensina.

---

## ➡️ O que vem depois

No **Módulo 06**, o Atlas ganha uma API REST com FastAPI. A sessão do
SQLAlchemy vira uma dependência injetada por requisição, e os modelos Pydantic
do M04 viram os schemas de entrada e saída.

Se a fachada desta etapa ficou boa, a API será quase só transporte.
