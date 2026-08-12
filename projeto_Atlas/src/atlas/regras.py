"""Motor de regras de precificação.

**A dor:**

    "Toda vez que o comercial cria uma promoção, eu abro a função
     calcular_desconto e adiciono mais um elif. Ela tem 200 linhas.
     Semana passada mexi nela e quebrei o desconto de volume."

**A solução:** cada regra é uma função independente que se auto-registra.

    Adicionar uma regra  = escrever uma função de 3 linhas
    Remover uma regra    = apagar a função
    Nenhum código existente é tocado → nenhum bug é introduzido no que já funcionava

Isso tem nome: **princípio aberto-fechado** — aberto para extensão,
fechado para modificação.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

from atlas.modelos import Pedido

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  Infraestrutura
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True, slots=True)
class DefinicaoRegra:
    """Metadados de uma regra registrada."""
    # TODO: nome: str, funcao: Callable[[Pedido], float],
    #       prioridade: int, descricao: str, ativa: bool = True


@dataclass(frozen=True, slots=True)
class AjusteAplicado:
    """Uma regra que disparou, para a trilha de auditoria."""
    # TODO: regra: str, ajuste: float, descricao: str


@dataclass(slots=True)
class ResultadoPrecificacao:
    """Resultado completo, com auditoria.

    💭 Por que devolver a trilha e não só o número final?

       Porque quando o cliente ligar reclamando que "o desconto veio
       errado", você precisa responder QUAIS regras dispararam e com
       qual peso. Um sistema que só devolve `0.23` não tem resposta.
    """
    valor_bruto: float = 0.0
    ajustes: list[AjusteAplicado] = field(default_factory=list)
    ajuste_bruto: float = 0.0
    ajuste_aplicado: float = 0.0
    teto_atingido: bool = False

    @property
    def valor_final(self) -> float:
        # TODO
        ...

    @property
    def economia(self) -> float:
        """Quanto o cliente deixou de pagar (positivo) ou pagou a mais."""
        # TODO
        ...

    def explicar(self) -> str:
        """Trilha legível, para atendimento e auditoria.

        Sugestão de saída:

            Bruto                            1.078,80
              volume            (prioridade 10)   -8,0%
              cliente_fiel      (prioridade 30)   -7,0%
            ────────────────────────────────────────────
              soma                              -15,0%
            TOTAL                              916,98
        """
        # TODO
        ...


# Registro global das regras
REGRAS: dict[str, DefinicaoRegra] = {}


def regra(nome: str, prioridade: int = 100, descricao: str = "", ativa: bool = True):
    """Decorador que REGISTRA uma função como regra de precificação.

    ⚠️ Este decorador devolve a função INTACTA. Ele não envelopa nada —
       apenas cataloga. Por isso `@wraps` não é necessário aqui.

    Args:
        nome: identificador único da regra
        prioridade: menor roda primeiro (só afeta a ordem da auditoria)
        descricao: texto para o relatório de auditoria
        ativa: permite desligar sem apagar

    Uso:
        @regra("volume", prioridade=10, descricao="10+ unidades: 8% off")
        def desconto_volume(pedido: Pedido) -> float:
            return -0.08 if pedido.quantidade_itens >= 10 else 0.0

    ⚠️ Convenção de sinal: NEGATIVO é desconto, POSITIVO é acréscimo.
       Documente isso em letras garrafais — inverter o sinal por engano
       é o bug mais caro que este arquivo pode produzir.

    ⚠️ Rejeite nome duplicado. Se duas regras se registram com o mesmo
       nome, a segunda sobrescreve a primeira silenciosamente.
    """
    # TODO
    raise NotImplementedError


def aplicar_regras(pedido: Pedido, teto: float = 0.25) -> ResultadoPrecificacao:
    """Aplica todas as regras ativas, respeitando o teto.

    Args:
        teto: ajuste máximo em módulo (0.25 = no máximo ±25%)

    ⚠️ O teto é a trava de segurança. Sem ele, cinco promoções
       simultâneas podem zerar o preço — e você só descobre quando o
       financeiro perguntar por que a receita do dia foi R$ 12.

    💡 Registre em log quando o teto for atingido. Isso é sinal de que
       as promoções estão se acumulando de forma não planejada, e o
       comercial precisa saber.
    """
    # TODO
    raise NotImplementedError


def listar_regras(incluir_inativas: bool = False) -> list[DefinicaoRegra]:
    """Regras registradas, ordenadas por prioridade.

    💡 Alimenta `atlas regras --listar` na CLI, sem nenhuma lista
       codificada à mão.
    """
    # TODO
    raise NotImplementedError


def desativar(nome: str) -> None:
    """Desliga uma regra sem removê-la do registro."""
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  As regras de negócio da Aurora
#
#  🎯 A partir daqui, cada regra é INDEPENDENTE.
#     Adicionar a próxima não exige tocar em nenhuma anterior.
# ═══════════════════════════════════════════════════════════════

# TODO: @regra("volume", prioridade=10)
#   10 unidades ou mais no pedido → 8% de desconto

# TODO: @regra("categoria_monitores", prioridade=20)
#   Queima de estoque de monitores → 5%

# TODO: @regra("cliente_corporativo", prioridade=30)
#   Segmento corporativo → 6%

# TODO: @regra("alto_valor", prioridade=40)
#   Subtotal >= R$ 5.000 → 10%

# TODO: @regra("comissao_marketplace", prioridade=50)
#   Canal marketplace → +12% (repasse da comissão da plataforma)
#   ⚠️ Note o sinal POSITIVO: é acréscimo, não desconto.

# TODO: @regra("frete_gratis", prioridade=60)
#   Subtotal >= R$ 500 → abate o frete
#   💭 Desafio de modelagem: o frete não é percentual sobre o subtotal.
#      Como expressar isso num motor que devolve percentuais?
#      Duas saídas: (a) converter para percentual equivalente;
#      (b) mudar o contrato da regra para devolver (tipo, valor).
#      Escolha uma e documente o motivo.

# TODO: @regra("sobretaxa_regiao", prioridade=70)
#   UF fora do Sudeste (SP/RJ/MG/ES) → +3% (logística)

# TODO (opcional): @regra("black_friday", prioridade=5)
#   Data em novembro → 15%
#   💡 Prioridade 5 a faz aparecer primeiro na auditoria — o que faz
#      sentido: é a promoção que o cliente veio buscar.


if __name__ == "__main__":
    # TODO: montar 3 pedidos que disparem combinações diferentes de regras
    #       e imprimir `resultado.explicar()` de cada um.
    #
    #       Inclua DELIBERADAMENTE um pedido que estoure o teto — é o
    #       caso que prova que a trava funciona.
    pass
