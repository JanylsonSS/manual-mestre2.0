# ═══════════════════════════════════════════════════════════════
#  Atlas — setup do ambiente de desenvolvimento (Windows)
#
#  Uso:  .\scripts\setup.ps1
#
#  Se o PowerShell recusar a execução, rode UMA VEZ:
#      Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
#
#  Deve ser IDEMPOTENTE: rodar duas vezes não pode quebrar nada.
# ═══════════════════════════════════════════════════════════════

# TODO: fazer o script abortar no primeiro erro.
#   $ErrorActionPreference = "Stop"
#
#   Por padrão o PowerShell CONTINUA depois de um erro não-terminante,
#   o que faz o script "funcionar" mesmo tendo falhado no meio.


# ── Descobrir a raiz do projeto ──────────────────────────────
# TODO: o script precisa funcionar sendo chamado de qualquer pasta.
#   $Raiz = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
#   Set-Location $Raiz


# ── Funções de saída ─────────────────────────────────────────
function Info    { param($msg) Write-Host "> $msg" -ForegroundColor Green }
function Aviso   { param($msg) Write-Host "! $msg" -ForegroundColor Yellow }
function Erro    { param($msg) Write-Host "x $msg" -ForegroundColor Red }


Write-Host "==============================================="
Write-Host "  Atlas - preparacao do ambiente"
Write-Host "==============================================="


# ── 1. Verificar o Python ────────────────────────────────────
# TODO: confirmar que `python` existe e a versão é >= 3.10.
#   - Get-Command python -ErrorAction SilentlyContinue
#   - python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)"
#   - Verifique $LASTEXITCODE
#   - Se falhar: mensagem com o link de download e `exit 1`
#
#   ⚠️ No Windows o comando é `python`, não `python3`.
#      Se o Windows abrir a Microsoft Store ao digitar `python`,
#      o Python não está no PATH — reinstale marcando
#      "Add Python to PATH".


# ── 2. Criar o ambiente virtual ──────────────────────────────
# TODO: criar .venv se não existir.
#   if (-not (Test-Path ".venv")) { python -m venv .venv }
#   else { Aviso "Reutilizando .venv existente" }


# ── 3. Atualizar o pip ───────────────────────────────────────
# TODO: & ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
#
#   💡 O `&` (call operator) é necessário para executar um caminho
#      guardado em string. Sem ele o PowerShell trata como texto.


# ── 4. Instalar dependências ─────────────────────────────────
# TODO: se requirements.txt existir:
#   & ".venv\Scripts\pip.exe" install -r requirements.txt --quiet


# ── 5. Criar as pastas de saída ──────────────────────────────
# TODO: New-Item -ItemType Directory -Force -Path "saida", "dados\processados"
#   O -Force não reclama se já existir.


# ── 6. Criar o .env a partir do exemplo ──────────────────────
# TODO: se .env NÃO existir e .env.example existir:
#   Copy-Item ".env.example" ".env"
#   Nunca sobrescreva um .env existente.


# ── 7. Resumo final ──────────────────────────────────────────
# TODO: imprimir as instruções:
#
#       Ambiente pronto. Para ativar:
#           .\.venv\Scripts\Activate.ps1
#       Para rodar o relatorio:
#           .\scripts\rodar.ps1


# TODO: exit 0
