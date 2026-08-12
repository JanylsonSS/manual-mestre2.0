"""Interface de linha de comando — orquestração do Atlas.

Este módulo é o **maestro**: ele não toca nenhum instrumento, só coordena.

Fluxo:

    ler → validar → calcular → renderizar → gravar → resumir

Se `main()` ficar difícil de ler, o problema quase sempre é que alguma
lógica que deveria estar em outro módulo vazou para cá.

⚠️ Este é o ÚNICO lugar do projeto que deve capturar `AtlasError` e
   transformá-lo em mensagem amigável. Nos módulos internos, as exceções
   sobem. É o padrão "trate na fronteira".
"""

from __future__ import annotations

import sys
from pathlib import Path

from atlas import config, leitura, metricas, relatorios, validacao
from atlas.excecoes import AtlasError


def resolver_caminho(argumento: str | None) -> Path:
    """Decide qual arquivo processar.

    Args:
        argumento: O que veio da linha de comando, ou None.

    Returns:
        Path do arquivo a processar. Se `argumento` for None, usa
        config.ARQUIVO_PADRAO.

    💡 Aceite tanto caminho relativo quanto absoluto. Path já lida com isso.
    """
    # TODO: implementar
    raise NotImplementedError


def preparar_saida() -> None:
    """Garante que a pasta de saída existe.

    💡 config.DIR_SAIDA.mkdir(parents=True, exist_ok=True)
    """
    # TODO: implementar
    raise NotImplementedError


def executar(caminho: Path) -> int:
    """Executa o pipeline completo para um arquivo.

    Args:
        caminho: CSV de entrada.

    Returns:
        Código de saída: 0 = sucesso, 1 = erro.

    Passos:
        1. leitura.ler_csv(caminho)
        2. validacao.validar_todas(linhas)
        3. metricas.calcular_metricas(validos)
        4. relatorios.render_txt / render_json
        5. relatorios.gravar_txt / gravar_json / gravar_rejeitados
        6. imprimir relatorios.resumo_terminal

    💡 Cada passo é UMA linha. Se você precisar de um `for` aqui, mova-o
       para o módulo apropriado.

    ⚠️ Caso de borda: e se TODAS as linhas forem rejeitadas? O programa não
       pode quebrar. Ele deve gerar os relatórios com zeros e deixar muito
       claro na saída que nenhum dado válido foi encontrado.
    """
    # TODO: implementar
    raise NotImplementedError


def main(argumento: str | None = None) -> int:
    """Ponto de entrada da CLI.

    Args:
        argumento: Caminho do CSV. Se None, tenta ler de sys.argv[1] e,
            na ausência, usa o padrão de config.

    Returns:
        Código de saída do processo (0 = sucesso).

    Responsabilidades:
        - Resolver o caminho
        - Preparar a pasta de saída
        - Chamar executar()
        - Capturar AtlasError e imprimir mensagem amigável (sem traceback)
        - Capturar KeyboardInterrupt (Ctrl+C) com elegância

    ⚠️ NÃO capture `Exception` genérico. Se um bug de programação acontecer,
       você QUER ver o traceback completo — ele é a informação que permite
       corrigir. Esconder isso atrás de "Ocorreu um erro" é sabotar você
       mesmo no futuro.

    💡 Mensagens de erro boas dizem o que aconteceu E o que fazer:
           ❌ Arquivo não encontrado: dados/brutos/vendas.csv
              Verifique o caminho ou rode: python main.py <caminho-do-csv>
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # Permite rodar este módulo diretamente também, além de via main.py.
    raise SystemExit(main())
