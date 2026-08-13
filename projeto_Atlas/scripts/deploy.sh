#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Deploy do Atlas — Módulo 09
#
#      ./scripts/deploy.sh producao
#      ./scripts/deploy.sh homologacao
#
#  💭 O deploy da Aurora hoje é: `ssh root@servidor`, `git pull`,
#     `kill`, `nohup ... &`. Cada uma dessas quatro coisas é um
#     problema — e este script resolve as quatro.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail
#   -e  🔴 aborta no primeiro erro. Sem isto, um passo falha e o
#       script continua, deixando o deploy pela metade — que é pior
#       que não ter feito deploy nenhum.
#   -u  variável não definida é erro (pega typo em nome de env)
#   -o pipefail  erro no meio de um pipe não é engolido

AMBIENTE="${1:?uso: ./scripts/deploy.sh <producao|homologacao>}"

# TODO: definir a partir do ambiente
# SERVIDOR="atlas-${AMBIENTE}"      # o Host do ~/.ssh/config
# RAIZ="/opt/atlas"

# 🔑 O nome do release começa com a DATA em formato ISO. É isso que
#    faz `sort` devolver a ordem cronológica — e é o que o rollback
#    e a limpeza usam para achar o "anterior".
# VERSAO="$(date -u +%Y%m%d-%H%M%S)-$(git rev-parse --short HEAD)"
# RELEASE="${RAIZ}/releases/${VERSAO}"


# ───────────────────────────────────────────────────────────────
# 1. Conferir ANTES de tocar no servidor
# ───────────────────────────────────────────────────────────────
# 🔑 Falhar aqui custa 5 segundos. Falhar no servidor custa um
#    rollback, o site fora do ar, e o seu domingo.
#
# TODO:
#   git diff --quiet || { echo "🔴 há alterações não commitadas"; exit 1; }
#   pytest -q -m "not integracao"              # M07
#   python scripts/auditar_containers.py       # M08
#
#   ⚠️ E limpe o bytecode antes de testar:
#        find . -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
#      Um .pyc velho faz o teste verificar código que não existe mais
#      (aula 09_03) — sem erro, sem aviso.


# ───────────────────────────────────────────────────────────────
# 2. Enviar o artefato
# ───────────────────────────────────────────────────────────────
# 🔴 ENVIE, não faça `git pull` no servidor.
#
#    `git pull` significa que o build acontece em produção — e o que
#    roda lá nunca foi testado. Uma dependência que resolveu
#    diferente, um arquivo não commitado, um .pyc velho.
#
# TODO:
#   ssh "$SERVIDOR" "mkdir -p ${RELEASE}"
#   rsync -az --delete --exclude-from=deploy_excluir.txt ./ "${SERVIDOR}:${RELEASE}/"
#
#   ⚠️ `--delete` é perigoso: na PRIMEIRA vez que apontar para um
#      destino novo, rode com `--dry-run`.


# ───────────────────────────────────────────────────────────────
# 3. Preparar o release
# ───────────────────────────────────────────────────────────────
# 🔑 O `.env` é um LINK para o compartilhado — assim a configuração
#    sobrevive a todo deploy e a todo rollback.
#
# TODO:
#   ssh "$SERVIDOR" bash -s <<REMOTO
#     set -euo pipefail
#     cd "${RELEASE}"
#     ln -sfn ${RAIZ}/compartilhado/.env .env
#     python -m venv .venv
#     .venv/bin/pip install --no-cache-dir -q .
#   REMOTO


# ───────────────────────────────────────────────────────────────
# 4. 🔴 Migrações — ANTES de trocar o código
# ───────────────────────────────────────────────────────────────
# 💭 Durante o deploy, código velho e novo convivem. Migração ANTES
#    exige que o código VELHO funcione com o schema NOVO — o que é
#    fácil para adicionar coluna e impossível para remover.
#
#    ✅ adicionar coluna/tabela/índice
#    🔴 renomear · remover · mudar tipo · NOT NULL sem default
#
#    Para renomear sem queda: três deploys (escreve nos dois → lê do
#    novo → remove o antigo).
#
# TODO:
#   ssh "$SERVIDOR" "cd ${RELEASE} && .venv/bin/alembic upgrade head"


# ───────────────────────────────────────────────────────────────
# 5. Trocar o symlink e recarregar
# ───────────────────────────────────────────────────────────────
# 🎯 A troca precisa ser ATÔMICA.
#
#    `ln -sfn` remove e recria — há uma janela de microssegundos em
#    que `atual` não aponta para nada. Sob carga, alguém cai nela, e
#    o bug acontece uma vez a cada dez mil requisições.
#
#    `mv -T` usa `rename()`, que é atômico no POSIX: ou é o antigo,
#    ou é o novo, nunca um estado intermediário.
#
# TODO:
#   ssh "$SERVIDOR" bash -s <<REMOTO
#     set -euo pipefail
#     ln -sfn "releases/${VERSAO}" "${RAIZ}/atual.novo"
#     mv -T "${RAIZ}/atual.novo" "${RAIZ}/atual"
#     sudo systemctl reload atlas
#   REMOTO
#
#   🔑 `reload` (SIGHUP), não `restart`. O gunicorn sobe workers
#      novos, deixa os velhos terminarem, e só então os encerra.


# ───────────────────────────────────────────────────────────────
# 6. 🔴 Verificar que subiu
# ───────────────────────────────────────────────────────────────
# 💭 Um deploy que não verifica não é um deploy — é uma esperança.
#
# TODO:
#   for i in $(seq 1 20); do
#     if curl -fsS --max-time 3 https://atlas.aurora.com.br/saude >/dev/null; then
#       echo "✅ ${VERSAO} no ar"
#       # limpeza: mantém os últimos 5 releases
#       ssh "$SERVIDOR" "ls -1dt ${RAIZ}/releases/*/ | tail -n +6 | xargs -r rm -rf"
#       exit 0
#     fi
#     sleep 3
#   done


# ───────────────────────────────────────────────────────────────
# 7. 🔴 Não subiu: reverter sozinho
# ───────────────────────────────────────────────────────────────
# 🎯 Esta é a diferença entre "o site está fora e não sei por quê" e
#    "voltou sozinho em 60 segundos, agora eu investigo com calma".
#
# TODO:
#   echo "🔴 a saúde não respondeu — revertendo"
#   ssh "$SERVIDOR" "${RAIZ}/rollback.sh"
#   exit 1
