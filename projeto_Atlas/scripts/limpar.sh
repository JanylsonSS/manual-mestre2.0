#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Atlas — limpeza de arquivos gerados (Linux / macOS)
#
#  Uso:
#      ./scripts/limpar.sh          # limpa saídas e caches
#      ./scripts/limpar.sh --tudo   # remove também o .venv
#
#  ⚠️ Este script APAGA arquivos. Seja explícito sobre o que ele
#     remove e nunca inclua nada que não seja regenerável.
# ═══════════════════════════════════════════════════════════════

# TODO: set -euo pipefail
# TODO: descobrir a raiz e fazer cd


# ── 1. Interpretar o argumento ───────────────────────────────
# TODO: detectar a flag --tudo
#   `LIMPAR_VENV=false`
#   `if [ "${1:-}" = "--tudo" ]; then LIMPAR_VENV=true; fi`


# ── 2. Limpar as saídas geradas ──────────────────────────────
# TODO: remover o CONTEÚDO de saida/ e dados/processados/,
#   mas MANTER as pastas e os arquivos .gitkeep.
#
#   💡 Um jeito seguro:
#      find saida -type f ! -name '.gitkeep' -delete
#
#   ⚠️ NÃO use `rm -rf saida/` — isso apaga a pasta e o .gitkeep,
#      e o próximo git status vai reclamar.


# ── 3. Limpar caches do Python ───────────────────────────────
# TODO: remover recursivamente:
#   - todas as pastas __pycache__
#   - todos os arquivos *.pyc
#   - .pytest_cache, .mypy_cache, .ruff_cache
#
#   💡 `find . -type d -name "__pycache__" -exec rm -rf {} +`
#      O `+` no final agrupa os caminhos em uma chamada só —
#      mais rápido que `\;`, que chama o rm uma vez por pasta.
#
#   ⚠️ Cuidado para não descer dentro de .venv/ — use
#      `-not -path "./.venv/*"` para excluí-lo da varredura.


# ── 4. Remover o venv (só com --tudo) ────────────────────────
# TODO: se LIMPAR_VENV for true, `rm -rf .venv`
#   Avise o usuário que ele vai precisar rodar setup.sh de novo.


# ── 5. Resumo ────────────────────────────────────────────────
# TODO: informar quantos itens foram removidos, ou pelo menos
#   confirmar que a limpeza terminou.
#
#   💡 Desafio: conte os arquivos antes de apagar e reporte
#      "removidos 47 arquivos e 12 pastas".
