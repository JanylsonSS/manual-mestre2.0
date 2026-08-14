"""Testes de validação e normalização (M01/M04).

A fronteira do sistema: aqui é onde dado sujo vira dado confiável — ou
é rejeitado com motivo.
"""

import pytest

# TODO: from atlas.validacao import ...


class TestNormalizacao:
    # TODO: "  campinas  " → "Campinas"
    # TODO: "sp" → "SP"
    # TODO: "1.234,56" → Decimal("1234.56")   (formato pt-BR)
    ...


class TestRejeicao:
    """Toda rejeição precisa dizer POR QUÊ."""

    # TODO: quantidade zero ou negativa é rejeitada
    # TODO: status fora do vocabulário é rejeitado
    # TODO: data em formato inválido é rejeitada
    #
    # 🔑 E afirme a MENSAGEM, não só que rejeitou:
    #
    #     with pytest.raises(ValorInvalido, match="quantidade"):
    #         validar(linha)
    #
    #   Sem o `match`, o teste passa quando a função rejeita pelo
    #   motivo ERRADO — e você fica com uma mensagem de erro inútil
    #   em produção, achando que testou.
    ...
