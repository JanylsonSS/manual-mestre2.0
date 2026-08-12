"""Configuração central do Atlas.

Todas as constantes e caminhos do projeto vivem aqui — em um lugar só.

**Por que centralizar?** Porque quando a regra mudar (e ela vai mudar), você
quer alterar UMA linha, não caçar o número 0.18 espalhado em seis arquivos.

Convenção: constantes em MAIÚSCULAS_COM_UNDERSCORE.

⚠️ Este módulo não deve importar nenhum outro módulo do Atlas. Ele é a base
   da pirâmide — todos importam dele, ele não importa de ninguém.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
# TODO: definir DIR_RAIZ apontando para a raiz do projeto.
#       Dica: Path(__file__) é este arquivo (src/atlas/config.py).
#       Você precisa subir 3 níveis com .parent para chegar em projeto_Atlas/.

DIR_RAIZ: Path = Path(__file__).parent.parent.parent # TODO

# TODO: derivar os demais diretórios a partir de DIR_RAIZ usando o operador /
#       DIR_DADOS           -> DIR_RAIZ / "dados"
#       DIR_DADOS_BRUTOS    -> DIR_DADOS / "brutos"
#       DIR_DADOS_PROCESSADOS
#       DIR_SAIDA

DIR_DADOS: Path = DIR_RAIZ / "dados"  # TODO
DIR_DADOS_BRUTOS: Path = DIR_DADOS / "brutos" # TODO
DIR_DADOS_PROCESSADOS: Path = DIR_DADOS / "processados"  # TODO
DIR_SAIDA: Path = DIR_RAIZ / "saida"  # TODO

# TODO: definir o arquivo de entrada padrão (usado quando o usuário não passa
#       nenhum argumento na linha de comando).
ARQUIVO_PADRAO: Path = DIR_DADOS_BRUTOS / "padrao.csv"  # TODO

# TODO: definir os caminhos dos três arquivos de saída:
#       SAIDA_RELATORIO_TXT, SAIDA_RELATORIO_JSON, SAIDA_REJEITADOS_CSV

SAIDA_RELATORIO_TXT: Path = DIR_SAIDA / "relatorio.txt"  # TODO
SAIDA_RELATORIO_JSON: Path = DIR_SAIDA / "relatorio.json"  # TODO
SAIDA_REJEITADOS_CSV: Path = DIR_SAIDA / "relatorio.csv"  # TODO


# ---------------------------------------------------------------------------
# Formato dos arquivos
# ---------------------------------------------------------------------------
ENCODING = "utf-8"
DELIMITADOR_CSV = ","
DELIMITADOR_CSV_EXCEL_BR = ";"  # o Excel em PT-BR espera ponto e vírgula

# TODO: listar as colunas que o CSV de entrada DEVE ter.
#       Serve para validar o arquivo antes de processar linha a linha —
#       melhor falhar cedo com "falta a coluna 'status'" do que estourar
#       um KeyError na linha 4.782.
COLUNAS_OBRIGATORIAS: tuple[str, ...] = ()  # TODO


# ---------------------------------------------------------------------------
# Domínio — valores válidos
# ---------------------------------------------------------------------------
# TODO: definir os conjuntos de valores aceitos. Use set (busca O(1)).
#       STATUS_VALIDOS -> pago, pendente, cancelado
#       CANAIS_VALIDOS -> site, app, marketplace

STATUS_VALIDOS: set[str] = set()  # TODO
CANAIS_VALIDOS: set[str] = set()  # TODO

# TODO: qual status conta como faturamento? (a diretora reclamou que
#       cancelados estavam entrando na conta — essa constante é a resposta)
STATUS_FATURAVEL: str = ...  # TODO

STATUS_CANCELADO = "cancelado"


# ---------------------------------------------------------------------------
# Regras de negócio
# ---------------------------------------------------------------------------
# Curva ABC: A = até 80% do faturamento acumulado, B = até 95%, C = o resto.
CORTE_CURVA_A = 0.80
CORTE_CURVA_B = 0.95

# Quantos itens exibir nos rankings "top N"
TOP_N_PRODUTOS = 5
TOP_N_CLIENTES = 5

# Formato de data esperado no CSV
FORMATO_DATA = "%Y-%m-%d"


# ---------------------------------------------------------------------------
# Banco de dados (Módulo 03)
# ---------------------------------------------------------------------------
# TODO: ARQUIVO_BANCO -> DIR_DADOS / "atlas.db"
#       ARQUIVO_SCHEMA -> DIR_DADOS / "schema.sql"
#       ARQUIVO_INDICES -> DIR_DADOS / "indices.sql"
#       DIR_CONSULTAS -> DIR_DADOS / "consultas"

ARQUIVO_BANCO: Path = ...  # TODO
ARQUIVO_SCHEMA: Path = ...  # TODO
ARQUIVO_INDICES: Path = ...  # TODO
DIR_CONSULTAS: Path = ...  # TODO

# PRAGMAs aplicados em TODA conexão nova.
# 🔴 foreign_keys=ON é obrigatório: o SQLite vem com FK desligada por
#    compatibilidade histórica, e sem isso suas FKs não garantem nada.
# 💡 journal_mode=WAL faz leitores não bloquearem o escritor.
PRAGMAS_CONEXAO: tuple[str, ...] = (
    "PRAGMA foreign_keys = ON",
    "PRAGMA journal_mode = WAL",
)

# 🔴 LISTA BRANCA de tabelas.
#    Nome de tabela NÃO pode ser parametrizado com `?` — o placeholder só
#    funciona para VALORES. Se alguma função precisar montar o nome na
#    string, ela DEVE validar contra esta lista antes.
TABELAS: tuple[str, ...] = (
    "categorias",
    "produtos",
    "clientes",
    "pedidos",
    "itens_pedido",
)


# ---------------------------------------------------------------------------
# Apresentação
# ---------------------------------------------------------------------------
LARGURA_RELATORIO = 78
SIMBOLO_MOEDA = "R$"

# TODO (opcional): adicione aqui o nome da empresa e um título para o
#       cabeçalho do relatório, em vez de deixá-los soltos em relatorios.py.


if __name__ == "__main__":
    # Rode `python src/atlas/config.py` para conferir se os caminhos batem
    # com a estrutura real de pastas do seu projeto.
    # TODO: imprimir DIR_RAIZ, ARQUIVO_PADRAO e se ARQUIVO_PADRAO existe.
    pass
