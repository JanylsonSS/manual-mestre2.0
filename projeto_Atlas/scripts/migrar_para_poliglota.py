#!/usr/bin/env python3
"""Migra o Atlas do SQLite (M03/M04) para PostgreSQL + MongoDB.

    SQLite  ──┬──►  PostgreSQL   clientes, pedidos, itens
              └──►  MongoDB      catálogo de produtos

🎯 REQUISITO CENTRAL: IDEMPOTÊNCIA.

   Rodar 1, 2 ou 10 vezes deixa os dois bancos no mesmo estado.

   Por que isso importa tanto aqui: agora são DOIS destinos. A migração
   pode falhar depois de gravar no Postgres e antes de gravar no Mongo,
   deixando os bancos inconsistentes. Sem idempotência, cada falha vira
   uma limpeza manual — e agora em dois lugares.

Uso:
    python scripts/migrar_para_poliglota.py
    python scripts/migrar_para_poliglota.py --origem dados/atlas.db
    python scripts/migrar_para_poliglota.py --apenas catalogo
    python scripts/migrar_para_poliglota.py --conferir

Código de saída: 0 se tudo bateu, 1 se houve divergência.
"""

from __future__ import annotations

import sys
from pathlib import Path

# TODO: imports do atlas (o pacote deve estar instalado com pip install -e .)


# ═══════════════════════════════════════════════════════════════
#  Extração — do SQLite
# ═══════════════════════════════════════════════════════════════

def ler_sqlite(caminho: Path) -> dict[str, list[dict]]:
    """Lê todas as tabelas do banco antigo.

    Returns:
        {"clientes": [...], "produtos": [...], "pedidos": [...],
         "itens_pedido": [...]}

    💡 Use `row_factory = sqlite3.Row` e converta para dict — você já
       fez isso no M03.

    ⚠️ Para bases grandes, leia em lotes com um gerador (aula 04_02)
       em vez de carregar tudo na memória.
    """
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Carga — PostgreSQL
# ═══════════════════════════════════════════════════════════════

def carregar_clientes(sessao, clientes: list[dict]) -> dict[str, int]:
    """Carrega clientes, de forma idempotente.

    Returns:
        {"inseridos": n, "atualizados": n}

    💡 Duas abordagens:
       (a) Buscar por e-mail e decidir insert/update — 2 idas ao banco
       (b) `INSERT ... ON CONFLICT (email) DO UPDATE` — 1 ida

       No SQLAlchemy 2.0, a (b) fica:
           from sqlalchemy.dialects.postgresql import insert
           stmt = insert(Cliente).values(...)
           stmt = stmt.on_conflict_do_update(index_elements=["email"],
                                             set_={...})

       ⚠️ O `insert` com `on_conflict_do_update` é ESPECÍFICO do dialeto.
          Se quiser rodar também em SQLite, importe de
          `sqlalchemy.dialects.sqlite`. Este é um dos poucos lugares em
          que a portabilidade do SQLAlchemy vaza.
    """
    # TODO
    raise NotImplementedError


def carregar_pedidos(sessao, pedidos: list[dict], itens: list[dict],
                     mapa_clientes: dict[int, int]) -> dict[str, int]:
    """Carrega pedidos e seus itens.

    Args:
        mapa_clientes: id antigo → id novo (podem diferir)

    ⚠️ ORDEM IMPORTA: clientes antes de pedidos, pedidos antes de itens.
       As FKs do Postgres vão recusar a ordem errada — e isso é bom.

    💡 Para volume grande, use `session.bulk_insert_mappings()` ou o
       `COPY` do Postgres, que é ordens de grandeza mais rápido que
       INSERTs individuais.
    """
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Carga — MongoDB
# ═══════════════════════════════════════════════════════════════

def montar_documento_produto(linha: dict) -> dict:
    """Converte uma linha da tabela `produtos` num documento.

    🎯 AQUI ACONTECE A DECISÃO DE MODELAGEM.

       A linha do SQLite é plana:
           {id, sku, nome, categoria, preco, custo, estoque}

       O documento é híbrido:
           {_id: sku, nome, categoria, preco, custo, estoque, ativo,
            tags: [...], specs: {...}}

       ⚠️ O SQLite não tem os `specs` — eles não existiam. Você precisa
          decidir o que fazer:

          (a) Deixar `specs: {}` e preencher depois, manualmente
          (b) Inferir alguns a partir do nome do produto
          (c) Ler de uma planilha auxiliar que o comercial mantém

       Escolha uma, documente, e **registre no log** quantos produtos
       ficaram sem specs. Esse número é uma dívida conhecida, não um
       detalhe a esconder.
    """
    # TODO
    raise NotImplementedError


def carregar_catalogo(repositorio, produtos: list[dict]) -> dict[str, int]:
    """Carrega o catálogo no MongoDB, de forma idempotente.

    💡 Use `upsert_muitos` (bulk_write) em vez de N chamadas.
    """
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Verificação
# ═══════════════════════════════════════════════════════════════

def conferir(origem: dict, sessao, repositorio) -> dict:
    """Compara a origem com os dois destinos.

    Deve verificar:
      • Contagem de cada entidade
      • Faturamento total (a métrica que não pode mudar)
      • Nenhum SKU referenciado em `itens_pedido` está ausente do catálogo
      • Nenhum pedido órfão

    Returns:
        {"ok": bool, "divergencias": [...]}

    ⚠️ A terceira verificação é a que só existe por causa da arquitetura
       poliglota. No modelo anterior, a FK garantia isso. Agora é este
       script.
    """
    # TODO
    raise NotImplementedError


def testar_idempotencia(caminho_origem: Path) -> bool:
    """Roda a migração duas vezes e compara o estado.

    🎯 Critério de aceitação da Etapa 6 do roteiro.
    """
    # TODO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Entrada
# ═══════════════════════════════════════════════════════════════

def main(argv: list[str] | None = None) -> int:
    """Orquestra a migração.

    Fluxo:
      1. Parsear argumentos
      2. Verificar que os dois bancos respondem  ← falhe cedo
      3. Ler o SQLite
      4. Carregar no PostgreSQL (em transação)
      5. Carregar no MongoDB
      6. Conferir
      7. Relatar

    ⚠️ Verifique a conexão dos DOIS antes de começar. Descobrir que o
       Mongo está fora depois de carregar 200 mil linhas no Postgres é
       uma tarde perdida.

    💡 Instrumente com o `Monitor` do M04: cada etapa vira uma etapa
       cronometrada, com métricas no log JSON.
    """
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
