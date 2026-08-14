"""Testes do pipeline analítico (M10).

Três propriedades, e as três já falharam com alguém.
"""

import pytest

# TODO: from atlas.dados import ...


@pytest.mark.integracao
class TestIdempotencia:
    """🔴 Rodar 2× o mesmo dia produz o MESMO ouro."""

    # TODO: rode duas vezes com a mesma data e compare os HASHES dos
    #       arquivos do ouro.
    #
    # 🔑 Exija que existam arquivos antes de comparar:
    #
    #       assert digitais_1, "o pipeline não produziu nada"
    #       assert digitais_1 == digitais_2
    #
    #   Sem a primeira linha, `{} == {}` é True e o teste APROVA um
    #   pipeline que não gerou arquivo nenhum. Foi exatamente esse o
    #   bug da bateria de aceitação do M10.
    ...


@pytest.mark.integracao
class TestPortaoQualidade:
    """Um portão que você nunca viu reprovar não é um portão."""

    # TODO: um teste POR VERIFICAÇÃO, cada um violando só a sua regra:
    #
    #   lote vazio             → reprova (completude)
    #   chave duplicada        → reprova (unicidade)
    #   coluna obrigatória nula→ reprova (obrigatórias)
    #   preço zero             → reprova (faixa)
    #   custo > preço          → reprova (coerência)
    #   volume 5% do histórico → reprova (volume)
    #
    # TODO: e um teste com lote BOM afirmando que TUDO passa.
    #
    #   ⚠️ Sem ele, seis verificações que reprovam qualquer coisa
    #      passariam nos seis testes acima com nota máxima.

    # TODO: 🔴 reprovar NÃO apaga o ouro anterior.
    #       Grave um ouro, force a reprovação, e afirme que ele
    #       continua lá. Dado de ontem é melhor que número errado
    #       de hoje.
    ...


@pytest.mark.integracao
class TestQuarentena:
    # TODO: linha inválida vai para a quarentena e o lote SEGUE
    # TODO: o arquivo de quarentena diz qual campo e qual valor
    ...
