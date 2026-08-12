"""Pacote Atlas — sistema central da Aurora Comércio.

A presença deste arquivo transforma a pasta `atlas/` em um **pacote** Python,
permitindo `from atlas.metricas import calcular_totais`.

Ele costuma ficar vazio (ou quase). Aqui usamos apenas para registrar a versão
e o nome do pacote — informação útil em logs e no cabeçalho dos relatórios.
"""

__version__ = "0.4.0"
__nome__ = "Atlas"

# ⚠️ A partir do M04 esta versão precisa bater com a de `pyproject.toml`.
#    Duas fontes de verdade para a mesma informação sempre divergem.
#
# TODO (desafio): elimine a duplicação lendo a versão dos metadados do
#    pacote instalado:
#
#        from importlib.metadata import version
#        __version__ = version("atlas")
#
#    Isso só funciona após `pip install -e .` — trate o ImportError para
#    o caso de alguém rodar sem instalar.

# TODO (opcional): se você quiser permitir `from atlas import calcular_totais`
#       em vez de `from atlas.metricas import calcular_totais`, reexporte os
#       nomes públicos aqui e liste-os em __all__.
#       Faça isso APENAS depois que os módulos estiverem funcionando —
#       imports no __init__.py criam dependências circulares com facilidade.
