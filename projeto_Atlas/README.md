# Atlas — Sistema Central da Aurora Comércio

> **Módulos 01–09 · do primeiro script ao sistema em produção**
> Estado atual: sistema orientado a objetos sobre **PostgreSQL** (transacional,
> via SQLAlchemy e Alembic) e **MongoDB** (catálogo), exposto por uma **API
> FastAPI** autenticada, integrado a serviços externos com resiliência e
> coberto por uma **suíte de testes**, empacotado em **containers** e
> publicado por um **pipeline** que testa, audita e reverte sozinho.

---

## Contexto

A **Aurora Comércio** é um e-commerce brasileiro de eletrônicos, sediado em Campinas-SP, que vende para todo o Brasil. A empresa cresce rápido e opera em caos funcional: pedidos em planilhas, relatórios manuais, dados perdidos.

Você é a **primeira pessoa de engenharia** da casa. Não há legado — só dores a resolver.

### A dor do Módulo 01

> *"Ninguém sabe quanto vendemos por cidade. Toda segunda alguém passa a tarde somando planilha à mão e o número nunca bate. Semana passada apresentamos um número errado para o investidor — tinha pedido cancelado no meio."*
> — Diretora Comercial

### A entrega do Módulo 01

Uma CLI em Python puro que lê o CSV de vendas, valida os dados, calcula as métricas e gera relatórios confiáveis em **texto** e **JSON**, além de um arquivo de **rejeições** com tudo que foi descartado e por quê.

**Sem bibliotecas externas.** Só a biblioteca padrão. Pandas vem no Módulo 10 — antes disso você precisa entender o que ele faz por baixo.

### A dor do Módulo 02

> *"Ontem o estagiário salvou por cima do `relatorio_vendas.py`. A gente tinha a versão que funcionava… agora tem `relatorio_final.py`, `relatorio_final_v2.py` e `relatorio_final_AGORA_VAI.py`. Perdemos o dia."*

### A entrega do Módulo 02

O projeto sob controle de versão: histórico limpo com commits atômicos, `.gitignore` que protege segredos e ambientes, `.gitattributes` que resolve o inferno de fins de linha, publicação no GitHub via SSH, e scripts de shell que automatizam setup, execução e limpeza.

Ver **`ROTEIRO_M02.md`** para o passo a passo.

### A dor do Módulo 03

> *"Os dados estão em 14 planilhas diferentes. A do comercial tem 'Campinas', a do financeiro tem 'campinas/SP', a do estoque tem 'CPS'. Quando alguém corrige o preço de um produto, corrige em uma planilha só. Ontem descobrimos que o mesmo cliente aparece 4 vezes com e-mails diferentes."*
> — Diretora de Operações

### A entrega do Módulo 03

O Atlas deixa de ler arquivos planos e passa a operar sobre um **banco relacional**: schema modelado com chaves e constraints, migração idempotente a partir dos CSVs, relatórios escritos em SQL e índices justificados por `EXPLAIN QUERY PLAN`.

**Critério de aceitação:** os números do relatório SQL batem exatamente com os do Módulo 01.

Ver **`ROTEIRO_M03.md`** para o passo a passo.

### A dor do Módulo 04

> *"O script virou um monstro de 800 linhas. Toda vez que preciso adicionar uma métrica nova, copio um bloco de 40 linhas e mudo três palavras. Já tem cinco cópias quase iguais. Ontem corrigi um bug em uma delas e esqueci das outras quatro. E quando roda de madrugada e falha, eu não faço ideia do que aconteceu."*

### A entrega do Módulo 04

O Atlas deixa de ser um script com funções e vira um sistema: modelos tipados com dataclasses, agregação parametrizada (uma dimensão nova = uma property), apresentação por composição, motor de regras que se estende sem editar código existente, e logging estruturado em JSON.

**Critério de aceitação:** a saída dos relatórios é **idêntica** à do Módulo 03. Refatoração que muda comportamento não é refatoração.

Ver **`ROTEIRO_M04.md`** para o passo a passo.

### A dor do Módulo 05

> *"O SQLite não aguenta mais. Quando o financeiro roda o fechamento e alguém tenta gravar um pedido, dá `database is locked`. E o catálogo mudou de novo: agora tem cadeira gamer, com altura regulável e peso suportado. Vou criar 40 colunas nulas?"*

### A entrega do Módulo 05

**Persistência poliglota.** O transacional (clientes, pedidos, itens) vai para o PostgreSQL, com SQLAlchemy como ORM e Alembic para migrações versionadas. O catálogo de produtos — cuja estrutura varia por categoria — vai para o MongoDB.

**Critério de aceitação:** os números continuam idênticos, e `servicos.py` praticamente não muda. Se mudar muito, o desenho do M04 tinha vazamento.

Ver **`ROTEIRO_M05.md`** para o passo a passo e **`docs/ARQUITETURA_DADOS.md`** para as decisões.

### A dor do Módulo 06

> *"O time do app precisa dos dados. Hoje eu exporto um CSV toda manhã e mando por e-mail — e ele já nasce desatualizado. Compras quer registrar entrada de estoque sem me pedir para abrir o banco. A diretoria quer ver margem, e isso não pode aparecer para mais ninguém."*

### A entrega do Módulo 06

