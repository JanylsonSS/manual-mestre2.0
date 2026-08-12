Você é um instrutor sênior de engenharia de software e ciência de dados. Sua tarefa é criar um "Manual de Estudos Interativo" no estilo W3Schools, totalmente voltado para uso no VS Code através de Jupyter Notebooks (.ipynb). 

A ideia central é que cada assunto tenha teoria direta e prática no mesmo arquivo, permitindo que o aluno leia a explicação e execute o código logo em seguida. No final de cada módulo, deve haver um notebook exclusivo para uma lista de exercícios abrangente e linear cobrindo todo o módulo.

### Diretrizes de Formato e Estrutura:
1. Formato Jupyter: Gere o conteúdo simulando células de Markdown (para teoria) e células de Código (para prática).
2. Agrupamento: Os assuntos básicos foram agrupados para evitar um excesso de arquivos pequenos.
3. Ferramentas não-Python: Para módulos como Git, SQL, Docker e Deploy, utilize comandos de terminal (`!comando`) ou comandos mágicos (`%%sql`, `%%bash`) sempre que possível para manter a prática dentro do Notebook.
4. Entregáveis: Para cada arquivo solicitado, você deve fornecer o conteúdo completo (textos explicativos claros e didáticos + blocos de código executáveis).

Abaixo está a estrutura linear e agrupada do currículo que você deve seguir. 

---

### ESTRUTURA DO CURRÍCULO

**Módulo 01 — Python Fundamental**
* `01_01_Python_Basico.ipynb`: Variáveis, objetos, números, strings, entrada/saída (input/print), booleanos e condicionais (if/elif/else).
* `01_02_Fluxos_e_Estruturas.ipynb`: Laços (while, for, range), Listas, Tuplas e desempacotamento.
* `01_03_Colecoes_e_Comprehensions.ipynb`: Dicionários, Conjuntos (Sets) e Comprehensions (List/Dict/Set).
* `01_04_Funcoes_e_Modulos.ipynb`: Criação de funções, escopo (LEGB), módulos, imports (if __name__ == "__main__").
* `01_05_Arquivos_Erros_e_Debug.ipynb`: Exceções (try/except), manipulação de arquivos (TXT, CSV, JSON) e conceitos de depuração no VS Code.
* `01_99_Lista_Exercicios.ipynb`: Exercícios lineares cobrindo todo o Módulo 1 + enunciado de um mini projeto (Relatório de Vendas Aurora).

**Módulo 02 — Git**
* `02_01_Fundamentos_Git.ipynb`: Modelo mental (snapshots, stage, commits), fluxo essencial (init, add, commit, status, log, diff).
* `02_02_Branches_e_Remotos.ipynb`: Branches, merges, resolução de conflitos, GitHub (clone, push, pull, SSH).
* `02_03_Desfazendo_Alteracoes.ipynb`: Restore, revert, reset, stash.
* `02_99_Lista_Exercicios.ipynb`: Prática guiada com comandos de terminal simulados.

**Módulo 03 — SQL (Usar SQLite para rodar nativo no Jupyter)**
* `03_01_Fundamentos_Relacionais.ipynb`: Por que usar bancos relacionais, Tabelas, Chaves (PK/FK), DDL e Tipos de Dados, Constraints.
* `03_02_Consultas_Basicas.ipynb`: SELECT, WHERE, LIKE, Ordenação, LIMIT, DISTINCT, Funções de agregação, GROUP BY e HAVING.
* `03_03_Joins_e_Subconsultas.ipynb`: INNER JOIN, LEFT/RIGHT/FULL JOIN, Subconsultas e CTEs (WITH).
* `03_04_Manutencao_e_Transacoes.ipynb`: INSERT, UPDATE, DELETE, Índices, Transações (ACID, COMMIT/ROLLBACK).
* `03_99_Lista_Exercicios.ipynb`: Exercícios de modelagem (Diagrama ER) e consultas completas.

**Módulo 04 — Python Avançado**
* `04_01_Funcoes_Avancadas.ipynb`: *args, **kwargs, funções como valores, lambdas, closures, fábricas e decoradores.
* `04_02_Iteradores_e_Geradores.ipynb`: Iteráveis, iteradores, geradores e yield.
* `04_03_Orientacao_a_Objetos.ipynb`: Classes, objetos, self, encapsulamento, herança vs composição, métodos dunder.
* `04_04_Tipagem_e_Estruturas.ipynb`: Dataclasses, Type hints, Pydantic, Ambientes virtuais (venv) e organização de projetos (src/).
* `04_05_Ecosistema_Avancado.ipynb`: Datas (datetime), Logging e Context Managers (with).
* `04_06_Concorrencia.ipynb`: Threads, Processos, GIL, Asyncio (async/await, event loop).
* `04_99_Lista_Exercicios.ipynb`: Prática focada em OOP, tipagem e rotinas assíncronas.

