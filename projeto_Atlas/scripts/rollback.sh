#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Rollback do Atlas — roda NO SERVIDOR (Módulo 09)
#
#      /opt/atlas/rollback.sh
#
#  💭 ESTE SCRIPT SERÁ RODADO ÀS 2H DA MANHÃ, POR ALGUÉM COM SONO,
#     COM O SITE FORA E O TELEFONE TOCANDO.
#
#     Por isso ele não tem opção nenhuma, não faz pergunta, e não
#     exige que você lembre de nada. Volta para o release anterior,
#     confere, e diz se deu certo.
#
#     🎯 Se você precisar pensar para usar o rollback, ele falhou
#        como projeto.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

# TODO: RAIZ="/opt/atlas"

# ───────────────────────────────────────────────────────────────
# 1. Descobrir o release anterior
# ───────────────────────────────────────────────────────────────
# 🔑 Funciona porque o nome do release começa com a DATA em formato
#    ISO — `sort` devolve a ordem cronológica de graça.
#
# TODO:
#   ATUAL="$(basename "$(readlink "${RAIZ}/atual")")"
#   ANTERIOR="$(ls -1d "${RAIZ}"/releases/*/ \
#               | sed 's:/$::' | xargs -n1 basename \
#               | sort | grep -B1 "^${ATUAL}$" | head -1)"
#
#   if [ -z "$ANTERIOR" ] || [ "$ANTERIOR" = "$ATUAL" ]; then
#       echo "🔴 não há release anterior"
#       exit 1
#   fi

# ───────────────────────────────────────────────────────────────
# 2. Trocar o symlink (atômico) e recarregar
# ───────────────────────────────────────────────────────────────
# TODO:
#   ln -sfn "releases/${ANTERIOR}" "${RAIZ}/atual.novo"
#   mv -T "${RAIZ}/atual.novo" "${RAIZ}/atual"
#   sudo systemctl reload atlas

# ───────────────────────────────────────────────────────────────
# 3. Confirmar
# ───────────────────────────────────────────────────────────────
# TODO:
#   sleep 3
#   if curl -fsS --max-time 5 http://127.0.0.1:8000/saude >/dev/null; then
#       echo "✅ revertido para ${ANTERIOR}"
#   else
#       echo "🔴 nem o release anterior responde"
#       exit 1
#   fi
#
#   ⚠️ SE O RELEASE ANTERIOR TAMBÉM NÃO RESPONDER, o problema quase
#      nunca é o código. Investigue, nesta ordem:
#        1. o banco está no ar?
#        2. a migração do deploy quebrou o schema?
#        3. alguma variável de ambiente mudou?
#        4. o disco encheu?


# ═══════════════════════════════════════════════════════════════
#  🔴 O QUE ESTE SCRIPT **NÃO** DESFAZ
#
#     O ROLLBACK DE CÓDIGO É FÁCIL. O DE BANCO, NÃO.
#
#     Se o deploy problemático rodou uma migração que REMOVEU uma
#     coluna, voltar o código não devolve os dados. O `downgrade` do
#     Alembic recria a coluna — vazia.
#
#     🧭 É por isso que migração compatível importa tanto: com ela, o
#        rollback do código funciona sozinho, porque o schema novo
#        continua servindo o código velho.
#
#     💭 A regra que se aprende com susto: NUNCA destrua dado no mesmo
#        deploy que muda o código. Separe em dois, com dias de
#        distância, e um backup TESTADO no meio.
# ═══════════════════════════════════════════════════════════════
