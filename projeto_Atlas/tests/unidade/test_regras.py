"""Testes do motor de regras (M04).

Por que unidade: regra de preço é função pura. Entra pedido, sai
número. Nenhum I/O — e é a camada onde um erro custa dinheiro.
"""

import pytest

# TODO: from atlas.regras import ...


class TestDesconto:
    """🔴 Os LIMITES. É onde mora o bug."""

    # TODO: teste EXATAMENTE no limite, e nos dois vizinhos.
    #
    #   Se a regra é "acima de R$ 1.000 ganha 10%", teste com
    #   999.99, 1000.00 e 1000.01.
    #
    #   🔑 O teste com 1000.00 é o que pega a confusão entre `>` e
    #      `>=` — o erro de uma letra que o teste de mutação vai
    #      procurar, e que nenhum teste de "caso típico" encontra.

    # TODO: desconto nunca deixa o total negativo
    # TODO: descontos acumulados não passam do teto
    # TODO: pedido cancelado não recebe desconto


class TestFrete:
    # TODO: frete grátis a partir do valor definido
    # TODO: frete de item único vs. vários
    # TODO: ⚠️ frete negativo deve levantar exceção, não ser aceito
    ...


@pytest.mark.parametrize("valor,esperado", [
    # TODO: (entrada, saída) — a tabela de casos.
    #
    # 💡 `parametrize` transforma 8 testes quase iguais em 1 teste e 8
    #    linhas de dados. E o pytest reporta cada caso separadamente:
    #    você vê QUAL entrada falhou, não só "o teste falhou".
    #
    # ⚠️  Não caia na tentação de calcular o esperado com a mesma
    #     fórmula do código:
    #
    #         (100, 100 * TAXA)      # ❌ testa que a fórmula é ela mesma
    #         (100, 118.00)          # ✅ número conferido à mão
    #
    #     O primeiro passa mesmo com a fórmula errada.
])
def test_tabela(valor, esperado):
    # TODO: implemente
    ...
