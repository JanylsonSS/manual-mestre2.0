#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Sobe a API do Atlas em modo desenvolvimento.
#
#      ./scripts/api.sh
#      ./scripts/api.sh 8001          # outra porta
#
#  ⚠️ --reload é SÓ para desenvolvimento. Ele vigia o sistema de
#     arquivos e reinicia o processo a cada salvamento. Em produção
#     isso é desperdício e risco — o modo de produção é assunto do M09.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail

cd "$(dirname "$0")/.."

PORTA="${1:-8000}"

# 🔴 Falha cedo e com mensagem clara em vez de subir quebrado.
if [ ! -f .env ]; then
  echo "🔴 .env não encontrado."
  echo "   cp .env.example .env"
  echo "   e depois gere a chave:"
  echo '   python -c "import secrets; print(secrets.token_urlsafe(48))"'
  exit 1
fi

if grep -q "^ATLAS_SECRET_KEY=gere-uma-chave" .env 2>/dev/null; then
  echo "🔴 ATLAS_SECRET_KEY ainda é o valor de exemplo."
  echo '   python -c "import secrets; print(secrets.token_urlsafe(48))"'
  exit 1
fi

echo "▶️  http://127.0.0.1:${PORTA}/docs"
echo

# --factory: chama criar_app() em vez de usar um `app` de módulo.
exec uvicorn "atlas.api.aplicacao:criar_app" \
  --factory --reload --port "${PORTA}"