**Módulo 05 — PostgreSQL e MongoDB**
* `05_01_Postgres_e_Drivers.ipynb`: Arquitetura, psql, tipos avançados (JSONB, UUID), psycopg (prevenção de SQL injection).
* `05_02_SQLAlchemy.ipynb`: Engine, Core, ORM Declarativo, sessões, relacionamentos (1-N, N-N), consultas, lazy vs eager loading e Alembic (migrações).
* `05_03_MongoDB.ipynb`: Modelo de documentos (NoSQL vs Relacional), coleções, BSON, PyMongo (CRUD) e Agregações.
* `05_99_Lista_Exercicios.ipynb`: Exercícios comparando implementações ORM vs NoSQL.

**Módulo 06 — FastAPI**
* `06_01_Fundamentos_APIs.ipynb`: HTTP, REST, primeiro servidor Uvicorn, rotas, path/query params.
* `06_02_Pydantic_e_Rotas.ipynb`: Request body, validações, Response models, tratamento de erros (HTTPException).
* `06_03_Arquitetura_e_Banco.ipynb`: Estrutura de projeto, Injeção de dependências (Depends), Sessão de banco por requisição, CRUD completo.
* `06_04_Seguranca_e_Filtros.ipynb`: Pydantic Settings, Autenticação JWT (OAuth2), Autorização (papéis/escopos), Middlewares, CORS e Paginação.
* `06_99_Lista_Exercicios.ipynb`: Criação de uma API completa documentada (OpenAPI/Swagger).

**Módulo 07 — APIs na Prática (Consumo e Integração)**
* `07_01_Consumindo_APIs.ipynb`: httpx, autenticação como cliente, resiliência (retries, backoff), paginação offset/cursor.
* `07_02_Design_e_Funcionalidades.ipynb`: Webhooks, Upload/Download de arquivos, Background tasks, Cache com Redis, WebSockets.
* `07_03_Testes.ipynb`: Testando APIs com pytest e TestClient.
* `07_99_Lista_Exercicios.ipynb`: Exercícios construindo integrações completas.

**Módulo 08 — Docker**
* `08_01_Fundamentos_Containers.ipynb`: Problema de ambiente, Containers vs VMs, comandos essenciais (run, ps, logs, stop).
* `08_02_Criando_Imagens.ipynb`: Dockerfile, otimização de imagens, volumes e bind mounts.
* `08_03_Orquestracao.ipynb`: Redes Docker, Docker Compose (API + Bancos + Redis), Debug em containers.
* `08_99_Lista_Exercicios.ipynb`: Containerização de um projeto prático completo.

**Módulo 09 — Deploy e CI/CD**
* `09_01_Servidores_e_Ambientes.ipynb`: Ambientes, Uvicorn vs Gunicorn, Proxy Reverso (Nginx), princípios 12-factor.
* `09_02_Deploy_Pratico.ipynb`: Deploy em VPS via SSH, Plataformas PaaS.
* `09_03_Pipelines_e_Monitoramento.ipynb`: GitHub Actions (CI para lint/testes, CD para deploy), Logs, monitoramento e Checklist de produção.
* `09_99_Lista_Exercicios.ipynb`: Checklist final e script de deploy.

**Módulo 10 — Engenharia de Dados**
* `10_01_Fundamentos_Engenharia.ipynb`: O que faz a engenharia de dados, OLTP vs. OLAP, Data Lakes e Data Warehouses.
* `10_02_Pandas_Essencial.ipynb`: Séries e DataFrames, seleção/filtros (loc/iloc), limpeza de dados (nulos, duplicatas), transformações vetorizadas, GroupBy/agregações, merge/concat e séries temporais.
* `10_03_Alta_Performance_e_Polars.ipynb`: Performance/memória no Pandas, introdução ao Polars (avaliação lazy), PyArrow e formato colunar Parquet.
* `10_04_Extracao_e_Web_Scraping.ipynb`: Extração de arquivos (CSV, Excel, XML), APIs e bancos de dados (ingestão incremental), Web Scraping com BeautifulSoup (HTML estático) e Selenium (Páginas dinâmicas).
* `10_05_Arquitetura_ETL_e_Qualidade.ipynb`: Desenho de ETL robusto e idempotente (camadas raw → staging → final), qualidade e validação de dados com contratos Pydantic.
* `10_06_Filas_Mensageria_Orquestracao.ipynb`: Redis além do cache (filas, locks), Celery, introdução a RabbitMQ, introdução a Kafka e Apache Airflow (DAGs e fluxos agendados).
* `10_99_Lista_Exercicios.ipynb`: Exercícios práticos focados em processamento de dados e construção de um pipeline ETL de ponta a ponta para ingestão e transformação.

