"""
Contratos — o que é um dado válido, escrito em Pydantic.
═══════════════════════════════════════════════════════════════════════

Você já usou Pydantic no M06, na API, para validar o que o CLIENTE
manda. Aqui é o mesmo Pydantic para validar o que a ORIGEM manda.

A diferença é o que fazer quando falha:

    Na API          →  400, e o cliente conserta e reenvia
    No pipeline     →  ❓ ninguém está lá para reenviar

Essa pergunta tem uma resposta específica, e ela é a ideia mais
importante deste arquivo:

    🔴 Uma linha inválida NÃO derruba o lote e NÃO é descartada.
       Ela vai para a QUARENTENA, com o motivo, e o lote segue.

Por quê? Porque as duas alternativas são piores:

    derrubar o lote   →  1 linha ruim em 2 milhões e você fica sem
                         relatório; e o pipeline vira o "boy que
                         chora lobo" que todo mundo aprende a ignorar

    descartar a linha →  o número sai errado e ninguém sabe; o
                         faturamento perde R$ 40 mil e a divergência
                         aparece na auditoria, seis meses depois

A quarentena é a única opção que preserva as duas coisas: o relatório
sai HOJE, e o dado ruim continua EXISTINDO para ser investigado.

⚠️  ESQUELETO. Assinaturas e TODOs prontos; os corpos são seus.
"""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any

# TODO: from pydantic import BaseModel, Field, field_validator, model_validator


# ═══════════════════════════════════════════════════════════════════════
#  Vocabulário fechado
# ═══════════════════════════════════════════════════════════════════════

class StatusPedido(str, Enum):
    """Os status que existem. Qualquer outro é dado inválido."""

    # TODO: PAGO / PENDENTE / CANCELADO / DEVOLVIDO
    #
    # 💭 Por que Enum e não `str`? Porque o dia em que a origem mandar
    #    "PAGO ", "pago" ou "paid", você quer descobrir na validação —
    #    não no relatório, quando o faturamento de uma categoria
    #    inteira aparecer como zero porque o filtro `== "pago"` não
    #    casou com nada.
    ...


class Canal(str, Enum):
    """Canais de venda."""
    # TODO: SITE / APP / MARKETPLACE
    ...


# ═══════════════════════════════════════════════════════════════════════
#  O contrato do pedido
# ═══════════════════════════════════════════════════════════════════════

class PedidoBruto:  # TODO: herde de BaseModel
    """Uma linha de pedido, como deve ser depois de limpa.

    Campos esperados:

        pedido_id        int, > 0, único no lote
        data             datetime COM fuso
        sku              str, formato XX-9999
        quantidade       int, 1..999
        preco_unitario   Decimal, > 0
        custo_unitario   Decimal, >= 0
        frete            Decimal, >= 0
        status           StatusPedido
        canal            Canal
        cidade           str, não vazia
    """

    # TODO: declare os campos com os tipos e as restrições acima.
    #
    # 🔴 Use Decimal para dinheiro, não float.
    #
    #    >>> 0.1 + 0.2
    #    0.30000000000000004
    #
    #    Com float, somar 3 milhões de linhas acumula erro e o
    #    fechamento não bate com o financeiro por centavos que ninguém
    #    consegue explicar. Decimal("0.1") + Decimal("0.2") é exato.
    #
    #    ⚠️  Parquet não tem Decimal nativo em toda ferramenta. Grave
    #        como int de centavos (`preco_centavos: int`) OU declare a
    #        precisão explicitamente no schema Arrow. Decida agora e
    #        escreva a decisão em docs/PIPELINE.md.

    # TODO: @field_validator("data")
    #       Rejeite datetime sem tzinfo. Um datetime "ingênuo" no lago
    #       é uma bomba-relógio: em algum momento alguém compara com
    #       um datetime com fuso e recebe TypeError — ou pior, alguém
    #       assume UTC onde era Brasília e o relatório diário fica com
    #       3 horas de pedidos no dia errado.

    # TODO: @field_validator("sku", mode="before")
    #       Normalize ANTES de validar o formato: .strip().upper()
    #
    # 🔴 O `mode="before"` é obrigatório aqui. Sem ele, o
    #    `pattern=` do Field roda primeiro, rejeita " nb-1001 " por
    #    causa dos espaços, e o seu normalizador nunca é chamado.
    #    (É exatamente a armadilha do M06 · Aula 02.)

    # TODO: @model_validator(mode="after")
    #       Coerência entre campos, que nenhum campo sozinho pega:
    #
    #         custo_unitario <= preco_unitario
    #
    #       Custo maior que preço não é impossível (liquidação), mas é
    #       raro o bastante para merecer quarentena e um olhar humano.
    #       Se a Aurora confirmar que é normal, mude para aviso — e
    #       escreva a decisão em docs/METRICAS.md.
    ...


