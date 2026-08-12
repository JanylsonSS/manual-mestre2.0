"""Formatação de valores para exibição.

Funções **puras**: recebem um valor, devolvem uma string. Não leem arquivo,
não imprimem nada, não dependem de estado externo.

Isso significa que você consegue verificar cada uma isoladamente — e é
exatamente o que vamos fazer com pytest no Módulo 12.

⚠️ Formatação NÃO é cálculo. Nunca arredonde aqui de um jeito que altere o
   número usado em outra conta. Formatar é a última coisa que acontece,
   logo antes de o valor virar texto na tela.
"""

from __future__ import annotations


def formatar_brl(valor: float) -> str:
    """Formata um número no padrão monetário brasileiro.

    Args:
        valor: O número a formatar.

    Returns:
        String no formato "R$ 1.234,56".

    Examples:
        >>> formatar_brl(1234.5)
        'R$ 1.234,50'
        >>> formatar_brl(0)
        'R$ 0,00'
        >>> formatar_brl(-99.9)
        'R$ -99,90'

    💡 O padrão brasileiro é PONTO no milhar e VÍRGULA no decimal — o inverso
       do que `f"{valor:,.2f}"` produz. Você precisa trocar os dois
       separadores. Trocar direto (`.replace(",", ".")` seguido de
       `.replace(".", ",")`) NÃO funciona: a segunda troca desfaz a primeira.
       Use um caractere temporário como ponte.
    """
    # TODO: implementar
    raise NotImplementedError


def formatar_pct(valor: float, casas: int = 1) -> str:
    """Formata uma fração como percentual brasileiro.

    Args:
        valor: Fração entre 0 e 1 (0.125 = 12,5%).
        casas: Casas decimais. Padrão 1.

    Returns:
        String no formato "12,5%".

    Examples:
        >>> formatar_pct(0.125)
        '12,5%'
        >>> formatar_pct(0.5, casas=0)
        '50%'
    """
    # TODO: implementar
    raise NotImplementedError


def formatar_int(valor: int) -> str:
    """Formata um inteiro com separador de milhar brasileiro.

    Examples:
        >>> formatar_int(1234567)
        '1.234.567'
    """
    # TODO: implementar
    raise NotImplementedError


def truncar(texto: str, limite: int = 30, sufixo: str = "…") -> str:
    """Corta um texto que exceda o limite, adicionando um sufixo.

    O resultado nunca deve passar de `limite` caracteres (o sufixo conta).

    Examples:
        >>> truncar("Notebook Dell Inspiron 15", 12)
        'Notebook De…'
        >>> truncar("Mouse", 12)
        'Mouse'
    """
    # TODO: implementar
    raise NotImplementedError


def barra_ascii(fracao: float, largura: int = 20, cheio: str = "█", vazio: str = "░") -> str:
    """Desenha uma barra de progresso em ASCII.

    Args:
        fracao: Valor entre 0 e 1. Valores fora da faixa devem ser limitados.
        largura: Número total de caracteres da barra.

    Examples:
        >>> barra_ascii(0.5, largura=10)
        '█████░░░░░'

    💡 Útil para o gráfico de barras do relatório em texto. Combine com
       `formatar_pct` para mostrar a barra e o número lado a lado.
    """
    # TODO: implementar
    raise NotImplementedError


def linha_tabela(colunas: list[str], larguras: list[int], alinhamentos: list[str] | None = None) -> str:
    """Monta uma linha de tabela com colunas alinhadas.

    Args:
        colunas: Os textos de cada coluna.
        larguras: A largura de cada coluna.
        alinhamentos: "<", ">" ou "^" para cada coluna. Padrão: "<" para a
            primeira, ">" para as demais (texto à esquerda, números à direita).

    Examples:
        >>> linha_tabela(["Campinas", "1.000,00"], [12, 12])
        'Campinas        1.000,00'

    💡 Use a mini-linguagem de formatação: f"{texto:{alinhamento}{largura}}".
       As chaves aninhadas permitem que alinhamento e largura sejam variáveis.
    """
    # TODO: implementar
    raise NotImplementedError


def cabecalho(titulo: str, largura: int = 78, caractere: str = "=") -> str:
    """Monta um cabeçalho centralizado entre duas linhas de separação.

    Returns:
        Um bloco de 3 linhas (separador, título centralizado, separador).
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # Bloco de verificação rápida. Rode com:
    #     python src/atlas/formatacao.py
    #
    # TODO: chamar cada função com os exemplos das docstrings e conferir
    #       a saída. Considere usar assert para que o script FALHE em vez
    #       de só imprimir algo errado. Exemplo:
    #
    #           assert formatar_brl(1234.5) == "R$ 1.234,50"
    #           print("✅ formatacao OK")
    pass