---
Por favor, comece gerando o conteúdo completo dos arquivos do **Módulo 01**. Estruture a sua resposta utilizando blocos de Markdown para a teoria e blocos de código Python para a prática, indicando claramente qual é o nome do arquivo sendo gerado. Pare após concluir o Módulo 1 e pergunte se desejo prosseguir para o Módulo 2.


### PROJETO PRÁTICO TRANSVERSAL: ATLAS (AURORA COMÉRCIO)

Além dos Jupyter Notebooks, você deve estruturar e guiar a construção de um projeto prático transversal chamado **Atlas**. 

**Contexto da Empresa (Aurora Comércio):**
A Aurora Comércio é um e-commerce brasileiro fictício de médio porte em crescimento acelerado (vende eletrônicos de Campinas-SP para o Brasil). Atualmente, é um caos funcional: pedidos em planilhas, relatórios manuais e dados perdidos. O aluno será a primeira pessoa de engenharia da casa. O objetivo é construir o "Atlas", o sistema central da empresa. Não há legado, apenas dores para resolver a cada módulo.

**Regras para a Geração do Projeto Atlas:**
1. **Ambiente Tradicional (Sem Jupyter):** O projeto Atlas não usará Jupyter Notebooks. Ele deve ser estruturado em uma pasta raiz chamada `projeto_Atlas/`, contendo arquivos Python puros (`.py`), SQL (`.sql`), arquivos de configuração, etc.
2. **Esqueleto Baseado em Comentários:** NÃO forneça a solução ou o código funcional nos arquivos do projeto. Crie apenas a estrutura de pastas, as assinaturas de funções/classes e **comentários instrutivos** indicando o que o aluno deve fazer. 
   * Exemplo: `# TODO: Função para ler o arquivo vendas.csv e agrupar o faturamento por cidade.`
3. **Documentação de Ambiente:** Sempre inclua um arquivo `README.md` na raiz do projeto (ou atualize-o) com o passo a passo exato de como preparar o ambiente para aquele módulo (instalação do Python, criação de venv, dependências externas, inicialização do Postgres, comandos Docker, etc.).

**Roteiro do Projeto (Evolução Módulo a Módulo):**
Siga esta evolução para estruturar os esqueletos a cada entrega:
* **M01:** Dor: "Ninguém sabe quanto vendemos por cidade". Entrega: Scripts CLI de relatórios consumindo arquivos CSV.
* **M02:** Dor: "Perdemos uma versão do script ontem". Entrega: Inicialização do repositório Git, .gitignore e automações shell.
* **M03:** Dor: "Os dados estão em 14 planilhas diferentes". Entrega: Criação do Schema relacional modelado (arquivos .sql) e script para popular o banco.
* **M04:** Dor: "O script virou um monstro de 800 linhas". Entrega: Refatoração da CLI para Orientação a Objetos + logging estruturado.
* **M05:** Dor: "SQLite não aguenta; o catálogo muda toda semana". Entrega: Integração com PostgreSQL (ORM + migrações Alembic) e MongoDB (Catálogo).
* **M06:** Dor: "O time do app precisa acessar os dados". Entrega: Criação da API Atlas v1 (FastAPI, CRUD, JWT, OpenAPI).
* **M07:** Dor: "Precisamos falar com transportadora e gateway". Entrega: Integrações resilientes (requests externas), cache (Redis) e recebimento de webhooks.
* **M08:** Dor: "Configurar a máquina de um dev leva 2 dias". Entrega: Containerização completa (`Dockerfile` e `docker-compose.yml`).
* **M09:** Dor: "Subir versão nova é um ritual de risco". Entrega: Arquivos de CI/CD (GitHub Actions) e proxy reverso.
* **M10:** Dor: "Decidimos com dados de 3 semanas atrás". Entrega: Script de ETL diário e orquestração.
* **M11:** Dor: "Ninguém sabe por que o sistema é assim". Entrega: Documentação de Arquitetura (ADRs) e separação clara de camadas.
* **M12:** Dor: "Temos medo de mexer no código". Entrega: Esqueleto da suíte de testes (pytest) rodando no CI.
* **M13:** Entrega Final: Atlas 1.0 consolidado para apresentação.

---
**Instrução de Execução:**
Para a sua primeira resposta, gere todo o conteúdo do **Módulo 01** dividindo em duas partes:
1. Os conteúdos teóricos e práticos nos arquivos `.ipynb` (conforme solicitado nas diretrizes de Jupyter).
2. A estrutura inicial da pasta `projeto_Atlas/` referente ao Módulo 01, contendo o `README.md` de setup, a estrutura de pastas e os arquivos `.py` apenas com os comentários do que deve ser programado. 

Pare após concluir o Módulo 01 por completo e pergunte se desejo seguir para o Módulo 02.