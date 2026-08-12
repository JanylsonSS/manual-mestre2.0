"""Cálculo das métricas de negócio.

Recebe registros **já validados** (saída de `validacao.py`) e produz números.

Este módulo não lê arquivo, não imprime nada e não formata. Ele só calcula.
Funções puras: mesma entrada → mesma saída, sempre.

⚠️ REGRA DE NEGÓCIO CENTRAL: faturamento considera APENAS pedidos com
   status == config.STATUS_FATURAVEL ("pago"). Foi exatamente esse detalhe
   que fez a Aurora apresentar um número errado ao investidor.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Callable

from atlas import config


# ---------------------------------------------------------------------------
# Blocos básicos
# ---------------------------------------------------------------------------


def valor_pedido(registro: dict) -> float:
    """Valor total de um pedido.

    Se `validar_linha` já calculou o campo `total`, apenas devolva-o.
    Caso contrário, calcule quantidade × preco_unitario.

    💡 Ter esta função de uma linha parece exagero, mas: quando amanhã
       entrar desconto ou frete no cálculo, você muda UM lugar.
    """
    # TODO: implementar
    raise NotImplementedError


def filtrar_faturados(registros: list[dict]) -> list[dict]:
    """Devolve apenas os pedidos que contam como faturamento.

    💡 Uma comprehension resolve. Use config.STATUS_FATURAVEL — não escreva
       a string "pago" literal aqui.
    """
    # TODO: implementar
    raise NotImplementedError


def agrupar_por(
    registros: list[dict],
    campo: str,
    metrica: Callable[[dict], float] | None = None,
) -> dict[str, dict]:
    """Agrupa registros por um campo e calcula métricas de cada grupo.

    Esta é a função mais reutilizada do módulo. Ela não sabe nada sobre
    "cidade" — agrupa por QUALQUER campo. É isso que permite usar a mesma
    função para cidade, categoria, canal, produto e cliente.

    Args:
        registros: Pedidos já filtrados (normalmente só os faturados).
        campo: Nome do campo de agrupamento (ex.: "cidade").
        metrica: Função que extrai o valor a somar de cada registro.
            Padrão: `valor_pedido`.

    Returns:
        Dict {valor_do_campo: {"faturamento": float, "pedidos": int,
                               "itens": int, "clientes": int}}

        `clientes` é a contagem de clientes DISTINTOS do grupo.

    💡 Use defaultdict. Para contar clientes distintos, acumule um set durante
       o laço e converta para len() no final — não dá para somar sets.

    💡 Considere um segundo dict auxiliar para os sets de clientes, em vez de
       guardar o set dentro do dict de métricas. Fica mais limpo na hora de
       serializar para JSON (set não é serializável!).
    """
    # TODO: implementar
    raise NotImplementedError


def calcular_totais(registros: list[dict]) -> dict:
    """Calcula os indicadores gerais do período.

    Args:
        registros: TODOS os registros válidos (não só os faturados) — a taxa
            de cancelamento precisa do denominador completo.

    Returns:
        {
            "pedidos_total": int,
            "pedidos_faturados": int,
            "pedidos_cancelados": int,
            "pedidos_pendentes": int,
            "faturamento": float,
            "itens": int,
            "ticket_medio": float,
            "taxa_cancelamento": float,   # fração, ex.: 0.15
            "clientes_unicos": int,
            "cidades_ativas": int,
        }

    ⚠️ PROTEJA TODA DIVISÃO. Se não houver nenhum pedido faturado, o ticket
       médio deve ser 0.0 e não estourar ZeroDivisionError. O mesmo para a
       taxa de cancelamento com lista vazia.

       Padrão: `x / y if y else 0.0`
    """
    # TODO: implementar
    raise NotImplementedError


def top_n(agrupado: dict[str, dict], n: int = 5, chave: str = "faturamento") -> list[tuple[str, dict]]:
    """Devolve os N maiores grupos, ordenados decrescentemente.

    Args:
        agrupado: Saída de agrupar_por().
        n: Quantos devolver.
        chave: Métrica de ordenação.

    Returns:
        Lista de tuplas (nome_do_grupo, metricas), do maior para o menor.

    💡 sorted(agrupado.items(), key=lambda kv: kv[1][chave], reverse=True)[:n]
    """
    # TODO: implementar
    raise NotImplementedError


def calcular_shares(agrupado: dict[str, dict]) -> dict[str, dict]:
    """Adiciona a chave "share" (participação no total) a cada grupo.

    Args:
        agrupado: Saída de agrupar_por().

    Returns:
        O mesmo dict, com "share" (fração de 0 a 1) em cada grupo.

    ⚠️ Decida: você altera o dict recebido ou devolve um novo? Alterar o
       argumento é um efeito colateral que surpreende quem chama. Prefira
       devolver um novo. (Revise a aula 01_04 sobre mutação de argumentos.)

    ⚠️ Proteja a divisão por total zero.
    """
    # TODO: implementar
    raise NotImplementedError


def calcular_curva_abc(agrupado: dict[str, dict]) -> list[dict]:
    """Classifica os grupos em curva ABC pelo faturamento acumulado.

    Regra (ver config):
        - Classe A: grupos até 80% do faturamento acumulado
        - Classe B: de 80% até 95%
        - Classe C: os 5% restantes

    Args:
        agrupado: Saída de agrupar_por().

    Returns:
        Lista ordenada por faturamento decrescente, cada item:
            {"nome": str, "faturamento": float, "share": float,
             "share_acumulado": float, "classe": "A"|"B"|"C"}

    💡 Algoritmo:
       1. Ordene decrescente por faturamento
       2. Percorra acumulando o share
       3. Classifique conforme o acumulado ATÉ AQUELE ITEM (inclusive)

    ⚠️ Detalhe sutil: o item que CRUZA os 80% ainda é classe A. A regra é
       "os itens necessários para atingir 80%", não "os itens abaixo de 80%".
    """
    # TODO: implementar
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Orquestração
# ---------------------------------------------------------------------------


def calcular_metricas(registros: list[dict]) -> dict:
    """Calcula TODAS as métricas do relatório, em um único dict.

    Esta é a função que `cli.py` chama. Ela não faz cálculo próprio — só
    orquestra as anteriores. Se você começar a escrever `for` aqui, algo
    está no lugar errado.

    Args:
        registros: Todos os registros válidos.

    Returns:
        {
            "totais": dict,               # calcular_totais
            "por_cidade": dict,           # agrupar_por + shares
            "por_categoria": dict,
            "por_canal": dict,
            "por_produto": dict,
            "por_cliente": dict,
            "top_produtos": list,         # top_n
            "top_clientes": list,
            "curva_abc_cidades": list,    # calcular_curva_abc
        }

    💡 Umas 12 linhas, cada uma chamando uma função. Se passar de 20,
       revise.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: montar 3 ou 4 registros fictícios na mão e conferir se
    #       calcular_totais devolve os números que você calculou no papel.
    #       Este é o teste mais valioso do projeto: se a matemática estiver
    #       errada, todo o resto é decoração.
    pass
