# ═══════════════════════════════════════════════════════════════
#  Atlas — limpeza de arquivos gerados (Windows)
#
#  Uso:
#      .\scripts\limpar.ps1
#      .\scripts\limpar.ps1 -Tudo     # remove também o .venv
#
#  ⚠️ Este script APAGA arquivos. Só inclua o que é regenerável.
# ═══════════════════════════════════════════════════════════════

# TODO: param([switch]$Tudo)
#
#   Um [switch] é um parâmetro booleano de linha de comando:
#   presente = $true, ausente = $false.

# TODO: $ErrorActionPreference = "Stop"
# TODO: descobrir a raiz e fazer Set-Location


# ── 1. Limpar as saídas geradas ──────────────────────────────
# TODO: remover o CONTEÚDO de saida\ e dados\processados\,
#   preservando as pastas e os arquivos .gitkeep.
#
#   💡 Get-ChildItem "saida" -File -Recurse |
#          Where-Object { $_.Name -ne ".gitkeep" } |
#          Remove-Item -Force
#
#   ⚠️ NÃO use Remove-Item "saida" -Recurse — isso apaga a pasta
#      inteira, incluindo o .gitkeep que mantém ela versionada.


# ── 2. Limpar caches do Python ───────────────────────────────
# TODO: remover recursivamente __pycache__, *.pyc,
#   .pytest_cache, .mypy_cache, .ruff_cache
#
#   💡 Get-ChildItem -Path . -Include "__pycache__" -Recurse -Directory |
#          Where-Object { $_.FullName -notlike "*\.venv\*" } |
#          Remove-Item -Recurse -Force
#
#   ⚠️ O filtro do .venv é importante: sem ele você varre milhares
#      de pastas de dependências sem necessidade (e demora muito).


# ── 3. Remover o venv (só com -Tudo) ─────────────────────────
# TODO: if ($Tudo) { Remove-Item ".venv" -Recurse -Force }
#   Avise que será preciso rodar setup.ps1 novamente.


# ── 4. Resumo ────────────────────────────────────────────────
# TODO: reportar o que foi removido.
#   💡 Desafio: conte os itens antes de apagar e mostre o total.
