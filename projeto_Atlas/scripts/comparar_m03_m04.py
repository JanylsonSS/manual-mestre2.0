#!/usr/bin/env python3
"""Verifica que a refatoração do M04 NÃO mudou o comportamento.

🎯 Este script é a rede de segurança do Módulo 04.

Refatorar é mudar a ESTRUTURA sem mudar o COMPORTAMENTO. Se a saída
mudou, você não refatorou — reescreveu, e provavelmente introduziu um bug.

Uso:
    python scripts/comparar_m03_m04.py
    python scripts/comparar_m03_m04.py --tolerancia 0.01
    python scripts/comparar_m03_m04.py --relatorio faturamento_por_cidade

Saída esperada:
    ✅ faturamento_por_cidade  : idêntico
    ✅ faturamento_por_canal   : idêntico
    ❌ curva_abc               : divergência em Sorocaba (80.1% vs 80.0%)

Código de saída: 0 se tudo bate, 1 se houver divergência.
⚠️ Esse código é o que o CI vai olhar no Módulo 09. Acerte-o.
"""

from __future__ import annotations

import sys
from pathlib import Path

# TODO: adicionar src ao path OU (melhor) instalar o pacote com
#       `pip install -e .` e simplesmente importar.
#       Se você fez a Etapa 7 do roteiro, o import já funciona direto.


# ═══════════════════════════════════════════════════════════════
#  Configuração
# ═══════════════════════════════════════════════════════════════

PASTA_REFERENCIA = Path("tests/referencia")
TOLERANCIA_PADRAO = 0.01     # 1 centavo

RELATORIOS = [
    "faturamento_por_cidade",
    "faturamento_por_categoria",
    "top_produtos",
    "top_clientes",
    "evolucao_mensal",
    "curva_abc",
    "alerta_estoque",
]


# ═══════════════════════════════════════════════════════════════
#  Comparação
# ═══════════════════════════════════════════════════════════════

def carregar_referencia(nome: str) -> list[dict]:
    """Carrega a saída congelada do M03.

    Os arquivos de referência foram gerados na Etapa 0 do roteiro:
        python main.py relatorio --todos --formato json > tests/referencia/...

    Raises:
        FileNotFoundError: com mensagem explicando como gerar.

    💡 Mensagem de erro boa diz o que fazer:
       "Referência não encontrada. Gere com: python main.py ... > ..."
    """
    # TODO
    raise NotImplementedError


def gerar_atual(nome: str) -> list[dict]:
    """Executa o relatório pela implementação NOVA (M04).

    💡 Chame o `ServicoRelatorio` com `FormatadorJSON` e `DestinoMemoria` —
       assim você compara os dados sem tocar no disco.
    """
    # TODO
    raise NotImplementedError


def comparar_valores(a, b, tolerancia: float) -> bool:
    """Compara dois valores, tolerando arredondamento em floats.

    ⚠️ Não use `==` em float. Você viu na aula 01_01 por quê.
       Use `abs(a - b) <= tolerancia`.

    ⚠️ Cuidado com tipos diferentes: o M03 pode devolver `Decimal` e o
       M04 `float`. Normalize antes de comparar.
    """
    # TODO
    raise NotImplementedError


def comparar_relatorio(nome: str, tolerancia: float) -> dict:
    """Compara um relatório linha a linha, campo a campo.

    Returns:
        {
            "nome": str,
            "identico": bool,
            "linhas_ref": int,
            "linhas_atual": int,
            "divergencias": [
                {"linha": int, "chave": str, "campo": str,
                 "esperado": ..., "obtido": ...},
            ],
        }

    Verificações, nesta ordem (falhe na primeira):
      1. Mesmo número de linhas?
      2. Mesmas chaves (cidades, produtos...)? Compare como CONJUNTOS.
      3. Mesma ORDEM? (importa em ranking; não importa em lookup)
      4. Mesmos valores, dentro da tolerância?

    💡 Reportar "5 divergências" sem dizer quais é inútil. Colete todas
       e mostre as 10 primeiras com esperado × obtido.
    """
    # TODO
    raise NotImplementedError


def formatar_resultado(resultado: dict) -> str:
    """Uma linha por relatório, com detalhe se houver divergência."""
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Diagnóstico
# ═══════════════════════════════════════════════════════════════

def diagnosticar(divergencias: list[dict]) -> list[str]:
    """Sugere causas prováveis a partir do padrão das divergências.

    Heurísticas que valem a pena implementar:

      • Todas as diferenças < 0.01        → arredondamento; provavelmente ok
      • Diferença constante em todas      → fator sistemático (imposto? frete?)
      • M04 sempre MAIOR                  → algo sendo somado duas vezes
      • M04 sempre MENOR                  → filtro a mais
      • Uma chave a mais/menos            → normalização diferente
      • Mesmos valores, ordem diferente   → falta desempate no sorted

    💭 Esta função transforma "deu diferente" em "provavelmente é X".
       É o tipo de ferramenta que você agradece às 23h de uma sexta.
    """
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Entrada
# ═══════════════════════════════════════════════════════════════

def main(argv: list[str] | None = None) -> int:
    """Compara todos os relatórios e devolve o código de saída.

    Estrutura:
      1. Parsear argumentos (--tolerancia, --relatorio, --verbose)
      2. Para cada relatório: carregar referência, gerar atual, comparar
      3. Imprimir uma linha por relatório
      4. Se houver divergência, imprimir o detalhe e o diagnóstico
      5. Resumo final
      6. return 0 se tudo bate, 1 caso contrário

    ⚠️ Se a pasta de referência não existir, oriente o usuário a gerá-la
       em vez de estourar um FileNotFoundError cru.
    """
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
