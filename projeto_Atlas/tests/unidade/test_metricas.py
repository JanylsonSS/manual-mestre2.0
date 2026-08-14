"""Testes das métricas de negócio (M04).

🔴 Esta é a camada onde um bug não vira erro — vira NÚMERO ERRADO. E
   número errado não aparece em traceback nenhum.
"""

import pytest

# TODO: from atlas.metricas import ...


class TestFaturamento:
    # TODO: só pedidos PAGOS entram
    # TODO: cancelado e pendente NÃO entram
    #
    # 🔑 O teste que quase ninguém escreve e que pega o bug clássico:
    #    uma lista SÓ com cancelados deve dar faturamento ZERO —
    #    não deve estourar `ZeroDivisionError` no ticket médio.
    ...


class TestTicketMedio:
    # TODO: lista vazia → 0 ou None (decida, e teste a decisão)
    #
    # ⚠️  Não deixe "o que acontece com lista vazia" indefinido. É o
    #     caso que sempre chega em produção — no primeiro dia de um
    #     cliente novo, num filtro que não achou nada.
    ...


class TestCurvaABC:
    # TODO: os cortes 80/95 caem no lado certo
    # TODO: ⚠️ empate no limite — dois SKUs com o mesmo faturamento
    #       exatamente sobre o corte. Qual vai para A? A resposta
    #       precisa ser determinística, senão o relatório muda entre
    #       execuções sem nada ter mudado.
    ...


class TestMargem:
    # TODO: 🔴 margem do TOTAL, não média das margens.
    #
    #   Monte três produtos cujas duas contas dêem números
    #   DIFERENTES, e afirme o correto. Um teste com números que
    #   coincidem passa com as duas fórmulas e não protege nada.
    ...
