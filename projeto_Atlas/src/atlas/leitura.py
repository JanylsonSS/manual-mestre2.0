"""Leitura de arquivos CSV.

Responsabilidade ÚNICA: pegar bytes do disco e devolver linhas cruas.

**Este módulo não valida nada.** Não converte tipos, não normaliza texto, não
aplica regra de negócio. Só lê. A validação é de `validacao.py`.

Por que essa separação obsessiva? Porque no Módulo 03 os dados vêm de SQLite,
no M05 de PostgreSQL e no M07 de uma API. Quando isso acontecer, só este
arquivo muda — `validacao.py` e `metricas.py` continuam idênticos.
"""

from __future__ import annotations

import csv
from pathlib import Path

from atlas import config
from atlas.excecoes import ArquivoInvalidoError


def verificar_arquivo(caminho: Path) -> None:
    """Valida que o arquivo existe e é legível, antes de tentar abrir.

    Args:
        caminho: Caminho do CSV.

    Raises:
        ArquivoInvalidoError: se não existir, não for arquivo ou estiver vazio.

    💡 "Falhar cedo" (fail fast): é muito melhor dar erro aqui, com mensagem
       clara, do que estourar um FileNotFoundError cru no meio do processamento.
    """
    # TODO: verificar caminho.exists()
    # TODO: verificar caminho.is_file()
    # TODO: verificar caminho.stat().st_size > 0
    # TODO: levantar ArquivoInvalidoError com mensagem específica em cada caso
    raise NotImplementedError


def verificar_colunas(cabecalho: list[str] | None) -> None:
    """Valida que o CSV tem todas as colunas obrigatórias.

    Args:
        cabecalho: Lista de nomes das colunas (DictReader.fieldnames).

    Raises:
        ArquivoInvalidoError: se o cabeçalho for None ou faltar alguma coluna
            de config.COLUNAS_OBRIGATORIAS.

    💡 Use set para descobrir o que falta:
       faltando = set(COLUNAS_OBRIGATORIAS) - set(cabecalho)
       A mensagem de erro deve LISTAR o que falta, não só dizer "colunas erradas".
    """
    # TODO: implementar
    raise NotImplementedError


def ler_csv(caminho: Path, delimitador: str = config.DELIMITADOR_CSV) -> list[tuple[int, dict[str, str]]]:
    """Lê um CSV e devolve as linhas cruas, numeradas.

    Args:
        caminho: Caminho do arquivo.
        delimitador: Separador de campos. Padrão "," (use ";" para Excel BR).

    Returns:
        Lista de tuplas (numero_da_linha, dict_com_a_linha). A numeração
        começa em 2, porque a linha 1 do arquivo é o cabeçalho — assim o
        número bate com o que o usuário vê ao abrir o arquivo no editor.

    Raises:
        ArquivoInvalidoError: arquivo ausente, vazio ou sem as colunas exigidas.

    ⚠️ Três detalhes que causam bug:
       1. `encoding=config.ENCODING` — sem isso, acentos quebram no Windows.
       2. `newline=""` — exigência do módulo csv.
       3. Use `csv.DictReader`, nunca `linha.split(",")`. Um campo com vírgula
          dentro de aspas ("Campinas, SP") destrói a abordagem ingênua.

    💡 `enumerate(leitor, start=2)` resolve a numeração de um golpe.
    """
    # TODO: 1. chamar verificar_arquivo
    # TODO: 2. abrir com with open(...)
    # TODO: 3. criar o DictReader
    # TODO: 4. chamar verificar_colunas(leitor.fieldnames)
    # TODO: 5. devolver a lista de tuplas numeradas
    raise NotImplementedError


def escrever_csv(
    caminho: Path,
    registros: list[dict],
    colunas: list[str],
    delimitador: str = config.DELIMITADOR_CSV,
) -> None:
    """Grava uma lista de dicts como CSV.

    Args:
        caminho: Destino. As pastas intermediárias devem ser criadas se
            não existirem.
        registros: Linhas a gravar.
        colunas: Nomes e ORDEM das colunas de saída.
        delimitador: Separador.

    💡 Use csv.DictWriter com fieldnames=colunas e não esqueça writeheader().
    💡 caminho.parent.mkdir(parents=True, exist_ok=True) evita
       FileNotFoundError quando a pasta saida/ ainda não existe.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: ler o arquivo padrão e imprimir quantas linhas vieram e a primeira.
    #       Rode com: python src/atlas/leitura.py
    #       (Se der ModuleNotFoundError, rode da raiz com
    #        `python -m atlas.leitura` após ajustar o PYTHONPATH, ou apenas
    #        teste este módulo a partir de main.py.)
    pass
