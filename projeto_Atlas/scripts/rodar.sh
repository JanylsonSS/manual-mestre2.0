#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Atlas — executa o relatório (Linux / macOS)
#
#  Uso:
#      ./scripts/rodar.sh                              # CSV padrão
#      ./scripts/rodar.sh dados/brutos/vendas_sujas.csv
# ═══════════════════════════════════════════════════════════════

# TODO: set -euo pipefail
# TODO: descobrir a raiz e fazer cd (igual ao setup.sh)


# ── 1. Verificar que o ambiente existe ───────────────────────
# TODO: se .venv não existir, informar que é preciso rodar
#   ./scripts/setup.sh primeiro, e sair com exit 1.
#
#   💡 Mensagem de erro boa diz o que fazer, não só o que deu errado:
#      ✖ Ambiente virtual não encontrado.
#        Rode primeiro: ./scripts/setup.sh


# ── 2. Resolver o argumento ──────────────────────────────────
# TODO: usar $1 se informado, senão o CSV padrão.
#   `ARQUIVO="${1:-dados/brutos/vendas_jul2026.csv}"`
#
#   A sintaxe ${VAR:-padrao} significa "use VAR, ou o padrão se
#   VAR estiver vazia/indefinida". É o idioma bash para valor default.


# ── 3. Verificar que o arquivo existe ────────────────────────
# TODO: `if [ ! -f "$ARQUIVO" ]; then ... exit 1; fi`


# ── 4. Executar ──────────────────────────────────────────────
# TODO: `.venv/bin/python main.py "$ARQUIVO"`
#
#   ⚠️ As aspas em "$ARQUIVO" são obrigatórias. Sem elas, um caminho
#      com espaço ("dados brutos/vendas.csv") vira dois argumentos.


# ── 5. Reportar o resultado ──────────────────────────────────
# TODO: capturar o código de saída do Python e reportar.
#   `CODIGO=$?`
#   Se 0, avise onde ficaram os relatórios (pasta saida/).
#   Se não, avise que falhou.
#   Propague o código com `exit $CODIGO` — o CI depende disso.
