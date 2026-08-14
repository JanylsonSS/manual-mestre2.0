"""
Transformação — bronze → prata → ouro.
═══════════════════════════════════════════════════════════════════════

    bronze   como chegou. Não se toca, não se corrige, não se apaga.
    prata    limpo, tipado, deduplicado, validado. Uma linha por fato.
    ouro     agregado, pronto para a pergunta. Pequeno e rápido.

A regra que dá sentido à separação:

    🔴 Toda camada é DERIVÁVEL da anterior.

       Apagar prata e ouro tem que ser seguro: uma rodada os
       reconstrói. Apagar bronze é perda permanente.

    Isso não é organização — é a sua capacidade de responder
    "recalcule março com a regra nova" sem pedir o dado de volta ao
    fornecedor.

───────────────────────────────────────────────────────────────────────
🔴 A regra de ouro do ouro
───────────────────────────────────────────────────────────────────────

    Rodar duas vezes para o mesmo dia produz EXATAMENTE o mesmo ouro.

Não "quase o mesmo". O mesmo — byte a byte, mesmo SHA-256.

Isso proíbe, dentro de uma transformação:

    ❌ datetime.now()      →  recebe a data como PARÂMETRO
    ❌ random / uuid4      →  se precisar de id, derive por hash
    ❌ INSERT sem chave    →  use UPSERT / substitua a partição
    ❌ ordem não definida  →  ordene antes de gravar

A Bateria 3 da lista de exercícios roda o seu pipeline duas vezes e
compara os hashes. Se você usar `datetime.now()` em qualquer lugar
aqui dentro, ela reprova — e está certa.

⚠️  ESQUELETO. Assinaturas e TODOs prontos; os corpos são seus.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

# TODO: import pandas as pd

from atlas.dados.extracao import BRONZE, OURO, PRATA


# ═══════════════════════════════════════════════════════════════════════
#  Bronze → Prata
# ═══════════════════════════════════════════════════════════════════════

def ler_bronze(fonte: str, dia: date) -> Any:
    """Lê a partição do bronze daquela fonte e dia.

    💭 Leia SÓ as colunas que a transformação usa
       (`pd.read_parquet(..., columns=[...])`). Parquet é colunar: ler
       6 de 40 colunas lê ~15% dos bytes. Num arquivo de 2 GB isso é a
       diferença entre 40 segundos e 6.
    """
    # TODO: monte o caminho da partição e leia. Se a partição não
    #       existir, levante um erro CLARO dizendo qual pasta faltou —
    #       não devolva DataFrame vazio, porque um vazio silencioso
    #       vira "faturamento zero" no relatório sem nenhum aviso.
    raise NotImplementedError


def normalizar_colunas(df: Any) -> Any:
    """Renomeia colunas da origem para o vocabulário do Atlas.

    Cada origem chama a mesma coisa de um jeito:

        banco        pedido_id      dt_pedido    vl_unitario
        CSV parceiro NumeroPedido   Data         Valor Unit.
        API          orderId        createdAt    unitPrice

    Aqui todas viram `pedido_id`, `data`, `preco_unitario`.
    """
    # TODO: um dicionário POR FONTE, e a função escolhe pelo nome da
    #       fonte. Não tente adivinhar por heurística ("se contém
    #       'valor' então é preço") — no dia em que a origem criar
    #       "valor_desconto", a heurística acerta a coluna errada e o
    #       relatório sai errado sem erro.
    raise NotImplementedError


def deduplicar(df: Any, chave: str = "pedido_id") -> Any:
    """Remove duplicatas — mantendo a versão MAIS RECENTE.

    🔴 `drop_duplicates(subset="pedido_id")` sem mais nada mantém a
       PRIMEIRA ocorrência. Se o pedido foi cancelado depois de pago, a
       primeira linha diz "pago" e você fatura um pedido cancelado.

       Ordene por `atualizado_em` e fique com a última:

           df.sort_values("atualizado_em").drop_duplicates(
               subset=chave, keep="last")

    ⚠️  E há uma armadilha de segunda ordem, que custou uma aula
        inteira (10_05): deduplicar ANTES do portão de qualidade
        ESCONDE o problema. Se a origem começar a mandar cada pedido
        3×, a dedup conserta em silêncio e a verificação de unicidade
        passa feliz — enquanto a origem está quebrada.

        Por isso: CONTE quantas duplicatas removeu e devolva esse
        número para a qualidade avaliar. Dedup é conserto, e todo
        conserto silencioso precisa deixar rastro.
    """
    # TODO: implemente, e devolva (df_limpo, quantidade_removida).
    raise NotImplementedError


def construir_prata(fonte: str, dia: date) -> Any:
    """bronze → prata, para uma fonte e um dia.

    Ordem das etapas (a ordem importa):

        1. ler_bronze
        2. normalizar_colunas
        3. converter tipos (datas com fuso, Decimal/centavos)
        4. validar com os contratos → aprovadas + quarentena
        5. deduplicar (contando o que removeu)
        6. gravar em prata/, particionado por dia
    """
    # TODO: implemente encadeando as funções acima.
    #
    # 🔑 Devolva um objeto de RESULTADO, não só o DataFrame:
    #
    #       {"df": ..., "rejeitadas": N, "duplicatas": N, "lidas": N}
    #
    #    Quem chama precisa desses números para decidir se publica.
    #    Uma função que devolve só o DataFrame obriga o chamador a
    #    recontar tudo — ou, o mais comum, a não conferir nada.
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Prata → Ouro
# ═══════════════════════════════════════════════════════════════════════

def faturamento_por_cidade(prata: Any) -> Any:
    """A pergunta do Módulo 01, agora em escala.

    🔴 Filtre `status == PAGO` ANTES de somar. Pedido pendente e
       cancelado não é faturamento — e essa decisão precisa estar
       escrita em `docs/METRICAS.md`, porque é ela que faz o seu
       número divergir do número do financeiro.
    """
    # TODO: groupby("cidade").agg(...)
    #
    # ⚠️  `groupby` descarta linhas cuja chave é NaN — silenciosamente.
    #     Se 3% dos pedidos vierem sem cidade, o total do relatório é
    #     3% menor que o total real e NADA avisa.
    #
    #     Use `dropna=False` e trate o grupo NaN explicitamente (ex.:
    #     rotule como "NÃO INFORMADA"). Melhor um relatório com uma
    #     linha feia do que um relatório errado e bonito.
    raise NotImplementedError


def faturamento_mensal(prata: Any) -> Any:
    """Série mensal, para a evolução.

    ⚠️  Em que fuso o mês é fechado? Um pedido de 31/07 às 22h em
        Brasília é 01/08 em UTC. Agrupar em UTC joga ele em agosto e o
        fechamento de julho não bate com o do financeiro.

        Converta para `America/Sao_Paulo` antes de extrair o
        ano/mês — e escreva isso em `docs/METRICAS.md`.
    """
    # TODO: converta o fuso, extraia o período, agrupe.
    raise NotImplementedError


def curva_abc(prata: Any) -> Any:
    """Classifica SKUs em A/B/C por participação acumulada no faturamento."""
    # TODO:
    #   1. some o faturamento por sku
    #   2. ordene decrescente
    #   3. participação acumulada (cumsum / total)
    #   4. A até 80%, B até 95%, C o resto — use pd.cut ou np.select
    raise NotImplementedError


def margem_por_categoria(prata: Any) -> Any:
    """Receita, custo e margem por categoria.

    🔴 A armadilha aritmética: margem do total ≠ média das margens.

           média das margens de 3 produtos = 30%
           margem sobre o total            = 18%

       As duas contas são "a margem". Só uma responde à pergunta que
       a Aurora está fazendo. Calcule
       `(receita_total - custo_total) / receita_total` e diga em
       `docs/METRICAS.md` que é essa.
    """
    # TODO: agregue receita e custo, e só então divida.
    raise NotImplementedError


def construir_ouro(dia: date) -> dict[str, Path]:
    """Lê a prata, produz todos os agregados, grava o ouro.

    Devolve {nome_do_agregado: caminho_do_arquivo}.
    """
    # TODO: implemente.
    #
    # 🔴 Grave de forma DETERMINÍSTICA — a Bateria 3 confere o hash:
    #
    #     1. ordene as linhas antes de gravar (sort_values)
    #     2. ordene as colunas também
    #     3. reset_index(drop=True) — o índice vai para o parquet
    #     4. NÃO grave "gerado_em" DENTRO do parquet (muda o hash a
    #        cada rodada); ponha num `_manifesto.json` ao lado
    #
    # 🔴 E publique de forma ATÔMICA: escreva num diretório temporário
    #    e só então mova para o lugar (`os.replace`). Sem isso, quem
    #    ler o ouro no meio da escrita lê um parquet truncado — é o
    #    mesmo símbolo atômico do deploy do M09, aplicado a dado.
    raise NotImplementedError
