"""
Extração — de onde o dado vem, e como saber onde a última rodada parou.
═══════════════════════════════════════════════════════════════════════

Três origens, três problemas diferentes:

    banco  →  muito dado, e não pode pesar no OLTP
    CSV    →  encoding, separador decimal, data em pt-BR
    API    →  paginação, limite de taxa, indisponibilidade

E um problema que é dos três: **como não reprocessar tudo toda noite?**

A resposta é a marca d'água (aula 10_04).

───────────────────────────────────────────────────────────────────────
🔴 A armadilha da marca d'água que você VAI cair se não pensar
───────────────────────────────────────────────────────────────────────

Ingenuamente:

    ultima = ler_marca()                  # 2026-08-13 22:00:00
    novos  = SELECT * WHERE atualizado_em > ultima
    salvar_marca(agora())                 # 2026-08-13 23:00:00

Parece certo. Perde dado.

Um pedido gravado às 22:59:58 mas cuja transação só fez COMMIT às
23:00:01 tem `atualizado_em = 22:59:58` — antes da nova marca — e
nunca mais será visto por `> 23:00:00`.

Duas defesas, e você vai implementar as duas:

    1. Margem de segurança: use `marca - X minutos` como limite
       inferior. Reprocessa um pouco. Por isso a etapa seguinte
       precisa ser idempotente (UPSERT, não INSERT).

    2. Marca d'água = MAIOR VALOR VISTO NO LOTE, não `agora()`.
       Se o lote trouxe até 22:58:03, a marca é 22:58:03.

───────────────────────────────────────────────────────────────────────

⚠️  ESQUELETO. Assinaturas e TODOs prontos; os corpos são seus.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator

# TODO: importe pandas aqui quando for usar.
#       import pandas as pd


# ═══════════════════════════════════════════════════════════════════════
#  Onde as coisas ficam
# ═══════════════════════════════════════════════════════════════════════

RAIZ = Path(__file__).resolve().parents[3]
LAGO = RAIZ / "dados" / "lago"

BRONZE = LAGO / "bronze"
PRATA = LAGO / "prata"
OURO = LAGO / "ouro"
QUARENTENA = LAGO / "quarentena"
ESTADO = LAGO / "estado"

# 🔴 Margem de segurança da marca d'água. Leia o bloco no topo do
#    arquivo antes de reduzir esse número.
MARGEM_SEGURANCA = timedelta(minutes=15)


# ═══════════════════════════════════════════════════════════════════════
#  Marca d'água
# ═══════════════════════════════════════════════════════════════════════

def caminho_marca(fonte: str) -> Path:
    """Onde fica a marca d'água de uma fonte.

    Uma marca POR FONTE. Se o CSV falhar, a extração do banco não deve
    reprocessar por causa disso.
    """
    # TODO: devolva ESTADO / f"marca_{fonte}.json"
    #       Não crie o arquivo aqui — só monte o caminho.
    raise NotImplementedError


def ler_marca(fonte: str, padrao: datetime | None = None) -> datetime:
    """Lê a marca d'água da fonte. Se não existir, devolve `padrao`.

    O `padrao` é a data da primeira carga — a partir de quando o
    histórico interessa.
    """
    # TODO:
    #   1. Se o arquivo não existe, devolva `padrao` (ou uma data bem
    #      antiga, tipo datetime(2020, 1, 1, tzinfo=timezone.utc)).
    #   2. Se existe, leia o JSON e devolva o campo como datetime.
    #
    # 🔴 Salve e leia SEMPRE em UTC com timezone explícito. Uma marca
    #    d'água ingênua ("2026-08-13 23:00:00", sem fuso) reprocessa ou
    #    perde exatamente 3 horas de pedidos no horário de verão.
    #    Use datetime.fromisoformat() e confira que .tzinfo não é None.
    raise NotImplementedError


def salvar_marca(fonte: str, valor: datetime) -> None:
    """Grava a marca d'água — de forma ATÔMICA.

    🔴 Se o processo morrer no meio do write, o arquivo fica truncado e
       a próxima rodada não consegue ler a marca. Escreva num arquivo
       temporário e renomeie: `os.replace()` é atômico no mesmo
       sistema de arquivos. (É o mesmo truque do symlink do M09.)
    """
    # TODO:
    #   1. tmp = caminho.with_suffix(".json.tmp")
    #   2. tmp.write_text(json.dumps({"marca": valor.isoformat(), ...}))
    #   3. os.replace(tmp, caminho)
    #
    #   Grave também `atualizado_em` e `linhas` — na madrugada em que o
    #   pipeline errar, você vai querer saber quando essa marca foi
    #   escrita e quantas linhas a produziram.
    raise NotImplementedError


def janela(fonte: str, ate: datetime | None = None) -> tuple[datetime, datetime]:
    """Devolve (inicio, fim) da janela a extrair, já com a margem.

    Retorna `(ler_marca(fonte) - MARGEM_SEGURANCA, ate or agora)`.
    """
    # TODO: implemente. É uma função de três linhas e é o coração da
    #       ingestão incremental — escreva um teste para ela.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Bronze — gravar o dado COMO ELE CHEGOU
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class Lote:
    """Um lote extraído, com tudo que é preciso para auditá-lo depois."""

    fonte: str
    dados: Any                  # TODO: tipe como pd.DataFrame
    inicio: datetime
    fim: datetime
    linhas: int = 0
    origem_detalhe: str = ""    # a query, a URL, o nome do arquivo


def particao_bronze(fonte: str, dia: date) -> Path:
    """Caminho particionado no bronze.

    O layout é `bronze/origem=<fonte>/data_ingestao=<AAAA-MM-DD>/`.

    💭 Por que esse formato esquisito com `=`? Porque é o padrão que
       Spark, DuckDB, Athena e Polars entendem: a pasta VIRA COLUNA na
       leitura. `SELECT ... WHERE data_ingestao = '2026-08-13'` lê UMA
       pasta em vez de varrer o lago inteiro.
    """
    # TODO: monte e devolva o Path. Crie os diretórios com
    #       mkdir(parents=True, exist_ok=True).
    raise NotImplementedError


def gravar_bronze(lote: Lote, dia: date | None = None) -> Path:
    """Grava o lote no bronze, em Parquet, com manifesto.

    🔴 A regra do bronze é: **não transforme nada**. Nem renomeie
       coluna, nem conserte data, nem tire espaço. O bronze é a sua
       única chance de responder "o que exatamente o fornecedor mandou
       naquele dia?" quando a regra de negócio mudar em novembro e
       você precisar recalcular março.
    """
    # TODO:
    #   1. pasta = particao_bronze(lote.fonte, dia or date.today())
    #   2. lote.dados.to_parquet(pasta / "dados.parquet", index=False)
    #   3. escreva o manifesto (função abaixo)
    #   4. devolva o caminho do parquet
    raise NotImplementedError


def escrever_manifesto(pasta: Path, lote: Lote, arquivo: Path) -> None:
    """Grava `_manifesto.json` ao lado dos dados.

    O manifesto é o que transforma "um parquet numa pasta" em "um lote
    auditável". Sem ele, daqui a seis meses você olha o arquivo e não
    sabe de que query ele veio nem se está completo.
    """
    # TODO: grave um JSON com, no mínimo:
    #
    #       fonte, linhas, janela_inicio, janela_fim,
    #       extraido_em (UTC), origem_detalhe,
    #       sha256 do arquivo, bytes, colunas (lista)
    #
    # 🔑 O sha256 não é paranoia: é como você prova que o parquet não
    #    foi alterado depois — e como a Bateria 3 da lista de
    #    exercícios detecta um pipeline não-idempotente.
    raise NotImplementedError


def sha256_arquivo(caminho: Path, bloco: int = 1 << 20) -> str:
    """SHA-256 de um arquivo, lendo em blocos.

    Em blocos porque `read_bytes()` de um parquet de 2 GB carrega 2 GB
    na memória — e o pipeline roda numa máquina de 4 GB.
    """
    # TODO: use hashlib.sha256() e um laço `while pedaco := f.read(bloco)`
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Origem 1 — o banco
# ═══════════════════════════════════════════════════════════════════════

def extrair_banco(inicio: datetime, fim: datetime,
                  tamanho_pagina: int = 50_000) -> Lote:
    """Extrai pedidos do banco transacional na janela dada.

    🔴 Três regras, e as três já custaram caro para alguém:

        1. Use a RÉPLICA de leitura, não o primário. Um `SELECT` de 4
           milhões de linhas segura conexões e derruba o checkout.

        2. Pagine. `pd.read_sql(...)` sem `chunksize` traz tudo para a
           memória de uma vez. Use `chunksize=` e concatene, ou melhor:
           grave cada pedaço.

        3. `ORDER BY` numa coluna estável junto com a paginação. Sem
           ordem definida, "página 2" pode repetir ou pular linhas
           entre as consultas.
    """
    # TODO:
    #   1. Monte a query com parâmetros (:inicio, :fim) — NUNCA com
    #      f-string. Você aprendeu isso no M03 e vale igual aqui.
    #   2. Leia em páginas.
    #   3. Devolva um Lote com origem_detalhe = a query (sem os dados).
    #
    #   Reaproveite a sessão de `atlas.orm.sessao` (M05) — mas aponte
    #   para a URL da réplica, que deve ser uma variável de ambiente
    #   SEPARADA (ATLAS_BANCO_REPLICA_URL). Se ela não estiver
    #   definida, FALHE com mensagem clara em vez de cair no primário
    #   silenciosamente.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Origem 2 — o CSV que o parceiro manda
# ═══════════════════════════════════════════════════════════════════════

def extrair_csv(caminho: Path) -> Lote:
    """Lê um CSV de parceiro — no formato brasileiro.

    O arquivo que a Aurora recebe tem, ao mesmo tempo:

        separador de campo    ;
        separador decimal     ,        (1.234,56)
        separador de milhar   .
        encoding              latin-1  (ou cp1252, ou utf-8-sig)
        data                  31/07/2026
        cabeçalho             na linha 3, com duas linhas de lixo antes

    🔴 O erro que produz número errado sem erro nenhum: ler
       "1.234,56" com o padrão americano. O pandas não reclama — ele
       lê a coluna como TEXTO, seu `sum()` vira concatenação ou vira
       NaN, e o faturamento sai errado sem uma linha de traceback.
    """
    # TODO:
    #   pd.read_csv(caminho,
    #               sep=";", decimal=",", thousands=".",
    #               encoding=?, skiprows=?, dayfirst=True, ...)
    #
    #   Sobre o encoding: NÃO chute. Tente na ordem
    #   ["utf-8-sig", "utf-8", "cp1252", "latin-1"] e pare no primeiro
    #   que não levantar UnicodeDecodeError.
    #
    #   ⚠️  latin-1 NUNCA levanta erro — ele decodifica qualquer byte.
    #       Por isso ele tem que ser o ÚLTIMO da lista. Se você o
    #       colocar antes, "Ação" vira "AÃ§Ã£o" e nada avisa.
    #
    #   Depois de ler: CONFIRA os dtypes. Se uma coluna que devia ser
    #   float veio como object, aborte. Não siga com dado suspeito.
    raise NotImplementedError


def detectar_encoding(caminho: Path,
                      tentativas: tuple[str, ...] = (
                          "utf-8-sig", "utf-8", "cp1252", "latin-1")) -> str:
    """Devolve o primeiro encoding que decodifica o arquivo inteiro."""
    # TODO: implemente o laço. Leia o arquivo em modo binário uma vez e
    #       teste `bytes.decode(enc)` para cada candidato.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Origem 3 — a API do parceiro
# ═══════════════════════════════════════════════════════════════════════

def extrair_api(inicio: datetime, fim: datetime) -> Lote:
    """Puxa dados da API do parceiro, paginando.

    Reaproveite `atlas.integracoes.cliente_http` (M07): ele já tem
    timeout, retry com backoff e circuit breaker. Não escreva outro.

    🔴 Paginação por offset (`?pagina=2`) DUPLICA e PERDE linhas quando
       a base muda durante a varredura. Se a API oferecer cursor
       (`?depois=<id>`), use cursor. Se só houver offset, ordene por
       uma coluna imutável (o id, não a data de atualização).
    """
    # TODO:
    #   1. Laço de paginação, com um teto de páginas para não girar
    #      para sempre se a API devolver sempre a mesma página.
    #   2. Respeite `Retry-After` no 429.
    #   3. Junte as páginas num único DataFrame.
    #   4. origem_detalhe = a URL base (SEM a chave de API!).
    #
    # 🔴 Ao gravar origem_detalhe no manifesto, tire token/chave da
    #    URL. O manifesto vai para o lago e o lago é lido por muita
    #    gente. É a mesma lição do `docker history` do M08.
    raise NotImplementedError


def paginar(url: str, parametros: dict, teto: int = 1000) -> Iterator[dict]:
    """Gerador que devolve uma página por vez.

    Gerador e não lista: com 1000 páginas de 50 mil linhas, uma lista
    é o processo morrendo por falta de memória. (Foi para isto que
    serviu o M04 · Aula 02.)
    """
    # TODO: implemente com `yield`.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  O passo completo
# ═══════════════════════════════════════════════════════════════════════

def extrair_tudo(dia: date, apenas: list[str] | None = None) -> dict[str, Path]:
    """Roda as três extrações e grava o bronze. Devolve {fonte: caminho}.

    🔑 Uma fonte que falha NÃO deve impedir as outras. Colete as
       exceções, siga adiante, e só ao final decida se o pipeline
       continua — a decisão é da orquestração, não daqui.
    """
    # TODO:
    #   Para cada fonte:
    #     1. inicio, fim = janela(fonte)
    #     2. lote = extrair_*(...)
    #     3. caminho = gravar_bronze(lote, dia)
    #     4. 🔴 salvar_marca(fonte, MAIOR data vista no lote) — e SÓ
    #        depois de gravar_bronze retornar com sucesso.
    #
    #        Se você salvar a marca antes de gravar, uma falha no
    #        disco faz o dado sumir para sempre: a marca já avançou e
    #        a próxima rodada não vai buscá-lo. Marca d'água é commit,
    #        e commit vem por último.
    raise NotImplementedError