**A Atlas API v1.** O sistema deixa de ter um único usuário no terminal e ganha uma porta HTTP: rotas com contrato declarado, validação na fronteira, autenticação por token, autorização por papel e documentação gerada a partir dos próprios tipos.

**Critério de aceitação:** um pedido cujo terceiro item não tem estoque **não altera o estoque dos dois primeiros**. Tudo o mais é boa prática; isto é corretude.

Ver **`ROTEIRO_M06.md`** para o passo a passo e **`docs/API.md`** para a referência e as decisões de projeto.

### A dor do Módulo 07

> *"A transportadora caiu 8 minutos e o nosso checkout caiu junto. Oito minutos sem vender. E o cliente paga o boleto e espera até 5 minutos para o pedido liberar, porque a gente pergunta ao gateway de 5 em 5 minutos. Ah — e precisamos mudar o cálculo de frete, mas ninguém quer mexer."*

### A entrega do Módulo 07

**O Atlas conectado ao mundo, e uma suíte que dá coragem.** Clientes HTTP com timeout, retry e disjuntor; webhooks validados por assinatura; cache com invalidação; e testes que rodam sem tocar a internet.

**Critério de aceitação:** com a transportadora **completamente fora do ar**, o checkout continua funcionando — com frete estimado e aviso honesto. E cada teste da suíte passa também quando rodado sozinho.

Ver **`ROTEIRO_M07.md`** para o passo a passo e **`docs/INTEGRACOES.md`** para as decisões.

### A dor do Módulo 08

> *"Contratamos uma desenvolvedora nova. Ela levou **dois dias** para conseguir rodar o Atlas. Python errado, PostgreSQL de outra versão, o Mongo não subia no Windows, e uma variável de ambiente que ninguém lembrava de documentar."*

### A entrega do Módulo 08

**O Atlas containerizado.** Imagem multi-stage rodando como usuário sem privilégio, `docker-compose` com os quatro serviços, healthchecks que substituem o `sleep 10`, e uma auditoria automática de Dockerfile e compose.

**Critério de aceitação:** `git clone`, `cp .env.example .env`, `docker compose up -d`. Dois comandos e um arquivo, em qualquer sistema operacional.

Ver **`ROTEIRO_M08.md`** para o passo a passo e **`docs/CONTAINERS.md`** para as decisões.

### A dor do Módulo 09

> *"Subir versão nova é um ritual. A gente marca para sexta à noite, três pessoas ficam de plantão, e uma vez em cada três dá errado. E a gente descobre que o site caiu quando um cliente liga."*

### A entrega do Módulo 09

**O Atlas em produção, sozinho.** Servidor com proxy reverso e HTTPS, deploy por symlink atômico com rollback em um comando, pipeline que testa e audita a cada push, e monitoramento que avisa antes do cliente.

**Critério de aceitação:** um deploy ruim é revertido **automaticamente** em menos de 60 segundos — e cada portão do CI reprova quando você o quebra de propósito.

Ver **`ROTEIRO_M09.md`**, **`docs/DEPLOY.md`** e **`docs/RUNBOOK.md`**.

> 🎯 **A boa notícia:** seis dos oito requisitos para containerizar já estavam prontos — configuração por ambiente (M06), rota de saúde (M06), API sem estado (M06), dependências declaradas (M04), log estruturado (M04), segredos fora do código (M06). Você não os fez pensando em Docker; fez porque eram boas práticas.
>
> **Containerizar não é adaptar a aplicação ao Docker. É descobrir que uma aplicação bem construída já é containerizável.**

---

## 1. Preparando o ambiente

### 1.1 Instalar o Python

Você precisa do **Python 3.10 ou superior** (usamos `match/case` e a sintaxe `int | None`).

