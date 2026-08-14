#!/usr/bin/env python3
"""
Verificador de camadas — a arquitetura que se prova sozinha.
═══════════════════════════════════════════════════════════════════════

    python scripts/verificar_camadas.py            # verifica
    python scripts/verificar_camadas.py --mapa     # imprime o grafo
    python scripts/verificar_camadas.py --grafo    # em Mermaid, para o doc

───────────────────────────────────────────────────────────────────────
Por que este script existe
───────────────────────────────────────────────────────────────────────

Porque `docs/ARQUITETURA.md` é uma intenção, e intenção não sobrevive a
uma sexta-feira apressada.

Nada no Python impede `from atlas.repositorio import ...` dentro de uma
rota. O código roda. Os testes passam. A camada morreu e ninguém viu.

    🔑 Arquitetura que não é verificada não é arquitetura.

Este script lê os imports de cada módulo **sem executá-los** (via
`ast`), monta o grafo de dependências e reprova quem importa para
cima.

> 💭 Repare que ele usa `ast`, não `import`. Importar para analisar
>    executaria o código de cada módulo — e um módulo que abre conexão
>    com o banco no topo faria o seu verificador de arquitetura
>    precisar de um Postgres no ar. Análise estática lê o texto.

⚠️  ESQUELETO. Assinaturas e TODOs prontos; os corpos são seus.
"""

from __future__ import annotations

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FONTE = RAIZ / "src" / "atlas"


# ═══════════════════════════════════════════════════════════════════════
#  O modelo das camadas
# ═══════════════════════════════════════════════════════════════════════

# Da mais externa (0) para a mais interna. Uma camada pode importar
# qualquer camada com número MAIOR. Nunca menor.
#
# TODO: complete o mapeamento com os módulos do seu projeto. Os que
#       estão aqui vieram de docs/ARQUITETURA.md — confira se batem
#       com o que você realmente construiu.
CAMADAS: dict[str, int] = {
    # 0 · ENTRADA — o mundo fala com o Atlas
    "cli": 0,
    "api": 0,
    "dados": 0,
    # 1 · SERVIÇO — o que o negócio faz
    "servicos": 1,
    "regras": 1,
    "metricas": 1,
    # 2 · ACESSO — onde o dado mora
    "repositorio": 2,
    "orm": 2,
    "mongo": 2,
    "leitura": 2,
    "relatorios_sql": 2,
    # 3 · DOMÍNIO — 🔑 não importa nada de dentro do Atlas
    "modelos": 3,
    "excecoes": 3,
    "validacao": 3,
    # TODO: e estes, em que camada ficam?
    #       apresentacao, relatorios, migracao, integracoes
    #
    #       Não há resposta única — é uma DECISÃO sua. `integracoes/`
    #       é especialmente interessante: ele é ENTRADA (o mundo lá
    #       fora) ou ACESSO (é só outra fonte de dado)? Decida, e
    #       registre num ADR. O verificador vai obrigar você a ser
    #       consistente com o que decidiu.
}

# Números das camadas, para as regras 2 e 3. Ajuste se você mudou a
# numeração acima.
CAMADA_SERVICO = 1
CAMADA_ACESSO = 2
CAMADA_DOMINIO = 3

# Módulos de APOIO: qualquer camada pode importá-los, e eles não podem
# importar ninguém do Atlas.
#
# 💭 Isto não é uma brecha — é uma camada com regra própria. O teste
#    para entrar aqui é rigoroso: sem regra de negócio, sem estado,
#    sem dependência interna. Se `config` começar a importar
#    `modelos`, ele deixou de ser apoio.
APOIO: set[str] = {"config", "formatacao", "observabilidade"}

# Exceções conscientes à regra.
#
# ⚠️  Toda entrada aqui precisa de um comentário dizendo POR QUÊ e,
#     idealmente, do número do ADR que a justifica.
#
#     Uma exceção justificada é engenharia. Um arquivo cheio de
#     exceções sem justificativa é a arquitetura morrendo devagar,
#     com aprovação do CI.
EXCECOES: dict[tuple[str, str], str] = {
    # ("modulo_que_importa", "modulo_importado"): "motivo (ADR NNNN)",
    # TODO: comece VAZIO. Só acrescente quando o verificador acusar
    #       algo e você concluir, honestamente, que a violação é
    #       legítima. Se a primeira coisa que você fizer for encher
    #       este dicionário para o script passar, você escreveu um
    #       verificador decorativo.
}


