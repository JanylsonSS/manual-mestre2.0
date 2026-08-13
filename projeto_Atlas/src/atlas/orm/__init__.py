"""Camada de persistência relacional — SQLAlchemy 2.0.

Contém os modelos mapeados, a sessão e o repositório SQL.

⚠️ Nada fora desta pasta deve importar `sqlalchemy` diretamente.
   Se `servicos.py` precisar de um `select()`, houve vazamento de
   responsabilidade — a camada de persistência não está isolada.
"""

# TODO: reexportar Base e os modelos, para o resto do projeto poder
#       fazer `from atlas.orm import Pedido` em vez de
#       `from atlas.orm.modelos import Pedido`.
#
#       ⚠️ Cuidado com import circular: só reexporte DEPOIS que os
#          módulos estiverem estáveis.
