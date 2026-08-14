"""Testes da camada de acesso (M03/M05).

SQL só se prova contra um banco. Estes testes existem porque uma
consulta pode estar sintaticamente perfeita e semanticamente errada.
"""

import pytest

# TODO: from atlas.repositorio import ...


class TestBusca:
    # TODO: buscar por id existente devolve o objeto
    # TODO: buscar por id inexistente devolve None (não levanta)
    # TODO: ⚠️ filtro com apóstrofo no texto ("D'Ávila") funciona —
    #       é o teste que prova que você usou parâmetro, não f-string
    ...


class TestGravacao:
    # TODO: gravar e reler devolve o mesmo valor
    # TODO: 🔴 violação de unicidade levanta a exceção de DOMÍNIO do
    #       Atlas, não `IntegrityError` do SQLAlchemy.
    #
    #   Se o erro do driver vaza para cima, a camada de acesso não
    #   está isolando nada — e trocar de banco vira mudança em todo
    #   o sistema.
    ...


@pytest.mark.integracao
class TestTransacao:
    """🔴 A propriedade que o M06 chamou de corretude."""

    # TODO: um pedido cujo TERCEIRO item falta em estoque não pode
    #       alterar o estoque dos dois primeiros.
    #
    #   Monte o cenário, tente, e afirme os três estoques INTACTOS.
    #
    # 🔑 Este é o teste mais valioso do arquivo. Ele não verifica uma
    #    função: verifica que a transação existe. E é o tipo de coisa
    #    que funciona por meses e quebra no dia em que alguém
    #    acrescenta um `commit()` no meio do laço.
    ...
