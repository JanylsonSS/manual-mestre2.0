# Manual de Estudos Interativo

**Engenharia de Software & Ciência de Dados — do zero à produção**

Um curso completo em Jupyter Notebooks, feito para rodar no VS Code. Cada
assunto tem a teoria e a prática **no mesmo arquivo**: você lê a explicação e
executa o código logo abaixo.

---

## O que é isto

Não é um livro nem uma coleção de tutoriais. É um **manual executável**.

Todo conceito aparece três vezes, em profundidade crescente:

1. **Explicação** — o que é e por que existe
2. **Código rodável** — que você executa, modifica e quebra de propósito
3. **Aplicação** — no projeto Atlas, um sistema real que cresce a cada módulo

A diferença em relação a um curso comum está no que vem **junto** com o
conteúdo: as armadilhas. Você não aprende só que `0.1 + 0.2` existe — você
executa a célula e vê que não dá `0.3`. Não aprende só que race conditions
existem — você provoca uma e vê 80% dos incrementos evaporarem.

---

## Estrutura

```
Roadmap/
├── README.md                       ← você está aqui
├── progresso.md                    ← controle de datas e conclusão
├── roadmap.md                      ← especificação original do currículo
│
├── Modulo_01_Python_Fundamental/   ← 6 notebooks
├── Modulo_02_Git/                  ← 4 notebooks
├── Modulo_03_SQL/                  ← 5 notebooks
├── Modulo_04_Python_Avancado/      ← 7 notebooks
├── Modulo_05_PostgreSQL_MongoDB/   ← 4 notebooks
├── Modulo_06_FastAPI/              ← 5 notebooks
├── Modulo_07_APIs_na_Pratica/      ← 4 notebooks
├── Modulo_08_Docker/               ← 4 notebooks
├── Modulo_09_Deploy_CICD/          ← 4 notebooks
│   └── (10 conforme for gerado)
│
└── projeto_Atlas/                  ← o projeto prático transversal
```

Dentro de cada módulo, os arquivos seguem a numeração `MM_AA_Nome.ipynb`, e o
`MM_99_Lista_Exercicios.ipynb` fecha o módulo com a lista completa e o projeto.

---

## O currículo

| # | Módulo | Aulas | Você sai sabendo |
|---|--------|:-----:|------------------|
| 01 | **Python Fundamental** | 6 | Variáveis, coleções, funções, arquivos, exceções, debug no VS Code |
| 02 | **Git** | 4 | Versionamento, branches, conflitos, GitHub, e como desfazer qualquer coisa |
| 03 | **SQL** | 5 | Modelagem relacional, consultas, joins, CTEs, índices, transações |
| 04 | **Python Avançado** | 7 | Decoradores, geradores, OOP, tipagem, logging, concorrência |
| 05 | **PostgreSQL e MongoDB** | 4 | ORM, migrações, NoSQL, agregações |
| 06 | **FastAPI** | 5 | REST, validação, autenticação JWT, OpenAPI |
| 07 | **APIs na Prática** | 4 | Consumo resiliente, webhooks, cache, WebSockets, testes |
| 08 | **Docker** | 4 | Containers, Dockerfile, Compose, orquestração local |
| 09 | **Deploy e CI/CD** | 4 | Servidores, proxy reverso, GitHub Actions, monitoramento |
| 10 | **Engenharia de Dados** | 7 | Pandas, Polars, scraping, ETL, Airflow, Kafka |

**Estado atual:** Módulos 01 a 09 prontos (43 notebooks, 3.104 células).

---

## O projeto Atlas

Paralelo aos notebooks, você constrói um sistema de verdade.

> **Aurora Comércio** é um e-commerce brasileiro de eletrônicos, de Campinas-SP.
> Cresce rápido e opera em caos: pedidos em planilhas, relatórios manuais,
> dados perdidos. Você é a **primeira pessoa de engenharia** da casa.

A cada módulo, uma dor nova do negócio:

| Módulo | A dor | O que você constrói |
|--------|-------|---------------------|
| M01 | *"Ninguém sabe quanto vendemos por cidade"* | CLI de relatórios sobre CSV |
| M02 | *"Perdemos uma versão do script ontem"* | Git, `.gitignore`, automações |
| M03 | *"Os dados estão em 14 planilhas"* | Schema relacional + carga |
| M04 | *"O script virou um monstro de 800 linhas"* | OOP + logging estruturado |
| M05 | *"SQLite não aguenta"* | PostgreSQL + MongoDB |
| M06 | *"O time do app precisa acessar os dados"* | API Atlas v1 |
| M07 | *"Precisamos falar com a transportadora"* | Integrações resilientes |
| M08 | *"Configurar a máquina leva 2 dias"* | Containerização |
| M09 | *"Subir versão é um ritual de risco"* | CI/CD |
| M10 | *"Decidimos com dados de 3 semanas atrás"* | ETL + orquestração |
| M11–13 | *"Temos medo de mexer no código"* | ADRs, testes, Atlas 1.0 |

O `projeto_Atlas/` vem como **esqueleto**: estrutura de pastas, assinaturas de
função, docstrings e comentários `# TODO` dizendo o que fazer. **A solução não
está lá** — o código é seu.

---

## Como começar

### 1. Instalar o necessário

| Ferramenta | Por quê |
|------------|---------|
| **Python 3.10+** | Marque *"Add Python to PATH"* no Windows |
| **VS Code** | Onde tudo acontece |
| **Git** | A partir do Módulo 02 |

Extensões do VS Code: **Python**, **Pylance** e **Jupyter** (todas da Microsoft).

### 2. Abrir o primeiro notebook

