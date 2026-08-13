#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Sobe a infraestrutura local (PostgreSQL + MongoDB)
#
#  Uso:  ./scripts/subir.sh
# ═══════════════════════════════════════════════════════════════

# TODO: set -euo pipefail
# TODO: descobrir a raiz e fazer cd (igual aos scripts do M02)

# ── 1. Docker está instalado e rodando? ──────────────────────
# TODO: `docker info` falha se o daemon não estiver de pé.
#   Mensagem de erro boa diz o que fazer:
#     ✖ Docker não está rodando. Abra o Docker Desktop.

# ── 2. Existe .env? ──────────────────────────────────────────
# TODO: se não existir, copie de .env.example e avise que é
#   preciso revisar as senhas.

# ── 3. Sobe ──────────────────────────────────────────────────
# TODO: docker compose up -d postgres mongo

# ── 4. Espera ficar saudável ─────────────────────────────────
# TODO: aguarde o healthcheck em vez de dormir um tempo fixo.
#
#   Laço com timeout, consultando:
#     docker compose ps --format json
#   ou
#     docker inspect --format='{{.State.Health.Status}}' atlas_postgres
#
#   ⚠️ `sleep 10` é o antipadrão clássico: lento quando o banco sobe
#      rápido, e insuficiente quando a máquina está carregada.

# ── 5. Aplica as migrações ───────────────────────────────────
# TODO: alembic upgrade head

# ── 6. Resumo ────────────────────────────────────────────────
# TODO: imprima as URLs de conexão (SEM as senhas) e os comandos
#   úteis para inspecionar cada banco.
