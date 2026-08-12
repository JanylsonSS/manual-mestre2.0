#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Atlas — setup do ambiente de desenvolvimento (Linux / macOS)
#
#  Uso:  ./scripts/setup.sh
#
#  Deve ser IDEMPOTENTE: rodar duas vezes não pode quebrar nada.
# ═══════════════════════════════════════════════════════════════

# TODO: ativar o modo estrito do bash.
#   set -e           -> aborta no primeiro comando que falhar
#   set -u           -> erro ao usar variável não definida
#   set -o pipefail  -> falha se QUALQUER comando de um pipe falhar
#
#   Sem isso, o script continua alegremente depois de um erro e
#   você descobre o problema três etapas depois. Escreva:
#
#       set -euo pipefail


# ── Descobrir a raiz do projeto ──────────────────────────────
# TODO: o script precisa funcionar sendo chamado de QUALQUER pasta.
#   Descubra a raiz a partir do caminho do próprio script:
#
#       RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
#       cd "$RAIZ"


# ── Cores (opcional, mas ajuda muito a ler a saída) ──────────
VERDE='\033[0;32m'
AMARELO='\033[1;33m'
VERMELHO='\033[0;31m'
SEM_COR='\033[0m'

info()    { echo -e "${VERDE}▶${SEM_COR} $1"; }
aviso()   { echo -e "${AMARELO}⚠${SEM_COR}  $1"; }
erro()    { echo -e "${VERMELHO}✖${SEM_COR} $1" >&2; }


echo "═══════════════════════════════════════════════"
echo "  Atlas — preparação do ambiente"
echo "═══════════════════════════════════════════════"


# ── 1. Verificar o Python ────────────────────────────────────
# TODO: confirmar que existe python3 e que a versão é >= 3.10.
#   - Use `command -v python3` para checar existência
#   - Use `python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)"`
#     para checar a versão
#   - Se falhar, imprima uma mensagem útil (link de download) e
#     `exit 1`


# ── 2. Criar o ambiente virtual ──────────────────────────────
# TODO: criar .venv se ainda não existir.
#   - `if [ ! -d ".venv" ]; then ... fi`
#   - `python3 -m venv .venv`
#   - Se já existir, avise que está reutilizando (idempotência!)


# ── 3. Atualizar o pip ───────────────────────────────────────
# TODO: `.venv/bin/python -m pip install --upgrade pip --quiet`
#
#   💡 Repare: chamamos o python DE DENTRO do venv diretamente,
#      em vez de "ativar" o venv. Ativar dentro de um script não
#      afeta o shell do usuário — e chamar o binário direto é
#      mais confiável.


# ── 4. Instalar dependências ─────────────────────────────────
# TODO: se requirements.txt existir, instalar:
#   `.venv/bin/pip install -r requirements.txt --quiet`
#
#   No M01/M02 o arquivo só tem comentários — não instala nada.
#   Isso é esperado. O script deve lidar bem com isso.


# ── 5. Criar as pastas de saída ──────────────────────────────
# TODO: `mkdir -p saida dados/processados`
#   O -p não reclama se já existir (idempotência de novo).


# ── 6. Criar o .env a partir do exemplo ──────────────────────
# TODO: se .env NÃO existir e .env.example existir, copiar.
#   Nunca sobrescreva um .env existente — ele tem os segredos reais.


# ── 7. Resumo final ──────────────────────────────────────────
# TODO: imprimir as instruções de ativação para o usuário:
#
#       Ambiente pronto. Para ativar:
#           source .venv/bin/activate
#       Para rodar o relatório:
#           ./scripts/rodar.sh


# TODO: terminar com `exit 0` explícito.
