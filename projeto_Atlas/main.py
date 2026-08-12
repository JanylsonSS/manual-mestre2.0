"""Atlas — ponto de entrada da CLI.

Uso:
    python main.py                                  # usa o caminho padrão
    python main.py dados/brutos/vendas_jul2026.csv  # caminho explícito

Este arquivo é propositalmente MINÚSCULO. A única responsabilidade dele é
resolver o import path e delegar para `src/atlas/cli.py`.

Regra geral: quanto menos código no ponto de entrada, melhor. Ele não deve
conter lógica de negócio — se você começar a calcular algo aqui, pare e
mova para o módulo correto.
"""

import sys
from pathlib import Path

# Coloca a pasta 'src' no caminho de import para que 'from atlas import ...'
# funcione sem precisar instalar o pacote. No Módulo 04 substituímos este
# truque por uma instalação editável (`pip install -e .`).
sys.path.insert(0, str(Path(__file__).parent / "src"))

from atlas.cli import main  # noqa: E402

if __name__ == "__main__":
    # TODO: chamar main() passando o argumento de linha de comando, se houver.
    #       Dica: sys.argv[0] é o nome do script; os argumentos começam em [1].
    #       Se não houver argumento, passe None e deixe a CLI usar o padrão.
    raise SystemExit(main())