# ═══════════════════════════════════════════════════════════════════════
#  Quarentena
# ═══════════════════════════════════════════════════════════════════════

class LinhaRejeitada:  # TODO: herde de BaseModel
    """Uma linha que não passou, com contexto suficiente para consertar.

    🔑 O critério: quem abrir a quarentena daqui a três semanas precisa
       resolver o caso SEM abrir o código e SEM rodar nada.
    """

    # TODO: campos
    #         linha_original  dict   — o dado cru, inteiro
    #         erros           list   — campo + mensagem + valor recebido
    #         fonte           str
    #         lote_id         str
    #         rejeitada_em    datetime
    #
    # ⚠️  `linha_original` pode conter dado pessoal (nome, e-mail,
    #     CPF). A quarentena é um arquivo em disco que muita gente lê.
    #     Antes de gravar, mascare o que for pessoal — ou grave só as
    #     colunas necessárias para o diagnóstico. LGPD, art. 6º:
    #     necessidade. Decida e documente.
    ...


def validar_lote(linhas: list[dict], contrato: type) -> tuple[list, list]:
    """Valida linha a linha. Devolve (aprovadas, rejeitadas).

    🔴 NÃO use `try/except` em volta do lote inteiro. Isso transforma
       "uma linha ruim" em "nenhum dado hoje" — e é o oposto do que
       este arquivo defende. O `try` fica DENTRO do laço.
    """
    # TODO:
    #   for i, bruta in enumerate(linhas):
    #       try:
    #           aprovadas.append(contrato(**bruta))
    #       except ValidationError as e:
    #           rejeitadas.append(LinhaRejeitada(
    #               linha_original=bruta,
    #               erros=[{"campo": ..., "msg": ..., "valor": ...}
    #                      for erro in e.errors()],
    #               ...))
    #
    # ⚠️  Em 2 milhões de linhas, um laço Python com Pydantic leva
    #     minutos. Duas saídas honestas:
    #
    #       a) valide o lote com operações vetorizadas de pandas
    #          (máscaras booleanas) e use Pydantic só para o que
    #          sobrar suspeito;
    #       b) valide uma AMOSTRA com Pydantic e o resto com máscaras.
    #
    #     Meça antes de otimizar. Se 2 min por noite é aceitável, o
    #     laço simples é a melhor escolha — código claro vale mais que
    #     um minuto às 3h da manhã.
    raise NotImplementedError


def gravar_quarentena(rejeitadas: list, lote_id: str) -> Any:
    """Grava as rejeitadas em `dados/lago/quarentena/`, particionado por dia."""
    # TODO: um parquet (ou JSONL) por lote. JSONL é mais fácil de
    #       inspecionar com `grep` às 3h da manhã; parquet é mais fácil
    #       de agregar depois. Escolha e justifique em docs/PIPELINE.md.
    raise NotImplementedError


def resumir_quarentena(rejeitadas: list) -> dict[str, int]:
    """Conta rejeições por motivo. É isto que vai para o log e o alerta.

    💭 O número absoluto não diz nada — 400 rejeições é muito ou
       pouco? O que importa é a PROPORÇÃO e a TENDÊNCIA:

         0,02% todo dia            →  normal, é o ruído da origem
         0,02% → 14% de um dia     →  a origem mudou algo. Investigue.

       Guarde o histórico dessa taxa. Sem ele, você não tem como
       distinguir os dois casos — e vai ou ignorar um incidente real
       ou acordar às 3h por causa do ruído de sempre.
    """
    # TODO: agrupe por (campo, tipo_do_erro) e devolva as contagens.
    raise NotImplementedError
