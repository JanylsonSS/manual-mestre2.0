"""Camada de acesso a dados — todo o SQL do Atlas mora aqui.

**Por que uma camada separada?**

1. **SQL em um lugar só.** Quando o schema mudar, você tem um arquivo
   para revisar, não trinta.
2. **Segurança auditável.** Se toda consulta está aqui, garantir que
   todas são parametrizadas é uma revisão de um arquivo.
3. **Troca de banco.** No Módulo 05 migramos para PostgreSQL. Só este
   módulo muda — `metricas.py` e `relatorios.py` continuam idênticos.
4. **Testabilidade.** No Módulo 12 você vai substituir esta camada por
   uma versão em memória para testar o resto sem banco.

🔴 **REGRA INEGOCIÁVEL DESTE ARQUIVO:**
   Toda consulta que recebe dado externo usa `?` ou `:nome`.
   Zero f-strings com valores. Zero concatenação. Sem exceção.

   Um único `f"... WHERE id = {id}"` neste arquivo reprova o projeto.
"""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from atlas import config


# ═══════════════════════════════════════════════════════════════
#  Conexão e transação
# ═══════════════════════════════════════════════════════════════


@contextmanager
def conectar(caminho: Path | str | None = None) -> Iterator[sqlite3.Connection]:
    """Abre uma conexão configurada e garante o fechamento.

    Args:
        caminho: Arquivo do banco. Se None, usa config.ARQUIVO_BANCO.

    Yields:
        A conexão pronta para uso.

    Configurações obrigatórias em TODA conexão nova:
        PRAGMA foreign_keys = ON    -> sem isto, as FKs não valem nada
        PRAGMA journal_mode = WAL   -> leitores não bloqueiam o escritor
        row_factory = sqlite3.Row   -> acesso por NOME da coluna

    💡 Use como:
        with conectar() as conexao:
            ...

    ⚠️ O `finally` do try é o que garante o `close()` mesmo se o
       bloco `with` levantar exceção. Sem ele, um erro vaza conexões
       até o processo esgotar os descritores de arquivo.
    """
    # TODO: implementar
    raise NotImplementedError


@contextmanager
def transacao(conexao: sqlite3.Connection) -> Iterator[sqlite3.Connection]:
    """Commit no sucesso, rollback em qualquer exceção.

    💡 Use como:
        with transacao(conexao):
            conexao.execute(...)
            conexao.execute(...)
        # commit automático aqui

    ⚠️ O `raise` depois do rollback é essencial. Sem ele, o erro é
       engolido e quem chamou acha que deu tudo certo.
    """
    # TODO: implementar
    #   try: yield conexao; conexao.commit()
    #   except: conexao.rollback(); raise
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Schema
# ═══════════════════════════════════════════════════════════════


def criar_schema(conexao: sqlite3.Connection, recriar: bool = False) -> None:
    """Aplica dados/schema.sql (e opcionalmente apaga tudo antes).

    Args:
        conexao: Conexão aberta.
        recriar: Se True, dropa todas as tabelas antes de recriar.
            ⚠️ Isso APAGA TODOS OS DADOS. Exija confirmação na CLI.

    💡 Leia o arquivo com Path.read_text(encoding="utf-8") e aplique
       com conexao.executescript(). O executescript aceita vários
       comandos separados por ponto e vírgula.
    """
    # TODO: implementar
    raise NotImplementedError


def criar_indices(conexao: sqlite3.Connection) -> None:
    """Aplica dados/indices.sql.

    ⚠️ Chame DEPOIS da carga inicial. Criar índices antes de inserir
       muitos dados deixa a inserção mais lenta, porque cada linha
       precisa atualizar cada índice.
    """
    # TODO: implementar
    raise NotImplementedError


def schema_existe(conexao: sqlite3.Connection) -> bool:
    """Verifica se as tabelas principais já foram criadas."""
    # TODO: consultar sqlite_master
    #   SELECT COUNT(*) FROM sqlite_master
    #   WHERE type='table' AND name IN (...)
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Escrita — UPSERTs idempotentes
# ═══════════════════════════════════════════════════════════════
# Todas as funções abaixo devem poder rodar N vezes com a mesma
# entrada e deixar o banco no mesmo estado. Isso é o que torna a
# migração re-executável sem medo.


def upsert_categoria(conexao: sqlite3.Connection, nome: str,
                     margem_alvo: float = 0.25) -> int:
    """Insere a categoria se não existir; devolve o id em qualquer caso.

    Returns:
        O id da categoria.

    💡 Duas abordagens:
       (a) INSERT ... ON CONFLICT (nome) DO NOTHING, depois um
           SELECT para pegar o id
       (b) INSERT ... ON CONFLICT (nome) DO UPDATE SET nome = nome
           RETURNING id     [SQLite 3.35+]

       A (b) é uma ida ao banco em vez de duas. O `DO UPDATE SET
       nome = nome` parece inútil, mas é um truque: o `DO NOTHING`
       não dispara o RETURNING, o `DO UPDATE` dispara.
    """
    # TODO: implementar — PARAMETRIZADO
    raise NotImplementedError


def upsert_produto(conexao: sqlite3.Connection, sku: str, nome: str,
                   categoria_id: int, preco: float, custo: float,
                   estoque: int = 0) -> int:
    """Insere ou atualiza um produto pelo SKU. Devolve o id."""
    # TODO: implementar — PARAMETRIZADO
    #   ON CONFLICT (sku) DO UPDATE SET nome=..., preco=..., ...
    #   Use `excluded.coluna` para referenciar os valores que
    #   tentaram ser inseridos.
    raise NotImplementedError


