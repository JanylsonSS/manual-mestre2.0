"""Testes da camada de serviço (M04/M05).

Onde as regras encontram os dados. Se `servicos.py` precisar mudar
muito para estes testes passarem, o desenho tem vazamento.
"""

import pytest

# TODO: from atlas.servicos import ...


class TestRelatorio:
    # TODO: 🔧 o critério de aceitação que atravessa o manual inteiro:
    #
    #   os números do relatório batem com os do Módulo 01.
    #
    #   Carregue o mesmo CSV, rode pela via nova, e compare com os
    #   valores conferidos à mão. É o teste que provou o M03, o M04 e
    #   o M05 — e continua provando cada refatoração futura.
    ...


class TestCriarPedido:
    # TODO: pedido válido baixa o estoque na medida certa
    # TODO: estoque insuficiente é recusado com mensagem clara
    # TODO: ⚠️ pedido sem itens — decida o comportamento e teste-o
    ...