@dataclass
class Violacao:
    origem: str
    destino: str
    arquivo: Path
    linha: int
    motivo: str


@dataclass
class Grafo:
    """O grafo de dependências internas do Atlas."""

    arestas: dict[str, set[str]] = field(default_factory=dict)
    posicoes: dict[tuple[str, str], tuple[Path, int]] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════════════
#  Leitura
# ═══════════════════════════════════════════════════════════════════════

def modulo_de(caminho: Path) -> str:
    """`src/atlas/api/rotas/produtos.py` → `api`.

    Devolve o nome da CAMADA, não do arquivo: tudo dentro de `api/`
    pertence à camada `api`.
    """
    # TODO: use caminho.relative_to(FONTE).parts e devolva a primeira
    #       parte — ou o nome do arquivo sem `.py`, se estiver na raiz
    #       de `src/atlas/`.
    raise NotImplementedError


def imports_de(caminho: Path) -> list[tuple[str, int]]:
    """Todos os módulos do Atlas importados por este arquivo.

    Devolve [(nome_do_modulo, numero_da_linha), ...].
    """
    # TODO:
    #   arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    #   for no in ast.walk(arvore):
    #       if isinstance(no, ast.ImportFrom): ...   # from atlas.x import y
    #       if isinstance(no, ast.Import): ...       # import atlas.x
    #
    # ⚠️  Três detalhes que fazem o verificador errar em silêncio se
    #     você não tratar:
    #
    #     1. `from atlas import modelos` — o módulo está em `names`,
    #        não em `node.module`.
    #     2. `from .modelos import Pedido` — import RELATIVO. O
    #        `node.module` vem sem o prefixo e `node.level` é 1.
    #        Se você ignorar isso, todo import relativo do projeto
    #        passa despercebido e o verificador aprova tudo.
    #     3. Imports dentro de função (`def f(): from atlas.x import y`)
    #        contam igual — `ast.walk` já os alcança, mas confira.
    raise NotImplementedError


def construir_grafo(fonte: Path = FONTE) -> Grafo:
    """Varre `src/atlas/` e monta o grafo."""
    # TODO: percorra fonte.rglob("*.py"), pule `__init__.py` se quiser,
    #       e acumule as arestas.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Verificação
# ═══════════════════════════════════════════════════════════════════════

def verificar(grafo: Grafo) -> list[Violacao]:
    """Devolve todas as violações da regra das camadas.

    A regra tem TRÊS partes (veja docs/ARQUITETURA.md):

        1. ninguém importa para fora
        2. DOMÍNIO e APOIO são livres para todos
        3. 🔑 ACESSO só pode ser importada por SERVIÇO (ou por ACESSO)
    """
    # TODO:
    #   Para cada aresta origem → destino:
    #     0. origem == destino (mesma camada)? → sempre permitido
    #     1. destino em APOIO ou DOMÍNIO?   → permitido
    #     2. origem em APOIO?               → 🔴 apoio não importa nada
    #     3. (origem, destino) em EXCECOES? → permitido, mas CONTE
    #     4. camada[origem] > camada[destino]? → violação (para fora)
    #     5. 🔑 destino é ACESSO e origem NÃO é SERVIÇO nem ACESSO?
    #        → violação
    #     6. módulo fora de CAMADAS?        → violação de classificação
    #
    # ⚠️  O passo 0 não é firula. Sem ele, `relatorios_sql` importando
    #     `repositorio` — dois módulos de ACESSO conversando — aparece
    #     como violação. Um verificador que reprova código correto é
    #     pior do que nenhum: a primeira coisa que a equipe faz é
    #     aprender a ignorá-lo.
    #
    # ───────────────────────────────────────────────────────────────
    # 🔴 SOBRE O PASSO 5 — não o trate como detalhe
    # ───────────────────────────────────────────────────────────────
    #
    # Sem ele, a regra linear (passo 4) APROVA `api` importando
    # `repositorio`: ENTRADA é camada 0, ACESSO é camada 2, e 0 → 2 é
    # "para dentro".
    #
    # E essa é justamente a violação que dói: a rota chama o banco
    # direto e pula a regra de negócio. Funciona hoje; no dia em que a
    # regra mudar, ela muda em `servicos.py` e continua velha nas
    # rotas que aprenderam a se virar sozinhas.
    #
    # 💭 Este furo não foi encontrado lendo o documento — foi
    #    encontrado plantando uma violação e vendo o verificador
    #    aprovar. Faça o mesmo com o SEU: escreva a regra, plante os
    #    quatro casos da tabela de `docs/ARQUITETURA.md`, e só confie
    #    depois de ver cada um reprovar.
    #
    # ───────────────────────────────────────────────────────────────
    # 🔑 SOBRE O PASSO 6
    # ───────────────────────────────────────────────────────────────
    #
    # É tentador escrever `if modulo not in CAMADAS: continue`.
    # Isso transforma o verificador num carimbo: basta criar um módulo
    # novo para ficar de fora da regra — e módulos novos são
    # exatamente onde a arquitetura costuma vazar.
    #
    # Módulo não classificado é ERRO, não é "tudo bem".
    raise NotImplementedError