def upsert_cliente(conexao: sqlite3.Connection, nome: str, email: str,
                   cidade: str, uf: str, segmento: str = "varejo",
                   data_cadastro: str | None = None) -> int:
    """Insere ou atualiza um cliente pelo e-mail. Devolve o id.

    ⚠️ O e-mail é a chave natural. Normalize (`.strip().lower()`)
       ANTES de gravar — senão 'Maria@X.com' e 'maria@x.com' viram
       dois clientes, que é exatamente a dor que o M03 veio resolver.
    """
    # TODO: implementar — PARAMETRIZADO
    raise NotImplementedError


def inserir_pedido(conexao: sqlite3.Connection, pedido_id: int | None,
                   cliente_id: int, data_pedido: str, status: str,
                   canal: str, frete: float = 0.0) -> int:
    """Insere um pedido. Se `pedido_id` vier do CSV, use-o como PK.

    Devolve o id do pedido.

    💡 Usar o id do arquivo de origem como PK é o que torna a carga
       idempotente: reprocessar o mesmo arquivo atualiza em vez de
       duplicar. Combine com ON CONFLICT (id) DO UPDATE.

    💡 Para pegar o id gerado quando pedido_id é None:
       conexao.execute("SELECT last_insert_rowid()").fetchone()[0]
       (ou use RETURNING id, se o SQLite for 3.35+)
    """
    # TODO: implementar — PARAMETRIZADO
    raise NotImplementedError


def inserir_itens(conexao: sqlite3.Connection, pedido_id: int,
                  itens: list[tuple[int, int, float]]) -> int:
    """Insere os itens de um pedido em lote.

    Args:
        itens: lista de (produto_id, quantidade, preco_unitario)

    Returns:
        Quantos itens foram inseridos.

    💡 Use `executemany`. Ele é MUITO mais rápido que N chamadas a
       `execute` — e a diferença cresce com o volume.

    ⚠️ Lembre-se do UNIQUE (pedido_id, produto_id). Se o mesmo
       produto aparecer duas vezes na lista, você precisa somar as
       quantidades ANTES de inserir, ou usar ON CONFLICT DO UPDATE
       somando.
    """
    # TODO: implementar — PARAMETRIZADO
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Leitura
# ═══════════════════════════════════════════════════════════════


def executar_consulta(conexao: sqlite3.Connection, sql: str,
                      parametros: tuple | dict = ()) -> list[dict]:
    """Executa uma consulta e devolve lista de dicionários.

    Args:
        sql: A consulta. Pode vir de um arquivo .sql.
        parametros: Valores para os placeholders.

    Returns:
        Lista de dicts (uma chave por coluna).

    💡 Com row_factory = sqlite3.Row configurado em conectar(),
       basta fazer [dict(linha) for linha in cursor.fetchall()].
    """
    # TODO: implementar
    raise NotImplementedError


def executar_arquivo_sql(conexao: sqlite3.Connection, caminho: Path,
                         parametros: tuple | dict = ()) -> list[dict]:
    """Lê uma consulta de um arquivo .sql e executa.

    💡 Por que SQL em arquivo separado? Porque assim o analista de
       negócio consegue ler e ajustar a consulta sem tocar em Python,
       e você consegue testá-la direto no cliente do banco.

    ⚠️ Valide que o arquivo está dentro de config.DIR_CONSULTAS.
       Aceitar um caminho arbitrário vindo da CLI é uma brecha de
       path traversal.
    """
    # TODO: implementar
    raise NotImplementedError


def contar(conexao: sqlite3.Connection, tabela: str) -> int:
    """Conta as linhas de uma tabela.

    🔴 ATENÇÃO — ARMADILHA DE SEGURANÇA:
       Nome de tabela NÃO pode ser parametrizado com `?`. O
       placeholder só funciona para VALORES, porque a estrutura da
       consulta precisa ser conhecida na compilação.

       Isso NÃO significa que você pode concatenar livremente.
       Valide contra uma LISTA BRANCA:

           if tabela not in config.TABELAS:
               raise ValueError(f"tabela desconhecida: {tabela}")

       Só depois monte a string. É a única exceção legítima à regra
       de nunca concatenar — e ela exige a lista branca.
    """
    # TODO: implementar com lista branca
    raise NotImplementedError


def estatisticas_banco(conexao: sqlite3.Connection) -> dict[str, int]:
    """Contagem de linhas de todas as tabelas do modelo.

    Útil para o comando `python main.py status` e para verificar
    idempotência: rode a migração duas vezes e compare.
    """
    # TODO: implementar
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Qualidade de dados
# ═══════════════════════════════════════════════════════════════


def verificar_integridade(conexao: sqlite3.Connection) -> dict:
    """Roda checagens de sanidade no banco.

    Deve verificar pelo menos:
        - PRAGMA integrity_check      (corrupção física)
        - PRAGMA foreign_key_check    (FKs violadas)
        - Pedidos sem nenhum item
        - Produtos com preco < custo
        - Clientes com e-mail duplicado ignorando maiúsculas
        - Itens com preco_unitario muito distante do preco do produto

    Returns:
        Dict com o resultado de cada verificação.

    💭 Por que isso importa? Porque constraint garante o presente,
       não o passado. Se o banco foi carregado antes de você adicionar
       um CHECK, os dados antigos podem violá-lo. E `foreign_key_check`
       encontra órfãos criados enquanto o PRAGMA estava desligado.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: um teste rápido — conectar, criar schema, contar tabelas.
    #       Rode com: python src/atlas/repositorio.py
    pass
