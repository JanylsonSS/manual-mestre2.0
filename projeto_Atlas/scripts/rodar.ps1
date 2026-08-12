# ═══════════════════════════════════════════════════════════════
#  Atlas — executa o relatório (Windows)
#
#  Uso:
#      .\scripts\rodar.ps1
#      .\scripts\rodar.ps1 dados\brutos\vendas_sujas.csv
# ═══════════════════════════════════════════════════════════════

# TODO: declarar o parâmetro opcional com valor padrão.
#   param(
#       [string]$Arquivo = "dados\brutos\vendas_jul2026.csv"
#   )
#
#   ⚠️ O bloco `param(...)` precisa ser a PRIMEIRA instrução
#      executável do arquivo (comentários antes tudo bem).

# TODO: $ErrorActionPreference = "Stop"
# TODO: descobrir a raiz e fazer Set-Location


# ── 1. Verificar que o ambiente existe ───────────────────────
# TODO: se .venv\Scripts\python.exe não existir, orientar o usuário
#   a rodar .\scripts\setup.ps1 primeiro e sair com exit 1.


# ── 2. Verificar que o arquivo existe ────────────────────────
# TODO: if (-not (Test-Path $Arquivo)) { ... exit 1 }


# ── 3. Executar ──────────────────────────────────────────────
# TODO: & ".venv\Scripts\python.exe" main.py $Arquivo


# ── 4. Reportar o resultado ──────────────────────────────────
# TODO: verificar $LASTEXITCODE.
#   Se 0, informar onde ficaram os relatórios (pasta saida\).
#   Propagar com `exit $LASTEXITCODE`.
#
#   💡 $LASTEXITCODE guarda o código de saída do último programa
#      externo executado. É o equivalente ao $? do bash.
