"""Relatórios a partir do banco — carrega e executa arquivos .sql.

**A mudança de mentalidade do Módulo 03:**

No M01, a lógica de agregação era Python: laços, `defaultdict`,
somas manuais. Agora ela é **SQL**, e o Python só orquestra e formata.

| Antes (M01) | Agora (M03) |
|-------------|-------------|
| ~40 linhas de laço para agrupar por cidade | 12 linhas de SQL |
| Você diz COMO percorrer | Você diz O QUE quer |
| Lê o arquivo inteiro para a memória | O banco processa e devolve o resultado |
| Nova dimensão = novo laço | Nova dimensão = mais uma coluna no GROUP BY |

⚠️ **Este módulo NÃO contém SQL.** As consultas vivem em
   `dados/consultas/*.sql`. Aqui só ficam o carregamento, a execução
   e a formatação.

   Motivo: o analista de negócio consegue abrir um `.sql`, entender e
   ajustar. Ele não vai abrir um `.py`.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from atlas import config, formatacao, repositorio
from atlas.excecoes import AtlasError


# ═══════════════════════════════════════════════════════════════
#  Catálogo de relatórios
# ═══════════════════════════════════════════════════════════════
# TODO: mapeie o nome do relatório (usado na CLI) para o arquivo .sql
#       e uma descrição. Algo como:
#
#   RELATORIOS = {
#       "faturamento_por_cidade": {
#           "arquivo": "faturamento_por_cidade.sql",
#           "titulo": "Faturamento por praça",
#           "descricao": "Ranking de cidades com share do total",
#       },
#       ...
#   }
#
#   💡 Ter um catálogo explícito permite:
#      - `python main.py relatorio --listar` mostrar as opções
#      - validar o nome vindo da CLI contra uma lista branca
#        (nada de aceitar um caminho arbitrário do usuário)

RELATORIOS: dict[str, dict] = {}  # TODO


# ═══════════════════════════════════════════════════════════════
#  Execução
# ═══════════════════════════════════════════════════════════════


def listar_relatorios() -> list[str]:
    """Nomes dos relatórios disponíveis."""
    # TODO: implementar
    raise NotImplementedError


def carregar_sql(nome: str) -> str:
    """Lê o arquivo .sql do relatório.

    Args:
        nome: Chave em RELATORIOS.

    Raises:
        AtlasError: se o nome não estiver no catálogo, ou o arquivo
            não existir.

    🔴 SEGURANÇA: valide `nome` contra RELATORIOS antes de montar
       qualquer caminho. Aceitar `nome` direto do usuário e fazer
       `DIR_CONSULTAS / nome` permite path traversal:
           ...
       `../../../etc/passwd` sai da pasta.
    """
    # TODO: implementar
    raise NotImplementedError


def executar_relatorio(conexao: sqlite3.Connection, nome: str,
                       parametros: dict | None = None) -> list[dict]:
    """Executa um relatório e devolve as linhas.

    Args:
        conexao: Conexão aberta.
        nome: Chave em RELATORIOS.
        parametros: Valores para placeholders nomeados na consulta
            (ex.: {"mes": "2026-07"}).

    Returns:
        Lista de dicts.

    💡 Consultas com filtro de período devem usar `:data_inicio` e
       `:data_fim` em vez de datas fixas. Assim o mesmo .sql serve
       para qualquer período.
    """
    # TODO: implementar
    raise NotImplementedError


def executar_todos(conexao: sqlite3.Connection,
                   parametros: dict | None = None) -> dict[str, list[dict]]:
    """Executa todos os relatórios do catálogo.

    ⚠️ Se um falhar, os outros devem continuar. Colete os erros e
       reporte ao final, em vez de abortar no primeiro.
    """
    # TODO: implementar
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Formatação
# ═══════════════════════════════════════════════════════════════


def formatar_tabela(linhas: list[dict], titulo: str = "",
                    largura_max: int = 100) -> str:
    """Formata o resultado como tabela alinhada em texto.

    Regras de apresentação:
        - Texto alinhado à esquerda, números à direita
        - Valores monetários com `formatacao.formatar_brl`
        - Colunas terminadas em `_pct` como percentual
        - `None` vira "—", não "None"
        - Larguras calculadas a partir do conteúdo

    💡 Você já escreveu algo parecido em `formatacao.linha_tabela`
       no M01. Reaproveite em vez de reimplementar.

    💡 Como saber quais colunas são monetárias? Uma convenção de
       nomes resolve: colunas terminadas em `_reais`, `faturamento`,
       `receita`, `margem` são dinheiro. Documente a convenção.
    """
    # TODO: implementar
    raise NotImplementedError


def formatar_json(linhas: list[dict]) -> dict:
    """Estrutura o resultado para saída JSON.

    ⚠️ Arredonde valores monetários para 2 casas AQUI. Não adianta
       o JSON carregar 2599.9000000000005.
    """
    # TODO: implementar
    raise NotImplementedError


def exportar_csv(linhas: list[dict], caminho: Path) -> None:
    """Grava o resultado em CSV para abrir no Excel.

    💡 Use config.DELIMITADOR_CSV_EXCEL_BR (";") — o Excel em
       português espera ponto e vírgula, porque a vírgula é o
       separador decimal.
    """
    # TODO: implementar
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Comparação com o Módulo 01
# ═══════════════════════════════════════════════════════════════


def comparar_com_m01(conexao: sqlite3.Connection, caminho_csv: Path) -> str:
    """Roda o relatório pelos dois caminhos e compara.

    Este é o entregável da Parte F do projeto: prove que a migração
    para SQL preservou os números **e** meça a diferença de esforço.

    Deve reportar, para "faturamento por cidade":
        - Resultado via CSV (métricas.py do M01)
        - Resultado via SQL (esta camada)
        - Diferença linha a linha
        - Tempo de execução de cada um
        - Linhas de código de cada implementação

    💭 Espere que o SQL seja mais LENTO em volume pequeno — abrir
       conexão e planejar a consulta tem custo fixo. A vantagem
       aparece quando o volume cresce e quando você precisa de uma
       dimensão nova. Reporte isso com honestidade em vez de forçar
       um número que favoreça o SQL.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: listar os relatórios disponíveis e executar um deles.
    pass
