# Atlas — Sistema Central da Aurora Comércio

> **Módulos 01–04 · Python Fundamental + Git + SQL + Python Avançado**
> Estado atual: sistema orientado a objetos, com modelos tipados, motor de
> regras extensível e logging estruturado, sobre banco relacional SQLite.

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
│   └── REFATORACAO.md           ← M04: decisões de desenho e medições
│
├── scripts/                     ← M02: automações de shell
│   ├── README.md
│   ├── setup.sh    / setup.ps1
│   ├── rodar.sh    / rodar.ps1
│   ├── limpar.sh   / limpar.ps1
│   ├── verificar.sh/ verificar.ps1
│   └── comparar_m03_m04.py      ← M04: prova de equivalência
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
        └── cli.py               ← orquestração e argumentos
```

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
| **M04** | *"O script virou um monstro de 800 linhas"* | **Refatoração para OOP + logging** ← você está aqui |
| M05 | *"SQLite não aguenta; o catálogo muda toda semana"* | PostgreSQL (ORM + Alembic) e MongoDB |
| M06 | *"O time do app precisa acessar os dados"* | API Atlas v1 (FastAPI, JWT, OpenAPI) |
| M07 | *"Precisamos falar com transportadora e gateway"* | Integrações resilientes, Redis, webhooks |
| M08 | *"Configurar a máquina de um dev leva 2 dias"* | Dockerfile + docker-compose |
| M09 | *"Subir versão nova é um ritual de risco"* | CI/CD (GitHub Actions) + proxy reverso |
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
