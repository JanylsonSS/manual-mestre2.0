"""Camada de serviço — a lógica de negócio do Atlas.

**A dor que este arquivo resolve:**

    "Toda vez que preciso de uma métrica nova, copio um bloco de 40
     linhas e mudo três palavras. Já tem cinco cópias quase iguais."

No Módulo 01 você tinha `agrupar_por_cidade`, `agrupar_por_produto`,
`agrupar_por_canal`... cada uma com o mesmo laço e o mesmo acumulador.

Aqui existe **um** método `por(dimensao)`. A dimensão é PARÂMETRO.

🎯 **O teste do desenho:** adicionar a dimensão "trimestre" deve ser
   uma linha no modelo (uma property), não uma função nova aqui.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Callable

from atlas.modelos import Metricas, Pedido

# Convenção: um logger por módulo, nomeado pelo próprio módulo.
# Isso cria a hierarquia atlas.servicos, atlas.leitura, etc., e permite
# silenciar um módulo barulhento sem tocar nos outros.
log = logging.getLogger(__name__)


class Agregador:
    """Agrega pedidos por qualquer dimensão.

    Guarda os pedidos UMA vez. Antes, 14 funções recebiam a mesma lista
    como argumento; agora todas usam `self.pedidos`.
    """

    def __init__(self, pedidos: list[Pedido]) -> None:
        # TODO: guardar os pedidos e registrar um log.debug com a contagem
        raise NotImplementedError

    # ── Propriedades derivadas ───────────────────────────────
    @property
    def faturados(self) -> list[Pedido]:
        """Apenas os pedidos que contam como faturamento.

        💡 Considere cachear: esta lista é recalculada a cada acesso, e
           todos os métodos abaixo a usam. Uma opção é `functools.cached_property`
           — mas cuidado, ela invalida o cache nunca. Se os pedidos puderem
           mudar, documente ou não cacheie.
        """
        # TODO
        raise NotImplementedError

    # ── Agregação genérica ───────────────────────────────────
    def por(self, dimensao: str) -> dict[str, Metricas]:
        """Agrupa por qualquer atributo do Pedido.

        Args:
            dimensao: nome de um atributo ou property de Pedido
                      ("cidade", "uf", "canal", "mes", "status"...)

        Returns:
            {valor_da_dimensao: Metricas}

        💡 A implementação usa `getattr(pedido, dimensao)`. É isso que
           torna o método genérico. Adicionar a dimensão "trimestre" é
           adicionar uma property `trimestre` em Pedido — este código
           não muda.

        ⚠️ Valide a dimensão! `getattr` com um nome errado levanta
           AttributeError no meio do laço, com mensagem obscura.
           Falhe cedo, com mensagem que liste as dimensões disponíveis.

        💡 Enum como chave: se a dimensão for `canal` (um Enum), a chave
           do dict será o Enum, não a string. Decida se converte com
           `.value` e seja consistente.
        """
        # TODO
        raise NotImplementedError

    def por_produto(self) -> dict[str, Metricas]:
        """Agrega no nível do ITEM, não do pedido.

        ⚠️ Este é o único método que precisa descer aos itens — por isso
           não cabe em `por()`. Repare que `Metricas.pedidos` aqui conta
           quantos PEDIDOS continham o produto, não quantos itens.
        """
        # TODO
        raise NotImplementedError

    def por_categoria(self) -> dict[str, Metricas]:
        """Como por_produto, mas agrupando pela categoria do produto."""
        # TODO
        raise NotImplementedError

    def totais(self) -> Metricas:
        """Métricas gerais do período."""
        # TODO
        raise NotImplementedError

    # ── Rankings e classificação ─────────────────────────────
    def top(self, dimensao: str, n: int = 5,
            por: str = "receita") -> list[tuple[str, Metricas]]:
        """Os N maiores de uma dimensão.

        Args:
            por: atributo de Metricas usado na ordenação
                 ("receita", "margem", "pedidos", "ticket_medio"...)
        """
        # TODO: sorted(..., key=lambda kv: getattr(kv[1], por), reverse=True)[:n]
        raise NotImplementedError

    def curva_abc(self, dimensao: str = "cidade",
                  corte_a: float = 0.80, corte_b: float = 0.95) -> list[dict]:
        """Classifica em A/B/C pelo faturamento acumulado.

        Returns:
            Lista ordenada, cada item com: nome, receita, share,
            share_acumulado, classe.

        ⚠️ O detalhe que quase todo mundo erra: o item que CRUZA os 80%
           ainda é classe A. A regra é "os itens necessários PARA ATINGIR
           80%", não "os que estão abaixo de 80%".
        """
        # TODO
        raise NotImplementedError

    def taxa_cancelamento(self) -> float:
        """Cancelados sobre o TOTAL de pedidos (não só os faturados).

        ⚠️ Cuidado para não filtrar cedo demais: o denominador aqui é
           `self.pedidos`, não `self.faturados`.
        """
        # TODO
        raise NotImplementedError

    def sem_giro(self, catalogo: list) -> list:
        """Produtos do catálogo que não tiveram nenhuma venda.

        💡 Um `set` de SKUs vendidos resolve isso em O(n). Uma busca
           linear no catálogo para cada venda seria O(n²).
        """
        # TODO
        raise NotImplementedError


class AnalisadorTemporal:
    """Análises que dependem da linha do tempo.

    Classe separada porque é uma responsabilidade distinta — e porque
    `Agregador` já está grande. Se uma classe passa de ~8 métodos
    públicos, provavelmente está fazendo duas coisas.
    """

    def __init__(self, pedidos: list[Pedido]) -> None:
        # TODO
        raise NotImplementedError

    def evolucao_mensal(self) -> list[dict]:
        """Uma linha por mês, com variação em relação ao anterior.

        ⚠️ Meses sem venda NÃO aparecem num agrupamento simples. Se junho
           teve zero pedidos, o gráfico fica com um buraco em vez de um
           vale — e a leitura muda completamente.

           Gere a série completa de meses entre o primeiro e o último,
           e preencha os vazios com zero. (Você fez isso com CTE recursiva
           no M03; aqui é um laço.)
        """
        # TODO
        raise NotImplementedError

    def sazonalidade_semanal(self) -> dict[str, Metricas]:
        """Faturamento por dia da semana.

        💡 `datetime.strptime(data, "%Y-%m-%d").weekday()` devolve 0-6.
           Traduza para nome — número de dia da semana em relatório é
           hostil com o leitor.
        """
        # TODO
        raise NotImplementedError


class ServicoRelatorio:
    """Orquestra: agrega os dados e entrega pelo destino configurado.

    🎯 REPARE NO CONSTRUTOR: ele RECEBE as dependências, não as constrói.

    Isso é *injeção de dependência*, e é o que torna o código testável.
    No Módulo 12 você vai passar um `DestinoMemoria` e verificar o
    conteúdo do relatório sem tocar no disco.

    Se este construtor fizesse `self.destino = DestinoArquivo()`, testar
    exigiria criar arquivos de verdade, limpar depois, e lidar com
    permissões no CI. Uma linha de desenho, muitas horas de diferença.
    """

    def __init__(
        self,
        agregador: Agregador,
        formatador,          # atlas.apresentacao.Formatador (Protocol)
        destino,             # atlas.apresentacao.Destino (Protocol)
        logger: logging.Logger | None = None,
    ) -> None:
        # TODO
        raise NotImplementedError

    def secao(self, titulo: str, dimensao: str) -> str:
        """Gera uma seção do relatório."""
        # TODO
        raise NotImplementedError

    def gerar(self, secoes: list[tuple[str, str]] | None = None) -> str:
        """Gera o relatório completo e entrega ao destino.

        Args:
            secoes: lista de (titulo, dimensao). Se None, usa o padrão.
        """
        # TODO
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: montar alguns Pedidos na mão, criar um Agregador e imprimir
    #       `por("cidade")` e `totais()`. Confira os números na calculadora
    #       — se a matemática estiver errada, todo o resto é decoração.
    pass
