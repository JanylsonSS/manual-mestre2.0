#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Atlas — verificação de sanidade (Linux / macOS)
#
#  Roda o relatório contra os DOIS CSVs e reporta o resultado.
#  É o embrião do que vai virar a suíte de testes no Módulo 12
#  e o job de CI no Módulo 09.
#
#  Uso:  ./scripts/verificar.sh
#
#  Código de saída: 0 se tudo passou, 1 se algo falhou.
#  ⚠️ Esse código é o que o CI vai olhar. Acerte-o.
# ═══════════════════════════════════════════════════════════════

# TODO: set -uo pipefail
#
#   ⚠️ Repare: aqui NÃO usamos `set -e`. Este script PRECISA
#      continuar rodando mesmo quando um teste falha — senão ele
#      para no primeiro erro e você não vê os outros resultados.
#      Controlamos as falhas manualmente com a variável FALHAS.

# TODO: descobrir a raiz e fazer cd


FALHAS=0


# ── Função auxiliar ──────────────────────────────────────────
# TODO: escreva uma função `verificar` que:
#   - recebe uma descrição e um comando
#   - executa o comando capturando a saída
#   - imprime ✅ ou ❌ conforme o código de saída
#   - incrementa FALHAS quando falhar
#   - em caso de falha, mostra as últimas linhas da saída
#
#   Esqueleto:
#
#       verificar() {
#           local descricao="$1"
#           shift
#           echo "▶ $descricao"
#           if saida=$("$@" 2>&1); then
#               echo "  ✅ passou"
#           else
#               echo "  ❌ falhou"
#               echo "$saida" | tail -5 | sed 's/^/     /'
#               FALHAS=$((FALHAS + 1))
#           fi
#       }


echo "═══════════════════════════════════════════════"
echo "  Atlas — verificação"
echo "═══════════════════════════════════════════════"


# ── Teste 1: o ambiente existe ───────────────────────────────
# TODO: verificar que .venv existe e que .venv/bin/python roda


# ── Teste 2: os módulos importam ─────────────────────────────
# TODO: `.venv/bin/python -c "import sys; sys.path.insert(0,'src'); import atlas.cli"`
#   Se isso falha, há erro de sintaxe ou import circular.


# ── Teste 3: CSV limpo ───────────────────────────────────────
# TODO: rodar main.py com dados/brutos/vendas_jul2026.csv
#   Deve sair com código 0.


# ── Teste 4: CSV sujo ────────────────────────────────────────
# TODO: rodar main.py com dados/brutos/vendas_sujas.csv
#   ⚠️ Também deve sair com código 0!
#      O programa não pode QUEBRAR com dado sujo — ele deve
#      rejeitar as linhas ruins e seguir. Este é o teste que
#      valida o requisito de robustez do M01.


# ── Teste 5: arquivo inexistente ─────────────────────────────
# TODO: rodar com um caminho que não existe.
#   Deve sair com código != 0, mas SEM traceback do Python.
#   Uma mensagem amigável é o esperado.
#
#   💡 Este é um "teste negativo": você verifica que o programa
#      falha do jeito certo. São tão importantes quanto os testes
#      de sucesso.


# ── Teste 6: os arquivos de saída foram gerados ──────────────
# TODO: confirmar que existem:
#   saida/relatorio.txt, saida/relatorio.json, saida/rejeitados.csv


# ── Resumo ───────────────────────────────────────────────────
# TODO: imprimir o total de falhas e sair com o código correto:
#
#       if [ "$FALHAS" -eq 0 ]; then
#           echo "✅ Tudo passou"
#           exit 0
#       else
#           echo "❌ $FALHAS verificação(ões) falharam"
#           exit 1
#       fi
