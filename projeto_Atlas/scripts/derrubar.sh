#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Derruba a infraestrutura local
#
#  Uso:
#      ./scripts/derrubar.sh              mantém os dados
#      ./scripts/derrubar.sh --apagar     ⚠️ APAGA OS VOLUMES
# ═══════════════════════════════════════════════════════════════

# TODO: set -euo pipefail
# TODO: descobrir a raiz e fazer cd

# ── Interpretar a flag ───────────────────────────────────────
# TODO: detectar --apagar

# ── 🔴 Confirmação obrigatória para --apagar ─────────────────
# TODO: `docker compose down -v` destrói os volumes. É irreversível.
#   EXIJA confirmação digitada:
#
#     read -p "Digite APAGAR para confirmar: " resposta
#     [ "$resposta" = "APAGAR" ] || { echo "Cancelado."; exit 1; }
#
#   Comando destrutivo sem trava é um acidente esperando acontecer —
#   a mesma lição do `schema --recriar` no M03.

# ── Derrubar ─────────────────────────────────────────────────
# TODO: docker compose down   (ou down -v)