| Sistema | Como instalar |
|---------|---------------|
| **Windows** | Baixe em [python.org/downloads](https://www.python.org/downloads/). ⚠️ Marque **"Add Python to PATH"** na primeira tela do instalador. |
| **macOS** | `brew install python@3.12` (ou baixe de python.org) |
| **Linux (Debian/Ubuntu)** | `sudo apt update && sudo apt install python3 python3-venv python3-pip` |

Confirme a instalação:

```bash
python --version        # Windows
python3 --version       # macOS / Linux
```

Deve aparecer `Python 3.10.x` ou superior. Se aparecer `3.9` ou "comando não encontrado", resolva isso antes de continuar.

> 💡 **Nota sobre `python` vs `python3`:** no Windows o comando é `python`. No macOS/Linux costuma ser `python3`. Neste README usamos `python` — adapte se necessário.

### 1.2 Instalar o VS Code e as extensões

1. Baixe o VS Code em [code.visualstudio.com](https://code.visualstudio.com/).
2. Abra a aba de extensões (`Ctrl+Shift+X`) e instale:
   - **Python** (Microsoft) — obrigatória
   - **Pylance** (Microsoft) — vem junto com a Python; dá autocompletar e checagem de tipos
   - **Jupyter** (Microsoft) — para os notebooks do manual de estudos
   - **Ruff** (Astral) — linter rápido, opcional mas recomendado

### 1.3 Criar o ambiente virtual (venv)

Um **ambiente virtual** é uma pasta isolada com sua própria cópia do Python e suas próprias dependências. Isso evita que o projeto A quebre quando você instala algo para o projeto B.

**Sempre crie um venv por projeto. Sem exceção.**

Na raiz de `projeto_Atlas/`:

```bash
# criar
python -m venv .venv

# ativar — Windows (PowerShell)
.venv\Scripts\Activate.ps1

# ativar — Windows (CMD)
.venv\Scripts\activate.bat

# ativar — macOS / Linux
source .venv/bin/activate
```

Quando ativado, o prompt ganha o prefixo `(.venv)`:

```
(.venv) C:\...\projeto_Atlas>
```

Para desativar: `deactivate`.

> ⚠️ **Erro comum no Windows:** se o PowerShell recusar o script com *"execução de scripts foi desabilitada"*, rode uma vez:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 1.4 Selecionar o interpretador no VS Code

1. `Ctrl+Shift+P` → **Python: Select Interpreter**
2. Escolha o que tem `.venv` no caminho.

Sem isso o VS Code usa o Python global e você verá imports "não encontrados" mesmo com tudo instalado.

### 1.5 Dependências

A partir do **Módulo 04**, o projeto usa `pyproject.toml` (padrão PEP 621) em vez de `requirements.txt`:

```bash
pip install -e ".[dev]"
```

O `-e` faz uma **instalação editável**: cria um link para o código-fonte em vez de copiá-lo. Você edita o arquivo e a mudança vale na hora, sem reinstalar. É como se desenvolve um pacote Python.

Depois disso:

- `import atlas` funciona de qualquer pasta
- o `sys.path.insert` do `main.py` vira desnecessário
- se você configurou `[project.scripts]`, o comando `atlas` fica disponível no terminal

**Nos Módulos 01–03** não havia dependências externas — só a biblioteca padrão. **No M04** entra o `pydantic`, para validação na fronteira.

> 💡 O `requirements.txt` continua no repositório porque você ainda vai encontrá-lo em projetos legados e em Dockerfiles (Módulo 08). Mas o padrão moderno é o `pyproject.toml`.

---

## 2. Estrutura do projeto

```
projeto_Atlas/
├── README.md                    ← você está aqui
├── ROTEIRO_M01.md               ← implementação do M01 (Python)
├── ROTEIRO_M02.md               ← implementação do M02 (Git)
├── ROTEIRO_M03.md               ← implementação do M03 (SQL)
├── ROTEIRO_M04.md               ← implementação do M04 (OOP)
├── ROTEIRO_M05.md               ← implementação do M05 (Postgres + Mongo)
├── ROTEIRO_M06.md               ← implementação do M06 (API)
├── ROTEIRO_M07.md               ← implementação do M07 (integrações + testes)
├── ROTEIRO_M08.md               ← implementação do M08 (containers)
├── ROTEIRO_M09.md               ← implementação do M09 (deploy e CI/CD)
├── .github/workflows/           ← M09: ci.yml e cd.yml
├── infra/                       ← M09: systemd e nginx
├── Dockerfile                   ← M08: imagem multi-stage
├── .dockerignore                ← M08: 🔴 primeira linha é .env
├── docker-compose.override.yml  ← M08: sobreposição de desenvolvimento
├── docker-compose.yml           ← M05: sobe os dois bancos
├── pyproject.toml               ← M04: metadados, deps e config das ferramentas
├── requirements.txt             ← legado; o pyproject é o padrão agora
├── main.py                      ← ponto de entrada da CLI
│
├── .gitignore                   ← M02: o que NÃO versionar
├── .gitattributes               ← M02: normalização de fins de linha
├── .env.example                 ← M02: documenta as variáveis (sem valores)
│
├── docs/
│   ├── RECUPERACAO.md           ← M02: seu manual de emergência do Git
│   ├── MODELAGEM.md             ← M03: diagrama ER e decisões de modelagem
│   ├── CSV_VS_SQL.md            ← M03: comparação medida entre as duas versões
│   ├── REFATORACAO.md           ← M04: decisões de desenho e medições
│   ├── ARQUITETURA_DADOS.md     ← M05: por que dois bancos, e o custo disso
│   ├── API.md                   ← M06: referência da API e decisões de projeto
│   ├── INTEGRACOES.md           ← M07: resiliência, webhooks, cache, testes
│   ├── CONTAINERS.md            ← M08: imagem, volumes, healthchecks
│   ├── DEPLOY.md                ← M09: como publicar, e as decisões
│   └── RUNBOOK.md               ← M09: 🔴 o que fazer quando quebrar
│
├── scripts/                     ← M02: automações de shell
│   ├── README.md
│   ├── setup.sh    / setup.ps1
│   ├── rodar.sh    / rodar.ps1
│   ├── limpar.sh   / limpar.ps1
│   ├── verificar.sh/ verificar.ps1
│   ├── comparar_m03_m04.py      ← M04: prova de equivalência
│   ├── migrar_para_poliglota.py ← M05: SQLite → Postgres + Mongo
│   ├── subir.sh                 ← M05: sobe a infraestrutura
│   ├── derrubar.sh
│   ├── api.sh      / api.ps1    ← M06: sobe a API em modo desenvolvimento
│   ├── entrada.sh               ← M08: entrypoint do container
│   ├── auditar_containers.py    ← M08: o portão de CI
│   ├── deploy.sh                ← M09: com verificação e rollback
│   └── rollback.sh              ← M09: 🔴 um comando
│
├── dados/
│   ├── brutos/
│   │   ├── vendas_jul2026.csv   ← dados limpos
│   │   └── vendas_sujas.csv     ← dados com problemas propositais
│   ├── processados/
│   ├── schema.sql               ← M03: DDL do modelo relacional
│   ├── indices.sql              ← M03: índices, cada um justificado
│   ├── consultas/               ← M03: um .sql por relatório
│   │   ├── faturamento_por_cidade.sql
│   │   ├── faturamento_por_categoria.sql
│   │   ├── top_produtos.sql
│   │   ├── top_clientes.sql
│   │   ├── evolucao_mensal.sql
│   │   ├── curva_abc.sql
│   │   ├── alerta_estoque.sql
│   │   └── qualidade_dados.sql
│   └── atlas.db                 ← M03: o banco (ignorado pelo Git)
│
├── saida/                       ← relatórios gerados (ignorado pelo Git)
│
└── src/
    └── atlas/
        ├── __init__.py
        ├── config.py            ← constantes e caminhos
        ├── excecoes.py          ← exceções de domínio
        ├── leitura.py           ← ler CSV do disco
        ├── validacao.py         ← validar e normalizar linhas
        ├── metricas.py          ← agregações em Python (M01)
        ├── formatacao.py        ← formatar valores para exibição
        ├── relatorios.py        ← renderizar txt / json / csv
        ├── repositorio.py       ← M03: TODO o SQL do sistema
        ├── migracao.py          ← M03: CSV → banco, idempotente
        ├── relatorios_sql.py    ← M03: executa os .sql e formata
        ├── modelos.py           ← M04: dataclasses do domínio
        ├── servicos.py          ← M04: Agregador, ServicoRelatorio
        ├── apresentacao.py      ← M04: formatadores × destinos
        ├── regras.py            ← M04: motor de precificação
        ├── observabilidade.py   ← M04: logging e instrumentação
        ├── cli.py               ← orquestração e argumentos
        │
        ├── orm/                 ← M05: persistência relacional
        │   ├── modelos.py       ←   modelos SQLAlchemy 2.0
        │   └── sessao.py        ←   engine, pool e ciclo da sessão
        ├── mongo/               ← M05: persistência de documentos
        │   └── catalogo.py      ←   repositório do catálogo
        │
        ├── api/                 ← M06: a porta HTTP do sistema
        │   ├── aplicacao.py     ←   monta o FastAPI (fábrica criar_app)
        │   ├── config.py        ←   configuração de INFRA, via ambiente
        │   ├── seguranca.py     ←   hash de senha e token
        │   ├── dependencias.py  ←   sessão, paginação, ordenação, papéis
        │   ├── esquemas.py      ←   contratos Pydantic (rede)
        │   └── rotas/
        │       ├── autenticacao.py
        │       ├── produtos.py
        │       ├── pedidos.py
        │       ├── relatorios.py
        │       └── webhooks.py  ←   M07: recepção validada
        │
        └── integracoes/         ← M07: o mundo lá fora
            ├── cliente_http.py  ←   base: timeout, retry, disjuntor
            ├── transportadora.py ←  Veloz: cotação e rastreio
            ├── gateway.py       ←   pagamento e validação de webhook
            └── cache.py         ←   cache-aside sobre Redis

tests/                           ← M07: a suíte que dá coragem
├── conftest.py                  ←   fixtures (banco isolado, cliente)
├── test_seguranca.py            ←   🔒 vazamento, autorização, injeção
└── test_integracoes.py          ←   com respx: sem tocar a internet
```

> 🎯 **`api/` vs `integracoes/` — a direção da seta.**
>
> | | `api/` | `integracoes/` |
> |---|--------|----------------|
> | Papel | você é o **servidor** | você é o **cliente** |
> | Contrato | você define | você obedece |
> | Falha | você escolhe quando | você sofre a dos outros |
>
> É a mudança de mentalidade do M07: como servidor você controla tudo;
> como cliente você não controla **nada** — nem a disponibilidade, nem a
> latência, nem o formato que o parceiro vai mudar sem avisar.

> 🎯 **`orm/modelos.py` vs `api/esquemas.py` — a distinção que mais confunde.**
>
> | | `orm/modelos.py` | `api/esquemas.py` |
> |---|---|---|
> | Biblioteca | SQLAlchemy | Pydantic |
> | Representa | Linha da tabela | Corpo da requisição/resposta |
> | Vive em | Disco | Rede |
> | Quem valida | O banco | A API |
>
> São **coisas diferentes** que por acaso têm campos parecidos. Tentar usar
> um no lugar do outro é exatamente como o `custo` de um produto acaba
> visível para o marketplace concorrente.

> 💭 **E `atlas/config.py` vs `atlas/api/config.py`?** O primeiro guarda
> constantes de **domínio** (cortes da curva ABC, formato de data) — iguais
> em qualquer máquina. O segundo guarda **infraestrutura** (URL do banco,
> chave secreta, CORS) — muda entre dev, homologação e produção, e parte
> é segredo. Misturar os dois é como senha de banco vai parar no Git.

> 💡 **Por que `metricas.py` (M01) e `repositorio.py` (M03) coexistem?**
> Porque o M03 pede que você **compare** as duas implementações (ver
> `docs/CSV_VS_SQL.md`). A partir do M04, a versão em Python vira material de
> referência — a produção usa o banco.

### Por que essa separação?

Cada módulo tem **uma responsabilidade**. Isso importa por três razões práticas:

1. **Você sabe onde mexer.** Regra de frete mudou? `metricas.py`. Formato do relatório mudou? `relatorios.py`.
2. **Você consegue testar.** No M12 vamos escrever testes — funções puras e isoladas são triviais de testar; um script de 800 linhas não é.
3. **Você consegue trocar peças.** No M03 a leitura vira SQL. Só `leitura.py` muda.

> 📌 O padrão `src/` (código dentro de uma pasta `src`, não na raiz) evita que Python importe acidentalmente o pacote local em vez do instalado. É a convenção recomendada pela comunidade — aprofundamos no M04.

---

## 3. Como executar

### Pela primeira vez (do zero)

```bash
git clone git@github.com:seu-usuario/atlas.git
cd atlas
./scripts/setup.sh          # Linux/macOS
.\scripts\setup.ps1         # Windows
```

### No dia a dia

```bash
./scripts/rodar.sh                                  # CSV padrão
./scripts/rodar.sh dados/brutos/vendas_sujas.csv    # CSV específico
./scripts/verificar.sh                              # roda contra os dois CSVs
./scripts/limpar.sh                                 # apaga o que foi gerado
```

### Trabalhando com o banco (M03)

```bash
python main.py schema --recriar                     # ⚠️ apaga e recria o banco
python main.py migrar dados/brutos/vendas_jul2026.csv
python main.py status                               # contagem das tabelas
python main.py relatorio --listar
python main.py relatorio faturamento_por_cidade
python main.py relatorio --todos --formato json
python main.py verificar                            # qualidade dos dados
```

Inspecionando o banco direto:

```bash
sqlite3 dados/atlas.db "SELECT type, name FROM sqlite_master ORDER BY type, name;"
sqlite3 dados/atlas.db "PRAGMA foreign_key_check;"
sqlite3 dados/atlas.db "EXPLAIN QUERY PLAN SELECT * FROM pedidos WHERE status='pago';"
```

> 💡 Para explorar visualmente, instale o [DB Browser for SQLite](https://sqlitebrowser.org/)
> ou a extensão *SQLite Viewer* no VS Code. Poder clicar nas tabelas acelera
> muito a depuração de consultas.

### Subindo os bancos (M05)

```bash
cp .env.example .env               # e revise as senhas
docker compose up -d               # PostgreSQL + MongoDB
docker compose ps                  # ambos devem estar "healthy"

alembic upgrade head               # aplica as migrações
python scripts/migrar_para_poliglota.py

# Inspecionando
docker compose exec postgres psql -U atlas -d atlas
docker compose exec mongo mongosh -u atlas -p atlas
```

Ou pelos scripts: `./scripts/subir.sh` e `./scripts/derrubar.sh`.

> 💡 **Sem Docker?** Os notebooks do M05 rodam em modo fallback (SQLite +
> mongomock) e ensinam quase tudo. Mas o **projeto** exige os bancos reais —
> é aqui que você aprende a operá-los.

### Subindo a API (M06)

```bash
# 1. dependências
pip install "fastapi[standard]" pydantic-settings pyjwt bcrypt python-multipart

# 2. configuração — 🔴 gere a SUA chave
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(48))"
#    cole o resultado em ATLAS_SECRET_KEY dentro do .env

# 3. confirme que o .env não vai para o Git
git check-ignore -v .env        # se não imprimir nada, PARE e conserte

# 4. suba
./scripts/api.sh                # ou: .\scripts\api.ps1
```

Depois abra **http://127.0.0.1:8000/docs**.

Manualmente, sem o script:

```bash
uvicorn "atlas.api.aplicacao:criar_app" --factory --reload
```

Testando pelo terminal:

```bash
# login (form-data, exigência do OAuth2 — não é JSON)
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/token \
  -d "username=ana@aurora.com.br&password=SUA_SENHA" | jq -r .access_token)

curl http://127.0.0.1:8000/produtos -H "Authorization: Bearer $TOKEN"
curl http://127.0.0.1:8000/saude
```

> 🔴 **`--reload` é só para desenvolvimento.** Ele vigia o sistema de
> arquivos e reinicia o processo a cada salvamento. O modo de produção
> (workers, proxy reverso, HTTPS) é assunto do M09.

> ⚠️ **Se o login devolver 500 com erro sobre `python-multipart`:** o
> `OAuth2PasswordRequestForm` lê `form-data`, e isso exige esse pacote.
> É a primeira pedra do caminho, e quase todo mundo tropeça nela.

### Rodando os testes (M07)

```bash
pip install pytest pytest-cov respx fakeredis

pytest                             # tudo
pytest -m "not lento"              # o que roda em segundos
pytest -m seguranca                # 🔒 só as verificações de segurança
pytest -k "frete and not api"      # por nome
pytest --lf                        # só o que falhou da última vez
pytest -x                          # para na primeira falha
pytest --cov=atlas --cov-report=term-missing
```

🔴 **A verificação que quase ninguém faz** — cada teste passa **sozinho**?

```bash
pytest --collect-only -q | grep :: | while read t; do
  pytest -q --tb=no "$t" >/dev/null || echo "🔴 só passa acompanhado: $t"
done
```

> Rodar a suíte duas vezes **não** detecta dependência de ordem: um estado
> guardado num módulo Python é recriado a cada processo. O que denuncia é
> rodar cada teste isolado. Um teste que só passa acompanhado é o que vai
> deixar o CI vermelho um dia, sem ninguém ter mexido em nada relacionado.

### Cache e integrações (M07)

```bash
# Redis (opcional — sem ele, os testes usam fakeredis)
docker compose up -d redis
docker compose exec redis redis-cli ping        # → PONG

# auditoria rápida do próprio código
grep -rn "httpx.Client(" src/ | grep -v timeout   # 🔴 deve sair VAZIO
grep -rnE '(secret|senha|password|token|api_key)\s*=\s*["'"'"'][^"'"'"']{8,}' src/
```

> 🔴 **O primeiro `grep` é o mais importante do módulo.** Um `httpx.Client`
> sem timeout espera para sempre — e uma requisição pendurada é um worker
> perdido. Com 4 workers, bastam 4 para a API inteira parar de responder,
> sem registrar um único erro: nada falhou, só nunca terminou.

### Qualidade de código (M04)

```bash
mypy src/                          # verificação estática de tipos
ruff check src/                    # linter
ruff check --fix src/              # corrige o que dá para corrigir sozinho
ruff format src/                   # formatador

python scripts/comparar_m03_m04.py # prova que a refatoração não mudou nada
```

### Observabilidade (M04)

```bash
python main.py relatorio --todos --verbose    # console em DEBUG
cat saida/atlas.jsonl | tail -20              # log estruturado
python -c "from atlas.observabilidade import Monitor; print(Monitor.analisar_historico())"
```

> 💭 O `saida/atlas.jsonl` é o que responde *"o que aconteceu na execução
> de madrugada?"*. Cada linha é um JSON com timestamp UTC, etapa, duração
> e métricas.

### Direto pelo Python

Com o venv ativado, na raiz do projeto:

```bash
# Relatório com os dados limpos
python main.py dados/brutos/vendas_jul2026.csv

# Relatório com os dados sujos (deve funcionar sem quebrar!)
python main.py dados/brutos/vendas_sujas.csv

# Sem argumento — usa o caminho padrão de config.py
python main.py
```

Saídas geradas em `saida/`:

| Arquivo | Conteúdo |
|---------|----------|
| `relatorio.txt` | Relatório formatado para leitura humana |
| `relatorio.json` | Mesma informação, estruturada para outro sistema consumir |
| `rejeitados.csv` | Linhas descartadas, com número da linha e motivo |

---

## 4. O que você precisa implementar

Todos os arquivos em `src/atlas/` estão como **esqueleto**: assinaturas de função, docstrings e comentários `# TODO:` descrevendo o que fazer. Nenhum contém a solução.

Siga a ordem sugerida em **`ROTEIRO_M01.md`**.

### Critérios de pronto

- [ ] `python main.py dados/brutos/vendas_jul2026.csv` gera os 3 arquivos em `saida/`
- [ ] `python main.py dados/brutos/vendas_sujas.csv` **não quebra** e lista as rejeições
- [ ] `python main.py caminho/que/nao/existe.csv` mostra mensagem amigável, sem traceback
- [ ] Nenhuma função passa de ~25 linhas
- [ ] Toda função pública tem docstring e type hints
- [ ] Nenhum `except: pass` no código
- [ ] Nenhuma variável `global` (constantes em `MAIÚSCULAS` não contam)

---

## 5. Dicionário de dados

Arquivo: `dados/brutos/vendas_*.csv`, separador `,`, encoding `utf-8`.

| Coluna | Tipo | Regra de validação |
|--------|------|--------------------|
| `id` | inteiro | Obrigatório, único |
| `data` | texto | Formato `AAAA-MM-DD` |
| `cliente` | texto | Não vazio; normalizar com `.title()` |
| `cidade` | texto | Não vazio; normalizar com `.title()` |
| `uf` | texto | Exatamente 2 letras maiúsculas |
| `categoria` | texto | Não vazio |
| `produto` | texto | Não vazio |
| `quantidade` | inteiro | Maior que zero |
| `preco_unitario` | decimal | Maior ou igual a zero |
| `status` | texto | Um de: `pago`, `pendente`, `cancelado` |
| `canal` | texto | Um de: `site`, `app`, `marketplace` |

**Regra de negócio central:** métricas de faturamento consideram **apenas** pedidos com status `pago`.

---

## 6. Glossário de métricas

| Métrica | Definição |
|---------|-----------|
| **Faturamento** | Σ (`quantidade` × `preco_unitario`) dos pedidos pagos |
| **Ticket médio** | Faturamento ÷ número de pedidos pagos |
| **Share** | Faturamento do grupo ÷ faturamento total |
| **Taxa de cancelamento** | Pedidos cancelados ÷ total de pedidos |
| **Curva ABC** | A = primeiros 80% do faturamento acumulado; B = 80–95%; C = 95–100% |

---

## 7. Roteiro do Atlas (visão geral)

Onde este módulo se encaixa na jornada completa:

| Módulo | Dor da Aurora | Entrega |
|--------|---------------|---------|
| ✅ M01 | *"Ninguém sabe quanto vendemos por cidade"* | Scripts CLI de relatórios sobre CSV |
| ✅ M02 | *"Perdemos uma versão do script ontem"* | Git, `.gitignore`, automações shell |
| ✅ M03 | *"Os dados estão em 14 planilhas"* | Schema relacional (`.sql`) + carga |
| ✅ M04 | *"O script virou um monstro de 800 linhas"* | Refatoração para OOP + logging |
| ✅ M05 | *"SQLite não aguenta; o catálogo muda toda semana"* | PostgreSQL (ORM + Alembic) e MongoDB |
| ✅ M06 | *"O time do app precisa acessar os dados"* | API Atlas v1 (FastAPI, JWT, OpenAPI) |
| ✅ M07 | *"Precisamos falar com transportadora e gateway"* | Integrações resilientes, Redis, webhooks, testes |
| ✅ M08 | *"Configurar a máquina de um dev leva 2 dias"* | Dockerfile + docker-compose + auditoria |
| **M09** | *"Subir versão nova é um ritual de risco"* | **CI/CD + proxy reverso + monitoramento** ← você está aqui |
| M10 | *"Decidimos com dados de 3 semanas atrás"* | ETL diário + orquestração |
| M11 | *"Ninguém sabe por que o sistema é assim"* | ADRs e separação de camadas |
| M12 | *"Temos medo de mexer no código"* | Suíte de testes (pytest) no CI |
| M13 | — | **Atlas 1.0** consolidado |

---

## 8. Solução de problemas

| Sintoma | Causa provável | Solução |
|---------|----------------|---------|
| `ModuleNotFoundError: No module named 'atlas'` | Rodando de outra pasta, ou `src` fora do path | Execute sempre da raiz: `python main.py`. Veja o ajuste de `sys.path` em `main.py`. |
| Acentos viram `Ã§Ã£o` | Encoding não informado | Sempre `open(..., encoding="utf-8")` |
| Linhas em branco no CSV gerado (Windows) | Falta `newline=""` | `open(caminho, "w", newline="", encoding="utf-8")` |
| VS Code marca import como não resolvido | Interpretador errado | `Ctrl+Shift+P` → Python: Select Interpreter → escolha o `.venv` |
| `Activate.ps1 não pode ser carregado` | Política de execução do PowerShell | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| Números de faturamento não batem | Provavelmente contando cancelados | Filtre por `status == "pago"` |
| `ValueError: mutable default` na dataclass | Lista/dict como valor padrão | `field(default_factory=list)` |
| `FrozenInstanceError` no `__post_init__` | Tentando atribuir em dataclass `frozen` | `object.__setattr__(self, "campo", valor)` |
| Log aparece duplicado | `configurar_logging` chamado duas vezes | `logger.handlers.clear()` e `propagate = False` |
| `AttributeError` ao agregar | Dimensão inexistente em `getattr` | Valide a dimensão na entrada de `por()` |
| Tabela desalinhada | Emoji na célula (`len` 1, largura 2) | Use marcadores ASCII |
| `ModuleNotFoundError: atlas` após o M04 | Pacote não instalado | `pip install -e .` |
| `connection refused` na porta 5432 | Container não subiu | `docker compose ps` e `logs postgres` |
| `port is already allocated` | Já há um Postgres local | Troque para `5433:5432` no compose |
| `MappedAnnotationError` | Modelo definido em notebook | Modelos ORM precisam estar em **módulo** |
| `DetachedInstanceError` | Objeto usado após a sessão fechar | Eager loading, ou converta para dict antes |
| Listagem lenta e muitas consultas | **N+1** | `selectinload` nas relações |
| `alembic` não detecta nada | Faltou `target_metadata` no `env.py` | Aponte para `Base.metadata` |
| Migração apagou uma coluna renomeada | Autogenerate não detecta rename | **Sempre revise antes de aplicar** |
| Pedido referencia produto inexistente | Não há FK entre os bancos | Rode a reconciliação (`verificar_integridade`) |
| `git status` mostra `.venv/` | `.gitignore` ausente ou o venv já foi commitado | `git rm -r --cached .venv` |
| Diff mostra o arquivo inteiro alterado | Fim de linha (CRLF vs LF) | O `.gitattributes` resolve; renormalize com `git add --renormalize .` |
| `Permission denied` ao rodar `./scripts/setup.sh` | Falta bit de execução | `chmod +x scripts/*.sh` |
| `Activate.ps1 não pode ser carregado` | Política do PowerShell | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |
| `git push` rejeitado | Remoto está à frente | `git pull` e depois `git push` — **nunca** `--force` |
| FK aceita valor inexistente | `PRAGMA foreign_keys` desligado | Execute em **toda** conexão nova — o SQLite não persiste esse PRAGMA |
| `database is locked` | Outro processo escrevendo (ou o DB Browser aberto) | Feche o cliente visual; ligue o modo WAL |
| Faturamento SQL maior que o do M01 | `JOIN` multiplicando linhas | `COUNT(DISTINCT p.id)`; não some `frete` depois do join com itens |
| `LEFT JOIN` trazendo menos linhas que o esperado | Condição da tabela da direita no `WHERE` | Mova a condição para o `ON` |
| Migração duplicou dados | Faltou `ON CONFLICT` | Toda escrita da carga precisa ser UPSERT |
| Texto com acento corrompido no `.db` | Encoding na leitura do CSV | `open(..., encoding="utf-8")` |
| **M06** — `Form data requires "python-multipart"` | `OAuth2PasswordRequestForm` lê form-data | `pip install python-multipart` |
| `GET /produtos/destaques` devolve 404 | Rota dinâmica declarada antes da estática | Declare `/produtos/destaques` **antes** de `/produtos/{sku}` |
| `PATCH` apaga campos não enviados | Faltou `exclude_unset` | `dados.model_dump(exclude_unset=True)` |
| `custo` aparece na resposta | Rota sem `response_model` | Toda rota que devolve dado declara o esquema de saída |
| Validador de `sku` "não roda" | Restrição do `Field` roda antes | `@field_validator("sku", mode="before")` |
| `QueuePool limit of size N reached` | `get_sessao` sem `finally: close()` | 🔴 `try: yield / finally: sessao.close()` |
| `no such table` só nos testes | SQLite `:memory:` é por conexão | `poolclass=StaticPool` no engine de teste |
| Front vê "blocked by CORS policy" num erro 500 | CORS não é o middleware mais externo | Adicione o `CORSMiddleware` **primeiro** |
| Login diferencia usuário de senha errada | Mensagens distintas | 🔴 Levante o **mesmo** objeto de exceção nos dois casos |
| Token continua válido após demissão | Só a assinatura foi verificada | Consulte o usuário no banco em `usuario_atual` |
| Estoque some sem erro nenhum | Falta `rollback` no caminho de erro | Valide **tudo** antes de alterar **qualquer** coisa |
| `alg: none` aceito no JWT | `decode` sem `algorithms=` | Passe `algorithms=["HS256"]` explicitamente |
| Aplicação sobe com chave secreta vazia | Sem validação na `Config` | `Field(min_length=32)` e sem default utilizável |
| **M07** — API trava sem erro nenhum | `httpx.Client` sem `timeout` | 🔴 timeout explícito em **todo** cliente |
| Requisições acumulam até a API parar | Serviço externo lento, não fora do ar | `connect` curto + `read` com teto |
| Cobrança duplicada | `POST` repetido sem `Idempotency-Key` | Só repita `POST` com chave |
| A chave de idempotência não protege | Gerada a cada tentativa | Uma chave por **operação**, reusada nas tentativas |
| Assinatura do webhook nunca bate | Corpo reserializado | `await requisicao.body()` — bytes **crus** |
| O gateway reenvia para sempre | Você respondeu erro ao evento repetido | Responda `2xx`: "já recebi" é sucesso |
| Evento processado várias vezes | Idempotência em `set` de memória | Redis (`SET NX EX`) ou tabela com `UNIQUE` |
| Sincronização duplica registros | Paginação por offset em lista viva | Use cursor para sincronizar dados |
| Laço infinito na madrugada | Paginação sem teto de páginas | `teto_paginas` + detecção de repetição |
| Banco cai no horário de pico | Estouro de cache | Trava distribuída + TTL com jitter |
| Dado velho servido para sempre | Só invalidação, sem TTL | Use os **dois** |
| Executável aceito como CSV | Confiou na extensão/`Content-Type` | Valide **magic bytes** |
| `no such table` só nos testes | SQLite `:memory:` sem `StaticPool` | `poolclass=StaticPool` |
| Teste passa junto e falha sozinho | Estado vazando entre testes | Banco recriado por teste; escopo `function` |
| Marcador ignorado em silêncio | Erro de digitação sem `--strict-markers` | Ative `--strict-markers` |
| 100% de cobertura e bugs em produção | Testes que executam sem verificar | Cobertura mede linhas, não comportamento |

---

## 7b. Fluxo de trabalho com Git

Este projeto segue o **GitHub Flow**:

```bash
git switch main && git pull              # partir sempre do main atualizado
git switch -c feature/nome-descritivo    # branch por mudança
# ... trabalha, commita ...
git push -u origin feature/nome-descritivo
# abre o Pull Request no GitHub
# revisão → merge → limpeza:
git switch main && git pull
git branch -d feature/nome-descritivo
```

**Regra número 1: nunca commite direto em `main`.**

### Padrão de mensagens (Conventional Commits)

```
<tipo>(<escopo>): <descrição no imperativo>
```

| Tipo | Quando |
|------|--------|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Só documentação |
| `refactor` | Reestrutura sem mudar comportamento |
| `test` | Testes |
| `chore` | Build, dependências, configuração |

Exemplo: `feat(metricas): adiciona curva ABC de praças`

### Padrão de branches

```
feature/relatorio-por-canal
fix/calculo-frete-negativo
hotfix/erro-producao
chore/atualiza-dependencias
docs/readme-instalacao
```

### Deu ruim?

Consulte **`docs/RECUPERACAO.md`** — seu manual de emergência.

---

## 9. Convenções de código

Seguimos a [PEP 8](https://peps.python.org/pep-0008/):

- `snake_case` para funções e variáveis
- `MAIUSCULAS_COM_UNDERSCORE` para constantes
- `PascalCase` para classes (aparecem no M04)
- 4 espaços de indentação, nunca tab
- Linhas de até ~100 caracteres
- Imports agrupados: padrão → terceiros → locais
- Docstring em toda função pública
- Type hints em toda assinatura

---

*Atlas · Aurora Comércio · Módulo 01*
