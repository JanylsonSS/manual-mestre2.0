# Roteiro de implementação — Módulo 02 (Git)

> **Pré-requisito:** o Módulo 01 precisa estar funcionando. Você vai versionar código que roda, não esqueleto.

---

## A dor

> *"Ontem o estagiário salvou por cima do `relatorio_vendas.py`. A gente tinha a versão que funcionava… Perdemos o dia."*

## A entrega

`projeto_Atlas` versionado, publicado no GitHub, com histórico limpo e automações de shell.

---

## Etapa 0 — Git instalado e configurado (15 min)

```bash
git --version                                    # 2.30+
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
```

Windows: `git config --global core.autocrlf true`
macOS/Linux: `git config --global core.autocrlf input`

**Pronto quando:** `git config --global --list` mostra seu nome e e-mail.

---

## Etapa 1 — Inicializar o repositório (10 min)

Na raiz de `projeto_Atlas/`:

```bash
git init -b main
git status
```

⚠️ **Antes de qualquer `git add`, olhe o `git status`.** Se `.venv/` aparecer na lista, o `.gitignore` não está sendo respeitado — resolva isso primeiro.

Os arquivos `.gitignore` e `.gitattributes` já estão prontos na raiz. Leia os dois: os comentários explicam cada decisão.

**Pronto quando:** `git status` **não** mostra `.venv/`, `__pycache__/` nem `saida/`.

---

## Etapa 2 — Construir o histórico (45 min)

Não faça um commit gigante. Construa a história como se você tivesse desenvolvido em etapas.

```bash
# 1 — fundação
git add .gitignore .gitattributes .env.example README.md ROTEIRO_M01.md ROTEIRO_M02.md
git commit -m "chore: estrutura inicial do projeto Atlas"

# 2 — dados
git add dados/
git commit -m "chore(dados): adiciona CSVs de exemplo para desenvolvimento"

# 3 em diante — um por módulo
git add src/atlas/__init__.py src/atlas/config.py
git commit -m "feat(config): adiciona constantes e caminhos do projeto"

git add src/atlas/excecoes.py
git commit -m "feat: adiciona hierarquia de exceções de domínio"

git add src/atlas/formatacao.py
git commit -m "feat(formatacao): adiciona formatação monetária brasileira"

git add src/atlas/leitura.py
git commit -m "feat(leitura): adiciona leitor de CSV com validação de colunas"

git add src/atlas/validacao.py
git commit -m "feat(validacao): adiciona validação e normalização de linhas"

git add src/atlas/metricas.py
git commit -m "feat(metricas): adiciona cálculo de métricas de vendas"

git add src/atlas/relatorios.py
git commit -m "feat(relatorios): adiciona renderização em texto e JSON"

git add src/atlas/cli.py main.py
git commit -m "feat(cli): adiciona ponto de entrada da linha de comando"

git add requirements.txt
git commit -m "chore: adiciona arquivo de dependências"
```

**Pronto quando:** `git log --oneline` mostra ~11 commits, todos no padrão Conventional Commits.

**Confira:** `git status` deve dizer *nothing to commit, working tree clean*.

---

## Etapa 3 — Branch de feature (30 min)

Pratique o GitHub Flow com uma funcionalidade nova.

```bash
git switch -c feature/relatorio-por-canal
```

Implemente o agrupamento por canal de venda:

- Em `metricas.py`: já existe `agrupar_por` genérica — só chame com `"canal"` em `calcular_metricas`
- Em `relatorios.py`: adicione a seção no `render_txt` e no `render_json`

Faça **2 ou 3 commits**, não um só.

```bash
git switch main
# faça uma alteração pequena no README para forçar merge de 3 vias
git add README.md
git commit -m "docs: adiciona seção de troubleshooting"

git merge feature/relatorio-por-canal
git branch -d feature/relatorio-por-canal
git log --oneline --graph --all
```

**Pronto quando:** o `--graph` mostra o "balão" do merge de 3 vias.

---

## Etapa 4 — GitHub via SSH (30 min)

**1. Gerar a chave** (se ainda não tiver):

```bash
ls -al ~/.ssh                                # já existe id_ed25519.pub?
ssh-keygen -t ed25519 -C "seu@email.com"
```

**2. Copiar a pública:**

