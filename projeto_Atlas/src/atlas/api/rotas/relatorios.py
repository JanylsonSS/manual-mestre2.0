"""Relatórios — 🔒 restritos.

💭 O momento de fechar o círculo.

   O faturamento por categoria você já calculou três vezes:

     M01  em Python puro, lendo CSV          (atlas/metricas.py)
     M03  em SQL                             (dados/consultas/faturamento_por_categoria.sql)
     M05  com SQLAlchemy / agregação Mongo   (atlas/relatorios_sql.py)

   Agora ele ganha uma quarta apresentação: JSON via HTTP.

   🎯 OS QUATRO DEVEM DAR O MESMO NÚMERO. Se não derem, um tem bug — e
      descobrir qual é o exercício mais valioso deste módulo, porque é
      exatamente o que acontece quando a diretoria compara o relatório
      do sistema com a planilha do financeiro.

🔒 Relatório expõe margem, custo e concentração de clientes. Toda rota
   aqui exige `admin`.
"""

from fastapi import APIRouter

# TODO: importar dependências e esquemas

roteador = APIRouter(prefix="/relatorios", tags=["Relatórios"])


# ═══════════════════════════════════════════════════════════════════════
#  GET /relatorios/faturamento  — 🔒 admin
# ═══════════════════════════════════════════════════════════════════════
#
# Parâmetros: `inicio` e `fim` (datas), `agrupar_por` (categoria | canal
# | cidade | mes).
#
# 🔴 `agrupar_por` é um IDENTIFICADOR vindo do usuário. Lista branca,
#    obrigatoriamente — a mesma regra da ordenação. Um `GROUP BY {campo}`
#    com valor cru é injeção de SQL de manual.
#
# ⚠️ Exija a faixa de datas, ou imponha um padrão curto (últimos 30
#    dias). Um relatório sem filtro varre a tabela inteira — e quando a
#    Aurora tiver 5 anos de histórico, essa rota vai derrubar o banco.
#
# 💡 Reaproveite `atlas/relatorios_sql.py`. A rota NÃO escreve SQL; ela
#    chama o que já existe. Se você se pegar escrevendo `select(...)`
#    aqui, a camada está errada.
#
# TODO: implementar `faturamento`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /relatorios/curva-abc  — 🔒 admin
# ═══════════════════════════════════════════════════════════════════════
#
# A curva ABC do M01: A até 80% do faturamento acumulado, B até 95%,
# C o resto. Os cortes já estão em `atlas/config.py` — use as constantes,
# não os números soltos.
#
# TODO: implementar.


# ═══════════════════════════════════════════════════════════════════════
#  GET /relatorios/alerta-estoque  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
# Produtos abaixo do ponto de reposição. Esta o operador de compras
# precisa ver — é o insumo do trabalho dele.
#
# 💡 Repare que o nível de acesso segue a NECESSIDADE, não a hierarquia
#    do organograma. Estoque baixo é operacional; margem é estratégico.
#
# TODO: implementar.


# ═══════════════════════════════════════════════════════════════════════
#  💭 Sobre exportação (para o M07)
# ═══════════════════════════════════════════════════════════════════════
#
# A diretoria vai pedir "manda em Excel". Duas armadilhas:
#
# 1. Gerar o arquivo DENTRO da requisição bloqueia um worker por
#    segundos ou minutos. Com 4 workers e 5 diretores curiosos, a API
#    inteira para.
#
#    O padrão correto: a rota devolve 202 Accepted com um id de tarefa,
#    um worker gera em segundo plano, e o cliente consulta o status.
#    Isso é assunto do M07 (filas) — mas o desenho começa aqui.
#
# 2. CSV para Excel em português precisa de `;` como separador e BOM
#    UTF-8, senão abre tudo numa coluna só com acentuação quebrada.
#    Você já resolveu isso no M01 — `DELIMITADOR_CSV_EXCEL_BR` existe
#    em `atlas/config.py` exatamente por causa disso.
