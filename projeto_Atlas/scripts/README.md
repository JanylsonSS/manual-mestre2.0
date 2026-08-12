# Scripts de automação — Atlas

## Por que automatizar

Todo comando que você digita mais de três vezes deve virar script. Não é preguiça — é:

- **Reprodutibilidade.** O script faz sempre a mesma coisa, na mesma ordem.
- **Documentação executável.** O `setup.sh` *é* a resposta para "como preparo o ambiente?".
- **Onboarding.** Um dev novo roda um comando em vez de seguir 12 passos de um README.
- **Base para CI/CD.** No Módulo 09, o GitHub Actions vai chamar exatamente estes scripts.

## Qual versão usar

| Seu sistema | Extensão | Como rodar |
|-------------|----------|------------|
| Linux / macOS | `.sh` | `./scripts/setup.sh` |
| Windows (PowerShell) | `.ps1` | `.\scripts\setup.ps1` |
| Windows (Git Bash / WSL) | `.sh` | `./scripts/setup.sh` |

Implemente os do **seu** sistema. Fazer os dois é desafio extra — mas vale a pena se você trabalha em time misto.

## Os quatro scripts

| Script | Responsabilidade |
|--------|------------------|
| `setup` | Prepara o ambiente do zero: venv, dependências, pastas |
| `rodar` | Executa o relatório |
| `limpar` | Remove tudo que é gerado |
| `verificar` | Roda contra os dois CSVs e reporta |

## Permissão de execução (Linux / macOS)

```bash
chmod +x scripts/*.sh
```

E — importante — **versione essa permissão**, senão quem clonar recebe os scripts sem ela:

```bash
git update-index --chmod=+x scripts/setup.sh scripts/rodar.sh scripts/limpar.sh scripts/verificar.sh
git commit -m "chore(scripts): marca scripts como executáveis"
```

## Política de execução (Windows / PowerShell)

Se o PowerShell recusar com *"execução de scripts foi desabilitada"*, rode **uma vez**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Convenções que os scripts devem seguir

1. **Falhar alto.** Em bash, comece com `set -euo pipefail`. Um script que continua depois de um erro é pior que um script que não roda.
2. **Ser idempotente.** Rodar duas vezes não pode quebrar nada.
3. **Dizer o que está fazendo.** Uma linha de eco por etapa.
4. **Devolver código de saída correto.** `0` = sucesso, diferente de `0` = falha. O CI depende disso.
5. **Funcionar de qualquer diretório.** Descubra a raiz do projeto a partir do caminho do próprio script, não de `pwd`.

> 💡 **Dica para a regra 5** em bash:
> ```bash
> RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
> cd "$RAIZ"
> ```
> Em PowerShell:
> ```powershell
> $Raiz = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
> Set-Location $Raiz
> ```
