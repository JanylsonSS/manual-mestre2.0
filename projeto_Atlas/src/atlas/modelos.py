"""Modelos de domínio do Atlas — dataclasses tipadas.

**A mudança do Módulo 04:** até aqui os dados circulavam como `dict`.
Isso funciona, mas custa caro:

  • `pedido["quantiade"]` (com typo) só falha em execução, e longe da causa
  • nenhum editor sabe quais chaves existem
  • a validação fica espalhada por quem consome
  • cálculos derivados são reescritos em cada lugar

Com dataclasses tipadas, o editor autocompleta, o mypy verifica antes de
rodar, e cada cálculo derivado mora em UM lugar (a property).

**A estratégia de validação em camadas:**

    CSV/API  →  [Pydantic]  →  dataclass  →  [confiança]  →  resto do sistema
                 fronteira      domínio                        miolo

Valide UMA VEZ, na fronteira. Depois disso, o tipo é a garantia.
Revalidar a cada camada só custa tempo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ═══════════════════════════════════════════════════════════════
#  Enums — domínios fechados
# ═══════════════════════════════════════════════════════════════

class Status(str, Enum):
    """Status de um pedido.

    💡 Por que herdar de `str`?
       Porque assim `Status.PAGO == "pago"` é True, e o valor serializa
       direto para JSON sem conversão. Você ganha a segurança do Enum
       sem perder a conveniência da string.
    """
    # TODO: PAGO, PENDENTE, CANCELADO


class Canal(str, Enum):
    """Canal de venda."""
    # TODO: SITE, APP, MARKETPLACE


class Segmento(str, Enum):
    """Segmento do cliente."""
    # TODO: VAREJO, CORPORATIVO


# ═══════════════════════════════════════════════════════════════
#  Modelos
# ═══════════════════════════════════════════════════════════════

@dataclass(frozen=True, slots=True)
class Produto:
    """Um produto do catálogo.

    Por que `frozen=True`?
      1. Um produto não muda de identidade no meio de um relatório.
      2. Torna a classe HASHEÁVEL — pode ser chave de dict nas agregações.
      3. Impede que uma camada altere o objeto por acidente.

    Por que `slots=True`?
      Menos memória e atributo inexistente vira erro em vez de criar um
      atributo novo silenciosamente. (Sem slots, `p.precoo = 10` funciona
      e cria um campo com typo.)
    """
    # TODO: declarar os campos com anotação de tipo:
    #   sku, nome, categoria: str
    #   preco, custo: float

    def __post_init__(self) -> None:
        """Valida invariantes logo após a criação.

        ⚠️ Com `frozen=True`, você NÃO pode fazer `self.campo = valor` aqui.
           Se precisar normalizar, use:
               object.__setattr__(self, "campo", valor_normalizado)
           É deliberadamente feio — para você pensar duas vezes.
        """
        # TODO: rejeitar preco < 0, custo < 0, sku vazio

    @property
    def margem_unitaria(self) -> float:
        """Margem em reais por unidade.

        💡 Property, não atributo. Se fosse atributo, você teria que
           lembrar de recalculá-lo toda vez que preco ou custo mudasse —
           e um dia esqueceria.
        """
        # TODO

    @property
    def margem_percentual(self) -> float:
        """Margem sobre o preço (0.0 a 1.0).

        ⚠️ Proteja a divisão por zero: preço pode ser 0 (brinde).
        """
        # TODO


@dataclass(frozen=True, slots=True)
class Cliente:
    """Um cliente da Aurora."""
    # TODO: id: int, nome, email, cidade, uf: str,
    #       segmento: Segmento, data_cadastro: str

    def __post_init__(self) -> None:
        # TODO: validar e-mail (contém @), UF (2 letras maiúsculas)
        ...

    @property
    def praca(self) -> str:
        """'Campinas/SP' — usado como chave de agrupamento."""
        # TODO


@dataclass(slots=True)
class ItemVenda:
    """Um item dentro de um pedido.

    NÃO é frozen: a quantidade pode ser ajustada antes do fechamento.

    ⚠️ Repare que guardamos `preco_unitario` além do `produto.preco`.
       Você respondeu por quê no M03: o preço de catálogo muda, o
       praticado na venda não pode mudar. Snapshot de dado histórico.
    """
    # TODO: produto: Produto, quantidade: int, preco_unitario: float

    def __post_init__(self) -> None:
        # TODO: quantidade > 0, preco_unitario >= 0
        ...

    @property
    def total(self) -> float:
        # TODO: quantidade * preco_unitario, arredondado
        ...

    @property
    def margem(self) -> float:
        """Margem do item — usa o preço PRATICADO, não o de catálogo."""
        # TODO: quantidade * (preco_unitario - produto.custo)
        ...

    @property
    def desconto_praticado(self) -> float:
        """Quanto abaixo do preço de catálogo a venda saiu (0.0 a 1.0).

        💡 Métrica valiosa: revela se um produto vive em promoção.
        """
        # TODO


@dataclass(slots=True)
class Pedido:
    """Um pedido com seus itens."""
    # TODO: id: int, cliente: Cliente, data: str,
    #       status: Status, canal: Canal, frete: float = 0.0,
    #       itens: list[ItemVenda] = field(default_factory=list)
    #
    # 🔴 `itens: list[ItemVenda] = []` levanta ValueError na definição
    #    da dataclass. É a terceira vez que você encontra essa armadilha
    #    (argumento padrão no M01, atributo de classe na aula 04_03).
    #    Desta vez a linguagem te protege.

    @property
    def subtotal(self) -> float:
        """Soma dos itens, SEM frete."""
        # TODO

    @property
    def total(self) -> float:
        """Subtotal + frete."""
        # TODO

    @property
    def margem(self) -> float:
        # TODO
        ...

    @property
    def quantidade_itens(self) -> int:
        """Total de UNIDADES (não de linhas de item)."""
        # TODO

    @property
    def faturado(self) -> bool:
        """Regra de negócio central do Atlas: só 'pago' conta."""
        # TODO: self.status is Status.PAGO

    @property
    def mes(self) -> str:
        """'2026-07' — para agrupamento mensal."""
        # TODO

    @property
    def cidade(self) -> str:
        """Atalho para self.cliente.cidade.

        💡 Existe para que `Agregador.por("cidade")` funcione com
           getattr(pedido, "cidade") sem precisar navegar o objeto.
        """
        # TODO

    @property
    def uf(self) -> str:
        # TODO
        ...

    def adicionar(self, item: ItemVenda) -> Pedido:
        """Adiciona um item e devolve self, permitindo encadeamento.

        💡 Devolver `self` permite:
               pedido.adicionar(a).adicionar(b).adicionar(c)
           É o padrão *fluent interface*.
        """
        # TODO


@dataclass(frozen=True, slots=True)
class Metricas:
    """Resultado de uma agregação.

    `frozen=True` de propósito: é um RETRATO de um instante. Depois de
    calculado, ninguém deveria alterá-lo.

    O método `somar` devolve uma instância NOVA em vez de mutar — isso
    se chama estrutura de dados PERSISTENTE. Vantagens: nenhuma camada
    pode corromper suas métricas, e o objeto é seguro entre threads.

    ⚠️ O custo é criar um objeto por soma. Para milhares, irrelevante.
       Para dezenas de milhões, use um acumulador mutável.
    """
    pedidos: int = 0
    itens: int = 0
    receita: float = 0.0
    margem: float = 0.0
    frete: float = 0.0

    @property
    def ticket_medio(self) -> float:
        # TODO: proteja a divisão por zero
        ...

    @property
    def margem_percentual(self) -> float:
        # TODO
        ...

    def somar(self, pedido: Pedido) -> Metricas:
        """Devolve uma NOVA Metricas com o pedido incorporado."""
        # TODO: return Metricas(pedidos=..., itens=..., ...)
        ...

    def __add__(self, outra: Metricas) -> Metricas:
        """Permite `total = sum(lista_de_metricas, Metricas())`.

        💡 Definir __add__ deixa as métricas combináveis — útil quando
           você agrega em paralelo (Parte G do projeto) e precisa juntar
           os resultados parciais de cada processo.
        """
        # TODO


@dataclass(frozen=True, slots=True)
class Rejeicao:
    """Uma linha descartada na validação, com o motivo."""
    # TODO: linha: int, campo: str, motivo: str, dado: str

    def __str__(self) -> str:
        # TODO: "linha 42 | quantidade | valor não inteiro: 'dez'"
        ...


if __name__ == "__main__":
    # TODO: crie um Produto, um ItemVenda e um Pedido; imprima as
    #       properties calculadas; e prove que Produto é hasheável
    #       ({produto: 0} deve funcionar) e imutável.
    pass
