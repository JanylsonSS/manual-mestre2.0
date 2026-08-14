"""Fixtures dos testes de UNIDADE.

🔑 A regra desta pasta, e é a única que importa aqui:

       nada nesta pasta toca disco, banco ou rede.

Se um teste seu precisar de `sessao`, ele não é de unidade — mova para
`integracao/`. Não "resolva" trazendo o banco para cá: o valor desta
pasta é ser rápida o bastante para rodar a cada `Ctrl+S`, e um único
teste com I/O contamina o tempo de todos.

💭 Como saber se vazou I/O sem perceber? Meça:

       pytest tests/unidade --durations=10

   Qualquer coisa acima de ~20 ms nesta pasta merece investigação.
"""

import pytest

# TODO: fixtures de DADOS, não de infraestrutura. Exemplos do que cabe:
#
#   @pytest.fixture
#   def pedido_simples(): ...       # um Pedido montado à mão
#
#   @pytest.fixture
#   def catalogo_minimo(): ...      # três produtos, sem banco
#
# 💡 Prefira FUNÇÕES CONSTRUTORAS a fixtures fixas:
#
#   @pytest.fixture
#   def montar_pedido():
#       def _montar(itens=1, status="pago", frete=0): ...
#       return _montar
#
#   Fixture fixa gera testes que dependem de valores mágicos ("por que
#   1234.50?"). Construtora deixa cada teste declarar exatamente a
#   condição que ele está testando — e o teste vira legível sozinho.