```bash
cat ~/.ssh/id_ed25519.pub                                  # macOS/Linux
type $env:USERPROFILE\.ssh\id_ed25519.pub                  # Windows PowerShell
```

**3. Cadastrar:** GitHub → Settings → SSH and GPG keys → New SSH key → colar.

**4. Testar:**

```bash
ssh -T git@github.com
# esperado: Hi seu-usuario! You've successfully authenticated...
```

**5. Criar o repositório** no GitHub (**sem** README, sem .gitignore — você já tem).

**6. Conectar e enviar:**

```bash
git remote add origin git@github.com:seu-usuario/atlas.git
git push -u origin main
```

**Pronto quando:** você abre o repositório no navegador e vê os 11+ commits.

---

## Etapa 5 — Scripts de automação (60 min)

Os esqueletos estão em `scripts/`. Implemente os do **seu** sistema operacional (fazer os dois é desafio extra).

| Script | O que deve fazer |
|--------|------------------|
| `setup` | Verifica Python, cria `.venv`, instala `requirements.txt`, cria pastas de saída |
| `rodar` | Ativa o venv (se necessário) e executa `main.py` com o CSV padrão ou o informado |
| `limpar` | Remove `saida/*`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/` |
| `verificar` | Roda contra o CSV limpo **e** o sujo, e reporta o resultado dos dois |

**Pronto quando:**

```bash
./scripts/limpar.sh && ./scripts/setup.sh && ./scripts/rodar.sh
```

funciona do zero em uma pasta recém-clonada.

⚠️ **Linux/macOS:** dê permissão de execução e **versione essa permissão**:

```bash
chmod +x scripts/*.sh
git update-index --chmod=+x scripts/setup.sh
```

Sem isso, quem clonar recebe os scripts sem permissão de execução.

---

## Etapa 6 — Simulação de recuperação (30 min)

Documente em `docs/RECUPERACAO.md` (o esqueleto já está lá). Execute de verdade e registre os comandos:

| Cenário | Ferramenta |
|---------|-----------|
| Descartar edição não commitada | `git restore` |
| Corrigir a mensagem do último commit | `git commit --amend` |
| Juntar 3 commits antes do PR | `git reset --soft` |
| Desfazer um commit já enviado | `git revert` |
| Recuperar commits apagados por `reset --hard` | `git reflog` |
| Guardar trabalho para um hotfix urgente | `git stash` |

**Pronto quando:** o documento tem, para cada cenário, o comando exato e a saída observada.

---

## Etapa 7 — Polimento (20 min)

```bash
# Aliases que economizam digitação o resto da vida
git config --global alias.st "status --short"
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 --stat"
git config --global alias.unstage "restore --staged"

# Tag da versão
git tag -a v0.1.0 -m "Atlas M01 — relatórios CLI sobre CSV"
git push --tags
```

Revise o `README.md`: quem clonar o repositório consegue rodar só lendo ele?

---

## Checklist de entrega

- [ ] `git status` limpo, sem `.venv`, `__pycache__` ou `saida/`
- [ ] Pelo menos 11 commits com mensagens no padrão Conventional Commits
- [ ] Um branch de feature criado, usado e mesclado (merge de 3 vias no `--graph`)
- [ ] Repositório no GitHub, autenticado por SSH
- [ ] `scripts/` com pelo menos `setup`, `rodar` e `limpar` funcionando
- [ ] `docs/RECUPERACAO.md` preenchido com os 6 cenários
- [ ] Tag `v0.1.0` criada e enviada
- [ ] Um colega (ou você mesmo, em outra pasta) consegue clonar e rodar

---

## Desafios extras

| Desafio | Onde |
|---------|------|
| ⭐ Hook `pre-commit` que roda `ruff check` | `.git/hooks/pre-commit` |
| ⭐ `CONTRIBUTING.md` com o padrão de branches e commits | raiz |
| ⭐ Template de commit (`git config commit.template .gitmessage`) | `.gitmessage` |
| ⭐⭐ Abrir um PR de verdade e fazer a autorrevisão no GitHub | GitHub |
| ⭐⭐ `.vscode/settings.json` versionado com a configuração do projeto | `.vscode/` |

---

## Tempo total estimado

**4 a 5 horas.** A parte de SSH costuma travar a primeira vez — reserve tempo para ela.