def detectar_ciclos(grafo: Grafo) -> list[list[str]]:
    """Ciclos de importação entre módulos.

    🔴 Um ciclo é pior que uma violação de camada: com ciclo, você não
       consegue entender nenhum dos módulos envolvidos sozinho, e não
       consegue testar um sem carregar o outro.

    O Python às vezes tolera ciclos (dependendo da ordem de import) e
    às vezes explode com `ImportError: cannot import name X (most
    likely due to a circular import)`. Tolerar é pior — significa que
    o ciclo está lá, funcionando, esperando a mudança que o quebra.
    """
    # TODO: DFS com marcação de cinza/preto, ou use a ordenação
    #       topológica do M10 (`orquestracao.ordenar`) e capture o erro
    #       de ciclo que ela já levanta. Reaproveite — a lógica é a
    #       mesma, e você já a escreveu.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Saída
# ═══════════════════════════════════════════════════════════════════════

def imprimir_mapa(grafo: Grafo) -> None:
    """Mapa de dependências em texto, agrupado por camada."""
    # TODO: imprima camada por camada, e dentro de cada uma o que ela
    #       importa. É o que você vai colar em docs/ARQUITETURA.md.
    raise NotImplementedError


def imprimir_mermaid(grafo: Grafo) -> None:
    """O grafo em Mermaid, para colar no Markdown.

    💡 O GitHub renderiza blocos ```mermaid direto no README. Um
       diagrama gerado do código está sempre certo; um diagrama
       desenhado à mão está errado desde o segundo commit.
    """
    # TODO: imprima `graph TD` e uma linha `A --> B` por aresta.
    #       Marque as violações com estilo diferente.
    raise NotImplementedError


def relatorio(violacoes: list[Violacao], ciclos: list[list[str]]) -> None:
    """Imprime o resultado de forma acionável."""
    # TODO: para cada violação, mostre ARQUIVO:LINHA. Sem isso, o
    #       desenvolvedor recebe "api importa repositorio" e ainda
    #       precisa caçar onde. Mensagem de erro que não permite agir
    #       é meio erro.
    #
    # 💡 Formato `caminho:linha:` faz o VS Code e o terminal
    #    transformarem a saída em link clicável. É de graça.
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Código de saída: 0 aprovado, 1 há violações."""
    # TODO:
    #   1. argparse com --mapa e --grafo
    #   2. grafo = construir_grafo()
    #   3. se --mapa ou --grafo: imprima e devolva 0
    #   4. violacoes = verificar(grafo); ciclos = detectar_ciclos(grafo)
    #   5. relatorio(...); devolva 1 se houver violação ou ciclo
    #
    # 🔴 O código de saída é o que faz este script valer alguma coisa:
    #    é por ele que o CI reprova o PR. Um verificador que só imprime
    #    bonito e sempre devolve 0 é um verificador que ninguém obedece.
    #
    # 🔑 E antes de considerá-lo pronto: PLANTE UMA VIOLAÇÃO de
    #    propósito (importe `repositorio` dentro de uma rota) e
    #    confirme que ele reprova. Um verificador que você nunca viu
    #    falhar não é um verificador — é uma esperança.
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
