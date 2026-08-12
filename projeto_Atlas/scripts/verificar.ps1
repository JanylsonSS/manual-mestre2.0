# ═══════════════════════════════════════════════════════════════
#  Atlas — verificação de sanidade (Windows)
#
#  Roda o relatório contra os DOIS CSVs e reporta o resultado.
#  Embrião da suíte de testes (M12) e do job de CI (M09).
#
#  Uso:  .\scripts\verificar.ps1
#
#  Código de saída: 0 se tudo passou, 1 se algo falhou.
# ═══════════════════════════════════════════════════════════════

# TODO: descobrir a raiz e fazer Set-Location
#
#   ⚠️ NÃO defina $ErrorActionPreference = "Stop" aqui.
#      Este script precisa continuar rodando mesmo quando um
#      teste falha — senão você só vê a primeira falha.


$Falhas = 0


# ── Função auxiliar ──────────────────────────────────────────
# TODO: escreva uma função `Verificar` que:
#   - recebe uma descrição e um scriptblock
#   - executa e verifica o resultado
#   - imprime OK ou FALHOU
#   - incrementa $script:Falhas quando falhar
#
#   Esqueleto:
#
#       function Verificar {
#           param([string]$Descricao, [scriptblock]$Acao)
#           Write-Host "> $Descricao"
#           try {
#               $saida = & $Acao 2>&1
#               if ($LASTEXITCODE -eq 0) {
#                   Write-Host "  OK" -ForegroundColor Green
#               } else {
#                   Write-Host "  FALHOU" -ForegroundColor Red
#                   $saida | Select-Object -Last 5 | ForEach-Object { "     $_" }
#                   $script:Falhas++
#               }
#           } catch {
#               Write-Host "  FALHOU: $_" -ForegroundColor Red
#               $script:Falhas++
#           }
#       }
#
#   💡 Repare no `$script:Falhas`. Sem esse escopo explícito,
#      a função criaria uma variável local e o contador nunca
#      seria incrementado. É a mesma armadilha do `global` em
#      Python que você viu na aula 01_04.


Write-Host "==============================================="
Write-Host "  Atlas - verificacao"
Write-Host "==============================================="


# ── Teste 1: o ambiente existe ───────────────────────────────
# TODO


# ── Teste 2: os módulos importam ─────────────────────────────
# TODO: & ".venv\Scripts\python.exe" -c "import sys; sys.path.insert(0,'src'); import atlas.cli"


# ── Teste 3: CSV limpo ───────────────────────────────────────
# TODO: deve sair com código 0


# ── Teste 4: CSV sujo ────────────────────────────────────────
# TODO: TAMBÉM deve sair com código 0 — o programa não pode
#   quebrar com dado sujo. Este é o teste do requisito de robustez.


# ── Teste 5: arquivo inexistente ─────────────────────────────
# TODO: deve falhar com mensagem amigável, sem traceback.
#   (Teste negativo: verifica que o programa falha do jeito certo.)


# ── Teste 6: arquivos de saída gerados ───────────────────────
# TODO: saida\relatorio.txt, saida\relatorio.json, saida\rejeitados.csv


# ── Resumo ───────────────────────────────────────────────────
# TODO:
#   if ($Falhas -eq 0) {
#       Write-Host "Tudo passou" -ForegroundColor Green
#       exit 0
#   } else {
#       Write-Host "$Falhas verificacao(oes) falharam" -ForegroundColor Red
#       exit 1
#   }
