"""Apresentação — formatadores e destinos, por composição.

**Por que composição e não herança?**

Você tem 4 formatos (texto, CSV, JSON, Markdown) e 3 destinos (console,
arquivo, memória).

    Com herança:    RelatorioTextoArquivo, RelatorioTextoConsole,
                    RelatorioCSVArquivo, ...  →  12 classes
                    Adicionar 1 formato       →  +3 classes
                    Adicionar 1 destino       →  +4 classes

    Com composição: 4 formatadores + 3 destinos  →  7 classes
                    Adicionar 1 formato          →  +1 classe (ganha 3 combos)
                    Adicionar 1 destino          →  +1 classe (ganha 4 combos)

A explosão combinatória é o argumento mais concreto contra herança —
e ela aparece em qualquer sistema com mais de uma dimensão de variação.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Protocol, runtime_checkable

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  Contratos (Protocol — tipagem estrutural, sem herança)
# ═══════════════════════════════════════════════════════════════

@runtime_checkable
class Formatador(Protocol):
    """Contrato de um formatador.

    💡 Por que Protocol e não ABC?
       Porque Protocol é *estrutural*: qualquer classe com `extensao` e
       `formatar` satisfaz o contrato, SEM precisar herdar de nada.

       Isso significa que um formatador escrito por outra pessoa, numa
       biblioteca de terceiro, funciona no seu sistema sem modificação.
       É duck typing com verificação estática.
    """
    extensao: str

    def formatar(self, titulo: str, dados: dict | list) -> str: ...


@runtime_checkable
class Destino(Protocol):
    """Contrato de um destino de entrega."""

    def entregar(self, conteudo: str, nome: str) -> None: ...


# ═══════════════════════════════════════════════════════════════
#  Formatadores
# ═══════════════════════════════════════════════════════════════

class FormatadorTexto:
    """Tabela alinhada em texto puro."""

    extensao = "txt"

    def __init__(self, largura: int = 78, ordenar_por: str = "receita") -> None:
        # TODO
        raise NotImplementedError

    def formatar(self, titulo: str, dados: dict | list) -> str:
        """Monta a tabela.

        Regras de apresentação:
          • texto à esquerda, números à direita
          • valores monetários com separador brasileiro
          • percentuais com 1 casa
          • None vira "—", nunca "None"
          • larguras calculadas a partir do conteúdo real

        ⚠️ CUIDADO COM EMOJI em célula de tabela: `len("🔴")` é 1, mas o
           terminal desenha 2 colunas. O alinhamento quebra. Use marcadores
           ASCII ([!], [*], [ ]) se precisar de indicadores visuais.

        💡 Reaproveite `formatacao.formatar_brl` do M01 em vez de
           reimplementar.
        """
        # TODO
        raise NotImplementedError


class FormatadorCSV:
    """CSV pronto para abrir no Excel brasileiro."""

    extensao = "csv"

    def __init__(self, delimitador: str = ";") -> None:
        # TODO
        # 💡 O Excel em PT-BR espera ";", porque a vírgula é o separador
        #    decimal. Com "," ele joga tudo numa coluna só.
        raise NotImplementedError

    def formatar(self, titulo: str, dados: dict | list) -> str:
        # TODO
        # 💡 Use csv.writer com io.StringIO em vez de montar a string na
        #    mão — ele cuida de aspas e escapes que você vai esquecer.
        raise NotImplementedError


class FormatadorJSON:
    """JSON estruturado, para outro sistema consumir."""

    extensao = "json"

    def __init__(self, indent: int = 2) -> None:
        # TODO
        raise NotImplementedError

    def formatar(self, titulo: str, dados: dict | list) -> str:
        # TODO
        # ⚠️ ensure_ascii=False — senão "São Paulo" vira "São Paulo"
        # ⚠️ dataclasses não são serializáveis: use dataclasses.asdict()
        #    ou um `default=` customizado
        # ⚠️ Enum precisa virar .value
        # ⚠️ Arredonde valores monetários AQUI — não adianta o JSON
        #    carregar 2599.9000000000005
        raise NotImplementedError


class FormatadorMarkdown:
    """Tabela Markdown, para colar em PR, wiki ou README."""

    extensao = "md"

    def formatar(self, titulo: str, dados: dict | list) -> str:
        # TODO
        # 💡 Alinhamento à direita em Markdown: |---:| na linha separadora
        raise NotImplementedError


class FormatadorHTML:
    """(Desafio extra) Tabela HTML com CSS embutido."""

    extensao = "html"

    def formatar(self, titulo: str, dados: dict | list) -> str:
        # TODO (opcional)
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Destinos
# ═══════════════════════════════════════════════════════════════

class DestinoConsole:
    """Imprime na tela.

    ⚠️ Este é o ÚNICO lugar do sistema onde `print` é aceitável.
       Em qualquer outro módulo, use `logging`.
    """

    def __init__(self, largura_maxima: int | None = None) -> None:
        # TODO
        raise NotImplementedError

    def entregar(self, conteudo: str, nome: str) -> None:
        # TODO
        raise NotImplementedError


class DestinoArquivo:
    """Grava em disco."""

    def __init__(self, pasta: Path | str = "saida") -> None:
        # TODO: guardar a pasta e criá-la com mkdir(parents=True, exist_ok=True)
        raise NotImplementedError

    def entregar(self, conteudo: str, nome: str) -> None:
        # TODO
        # ⚠️ encoding="utf-8" sempre
        # 💡 registre um log.info com o caminho e o tamanho gravado
        raise NotImplementedError


class DestinoMemoria:
    """Guarda em um dicionário, sem tocar no disco.

    🎯 ESTA CLASSE EXISTE PARA OS TESTES.

    No Módulo 12 você vai escrever:

        destino = DestinoMemoria()
        ServicoRelatorio(agregador, FormatadorCSV(), destino).gerar()
        assert "Campinas" in destino.arquivos["faturamento.csv"]

    Sem tocar em disco, sem limpar arquivos depois, sem problema de
    permissão no CI. É por isso que injeção de dependência importa.
    """

    def __init__(self) -> None:
        # TODO: self.arquivos: dict[str, str] = {}
        raise NotImplementedError

    def entregar(self, conteudo: str, nome: str) -> None:
        # TODO
        raise NotImplementedError

    def __getitem__(self, nome: str) -> str:
        """Permite `destino["relatorio.csv"]`."""
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        # TODO
        raise NotImplementedError


class DestinoMultiplo:
    """Entrega para vários destinos de uma vez.

    💡 Isto é o padrão *Composite*: um destino que contém destinos, e
       satisfaz o mesmo Protocol. Quem usa não sabe a diferença.

           DestinoMultiplo(DestinoConsole(), DestinoArquivo())
    """

    def __init__(self, *destinos) -> None:
        # TODO
        raise NotImplementedError

    def entregar(self, conteudo: str, nome: str) -> None:
        # TODO
        # ⚠️ Se um destino falhar, os outros devem receber mesmo assim.
        #    Colete os erros e reporte no final.
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Registro de formatadores (desafio extra: sistema de plugins)
# ═══════════════════════════════════════════════════════════════

FORMATADORES: dict[str, type] = {}


def registrar_formatador(nome: str):
    """Decorador que cataloga um formatador.

    💡 Repare: este decorador NÃO altera a classe. Ele apenas a registra
       e devolve intacta. É um uso de decorador que muita gente desconhece.

    Uso:
        @registrar_formatador("yaml")
        class FormatadorYAML:
            extensao = "yaml"
            def formatar(self, titulo, dados): ...

    Ganhos:
        • `--formato` da CLI valida contra FORMATADORES
        • `--listar-formatos` funciona sozinho
        • adicionar um formato não exige editar a CLI
    """
    # TODO
    raise NotImplementedError


def criar_formatador(nome: str, **opcoes):
    """Fábrica: devolve uma instância a partir do nome.

    🔴 Valide `nome` contra FORMATADORES antes de usar. Aceitar entrada
       do usuário sem lista branca é como o M03 fazia com nome de tabela.
    """
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: montar dados fictícios e imprimir a MESMA tabela nos 4
    #       formatos, para conferir visualmente. Depois prove que
    #       `isinstance(FormatadorCSV(), Formatador)` é True — mesmo
    #       sem a classe herdar de nada.
    pass