```
Modulo_01_Python_Fundamental/01_01_Python_Basico.ipynb
```

Clique em **Select Kernel** no canto superior direito e escolha seu Python.

### 3. Executar

`Shift + Enter` roda a célula e vai para a próxima.

> ⚠️ **Execute as células na ordem, de cima para baixo.** Muitos notebooks têm
> uma célula de preparação no início que cria os dados usados pelo resto.

---

## Como usar de verdade

**Leia menos, execute mais.** O manual foi escrito para ser rodado, não lido.

| Faça | Não faça |
|------|----------|
| Mude os valores e rode de novo | Ler passivamente até o fim |
| Descomente as linhas que causam erro | Pular as células marcadas com ⚠️ |
| Tente prever a saída antes de executar | Copiar a resposta dos exercícios |
| Quebre o código de propósito | Seguir para o módulo seguinte sem o projeto |

### Os marcadores

Ao longo dos notebooks você vai encontrar:

| Marcador | Significa |
|----------|-----------|
| 💡 | Dica prática, atalho ou idioma da linguagem |
| ⚠️ | Armadilha — leia com atenção |
| 🔴 | Erro grave ou risco de segurança |
| 💭 | Reflexão sobre a decisão de projeto |
| 🔧 | Prática guiada com os dados da Aurora |
| 📝 | Exercícios |
| 📋 | Cola de referência do módulo |
| ✅ | Checklist de saída |

### O ritmo

Cada módulo tem uma estimativa no seu `ROTEIRO_MXX.md` dentro de
`projeto_Atlas/`. Como referência, o Módulo 01 leva de 6 a 8 horas de trabalho
concentrado, e o Módulo 04 de 10 a 12.

**Não pule os projetos.** Os notebooks ensinam as peças; o Atlas é onde você
descobre que sabe montá-las.

Registre suas datas em **`progresso.md`**.

---

## Como o conteúdo foi verificado

Todos os notebooks foram executados célula a célula num simulador fiel ao
Jupyter (usando o próprio transformador de entrada do IPython), e as saídas
foram inspecionadas manualmente.

Até aqui: **1.770 células de código, zero falhas**. Os comandos Git rodam de
verdade em repositórios descartáveis, o SQL executa contra um SQLite real, o
Alembic gera e aplica migrações de verdade, as APIs do M06 respondem a
requisições HTTP reais, o M07 sobe servidores em `127.0.0.1` e fala com eles
por **HTTP sobre socket** (para que timeout e recusa de conexão sejam de
verdade), o `pytest` roda 47 testes reais, o M08 constrói containers ao vivo
com `unshare` (os cinco namespaces do Linux, sem precisar de Docker), o M09
sobe Gunicorn com múltiplos workers e um proxy reverso de verdade, e os
benchmarks de memória e concorrência foram medidos, não estimados.

Isso importa porque um manual em que uma célula não roda é um manual em que
você vai perder uma hora achando que o erro é seu.

### Bancos de dados: dois modos

A partir do Módulo 05 entram PostgreSQL e MongoDB, que são **servidores**. Os
notebooks detectam o que está disponível na sua máquina:

| Modo | Quando | O que roda |
|------|--------|------------|
| 🐘🍃 **Real** | Você rodou `docker compose up -d` | Tudo |
| 📦 **Fallback** | Sem Docker | SQLAlchemy sobre SQLite + `mongomock` |

### Docker: modo duplo no Módulo 08

Docker exige um *daemon*, que não roda dentro de todo ambiente. O Módulo 08 é
explícito sobre o que é executado e o que não é:

| | O que é | Como aparece |
|---|---------|--------------|
| ✅ **Executado** | Namespaces do Linux, análise de Dockerfile, validação de compose | Saída normal |
| 📖 **Referência** | Comandos `docker ...` | Marcados com `[referência]` |

E há um ganho no arranjo: em vez de decorar `docker run`, você **constrói um
container à mão** com as chamadas de sistema que o Docker usa por baixo — e
escreve um analisador de Dockerfile e um validador de compose que encontram os
problemas antes do build. Se você tiver Docker instalado, os comandos executam
de verdade.

O fallback cobre a maior parte do conteúdo, e os trechos exclusivos de cada
banco aparecem como blocos de referência com o SQL comentado. **Nenhuma célula
falha em nenhum dos dois modos.**

---

## Convenções

- **Tudo em português**, exceto palavras-chave da linguagem e termos técnicos
  consagrados (*commit*, *merge*, *deploy*)
- Código segue **PEP 8**: `snake_case`, 4 espaços, type hints
- Os laboratórios criam pastas descartáveis (`lab_git/`, `dados_aula/`) —
  apague quando quiser
- Dados sintéticos usam **semente fixa**: os números que você vê são os mesmos
  do manual

---

## Perguntas frequentes

**Preciso saber programar?**
Não. O Módulo 01 começa em variáveis. Mas o ritmo é de quem quer trabalhar com
isso, não de quem está curioso.

**Posso pular módulos?**
Os notebooks se referenciam entre si e o Atlas é cumulativo. Se você já sabe
Git, faça a lista de exercícios do M02 e siga — mas não pule o projeto.

**As respostas dos exercícios estão em algum lugar?**
Não, deliberadamente. Exercício com gabarito ao lado vira leitura. Quando
travar, releia a aula correspondente e o traceback — nessa ordem.

**E se um notebook der erro?**
Confira se você executou as células anteriores, e se o kernel é o Python certo.
Se o erro persistir, ele provavelmente é intencional: várias células
demonstram falhas de propósito.

---

*Manual de Estudos Interativo · Projeto Atlas / Aurora Comércio*
