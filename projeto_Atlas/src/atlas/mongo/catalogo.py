"""Catálogo de produtos — MongoDB.

**Por que o catálogo saiu do relacional:**

    "O catálogo muda toda semana. Entrou cadeira gamer: altura regulável,
     tipo de espuma, peso suportado. Semana passada foram fones, com
     impedância e tipo de conexão. Não dá para pedir uma migração de
     banco a cada categoria nova."

🎯 **A MODELAGEM É HÍBRIDA — e essa é a decisão mais importante deste arquivo.**

    Campos ESTÁVEIS (todo produto tem)  →  raiz do documento
        _id (sku), nome, categoria, preco, custo, estoque, ativo, tags

    Campos VARIÁVEIS (dependem da categoria)  →  subdocumento `specs`
        ram_gb, tela_pol, peso_max_kg, impedancia_ohm, comprimento_m...

    ⚠️ Não jogue tudo em `specs`. O que é consultado, filtrado e
       agregado com frequência merece ficar na raiz, onde o índice é
       barato e a consulta é direta.

       **A pergunta que decide:** *todo produto tem esse campo?*
"""

from __future__ import annotations

import logging
from typing import Any, Iterator

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════
#  Validação de schema (o Mongo permite, e você deveria usar)
# ═══════════════════════════════════════════════════════════════

# TODO: definir o $jsonSchema da coleção.
#
# 💭 "Mas MongoDB não é sem schema?" É sem schema OBRIGATÓRIO. Isso não
#    significa que você deva abrir mão de qualquer garantia.
#
#    O validador abaixo garante o mínimo (sku, nome, categoria, preço)
#    e deixa `specs` completamente livre — que é exatamente o que você
#    quer: rigor onde há estabilidade, liberdade onde há variação.
#
# ESQUEMA_PRODUTO = {
#     "$jsonSchema": {
#         "bsonType": "object",
#         "required": ["_id", "nome", "categoria", "preco", "custo"],
#         "properties": {
#             "_id":       {"bsonType": "string", "description": "SKU"},
#             "nome":      {"bsonType": "string", "minLength": 3},
#             "categoria": {"bsonType": "string"},
#             "preco":     {"bsonType": ["double", "decimal"], "minimum": 0},
#             "custo":     {"bsonType": ["double", "decimal"], "minimum": 0},
#             "estoque":   {"bsonType": "int", "minimum": 0},
#             "ativo":     {"bsonType": "bool"},
#             "tags":      {"bsonType": "array", "items": {"bsonType": "string"}},
#             "specs":     {"bsonType": "object"},   # ← livre, de propósito
#         },
#     }
# }
#
# ⚠️ O validador só age em documentos NOVOS ou atualizados. Os que já
#    existiam continuam como estavam — igual ao CHECK que você adiciona
#    numa tabela já populada (M03).

ESQUEMA_PRODUTO: dict[str, Any] = {}  # TODO


class RepositorioCatalogo:
    """Acesso ao catálogo. Todo o PyMongo do sistema vive aqui.

    🎯 Mesma disciplina do `repositorio.py` (M03): a camada acima não
       sabe que existe MongoDB. Se amanhã o catálogo voltar para o
       Postgres em JSONB, só este arquivo muda.
    """

    def __init__(self, cliente, banco: str = "atlas_catalogo",
                 colecao: str = "produtos") -> None:
        # TODO: guardar cliente, db e a coleção
        raise NotImplementedError

    # ── Estrutura ────────────────────────────────────────────
    def criar_colecao(self, com_validacao: bool = True) -> None:
        """Cria a coleção com $jsonSchema, se ainda não existir.

        💡 `create_collection(nome, validator=ESQUEMA_PRODUTO)`.
           Se já existir, use `db.command("collMod", ...)` para
           aplicar o validador sem recriar.
        """
        # TODO
        raise NotImplementedError

    def criar_indices(self) -> None:
        """Cria os índices do catálogo.

        ⚠️ REGRA: nenhum índice sem justificativa escrita. A mesma
           disciplina do `indices.sql` do M03.

        Sugestões (justifique cada uma):
          • categoria              → filtro mais comum
          • (categoria, preco)     → listagem ordenada por preço
          • tags                   → multichave, para busca por tag
          • ativo                  → 🤔 vale? Tem só 2 valores...
                                      (revise cardinalidade, M03)
          • specs.$**              → 🎯 índice curinga: indexa TODOS os
                                      campos de specs, mesmo os que
                                      ainda não existem
          • nome (text)            → busca textual

        💡 O **índice curinga** (`{"specs.$**": 1}`) é a resposta do
           Mongo ao problema do schema variável: você não precisa saber
           de antemão quais atributos existirão.

           ⚠️ Ele é maior e mais lento de manter que um índice
              específico. Meça antes de adotar.
        """
        # TODO
        raise NotImplementedError

    # ── Escrita ──────────────────────────────────────────────
    def upsert(self, produto: dict) -> str:
        """Insere ou atualiza pelo SKU. IDEMPOTENTE.

        Returns:
            O SKU.

        ⚠️ Use `$set` com o documento, não `replace_one` — a menos que
           você QUEIRA apagar campos que não vieram no payload.

        💭 Decisão sutil: se o payload não traz `specs.gpu` e o
           documento tem, você remove ou preserva? As duas respostas
           são defensáveis. Escolha, documente e seja consistente.
        """
        # TODO
        raise NotImplementedError

    def upsert_muitos(self, produtos: list[dict]) -> dict[str, int]:
        """Upsert em lote.

        💡 Use `bulk_write` com `UpdateOne(..., upsert=True)`. Fazer N
           chamadas de `update_one` é uma ida à rede por documento —
           a mesma lição do `executemany` no M03.

        Returns:
            {"inseridos": n, "atualizados": n}
        """
        # TODO
        raise NotImplementedError

    def ajustar_estoque(self, sku: str, delta: int) -> bool:
        """Soma `delta` ao estoque (negativo = baixa).

        Returns:
            False se não havia estoque suficiente.

        ⚠️ Use `$inc` com um filtro que garanta o saldo:

            update_one({"_id": sku, "estoque": {"$gte": -delta}},
                       {"$inc": {"estoque": delta}})

           Fazer `find` → checar em Python → `update` é uma **race
           condition**: dois processos leem 5, ambos aprovam a baixa de
           5, e o estoque vai a -5.

           O filtro dentro do update torna a operação **atômica**.
           É o mesmo raciocínio da aula 04_06.
        """
        # TODO
        raise NotImplementedError

    def desativar(self, sku: str) -> bool:
        """Soft delete — marca como inativo em vez de remover.

        💭 Mesma decisão do M03: produto removido quebraria o histórico
           de pedidos que o referenciam. E agora o risco é maior, porque
           o Postgres não tem FK para cá — nada avisaria.
        """
        # TODO
        raise NotImplementedError

    # ── Leitura ──────────────────────────────────────────────
    def buscar_por_sku(self, sku: str) -> dict | None:
        # TODO
        raise NotImplementedError

    def buscar_muitos_por_sku(self, skus: list[str]) -> dict[str, dict]:
        """Busca vários de uma vez, devolvendo {sku: produto}.

        🎯 ESTA FUNÇÃO EXISTE PARA EVITAR N+1 ENTRE OS DOIS BANCOS.

           Ao montar um relatório, você tem 200 itens de pedido, cada um
           com um SKU. Chamar `buscar_por_sku` 200 vezes são 200 idas ao
           Mongo — o mesmo problema que o `selectinload` resolve no ORM,
           só que atravessando bancos.

           Uma consulta com `{"_id": {"$in": skus}}` resolve.

        ⚠️ Cuidado com listas gigantes: `$in` com 100.000 SKUs é uma
           consulta enorme. Quebre em lotes de ~1.000.
        """
        # TODO
        raise NotImplementedError

    def buscar(self, filtros: dict | None = None, texto: str | None = None,
               ordenar: str = "nome", limite: int = 50,
               pular: int = 0) -> list[dict]:
        """Busca com filtros dinâmicos.

        Args:
            filtros: pode misturar campos da raiz e de `specs`.
                     Ex.: {"categoria": "Notebooks", "specs.ram_gb": {"$gte": 16}}

        🔴 SEGURANÇA — NoSQL injection existe:

           Se `filtros` vier direto do usuário (query string da API),
           alguém pode enviar `{"$where": "..."}` ou `{"preco": {"$gt": ""}}`
           e vazar a coleção inteira.

           **Valide as chaves contra uma lista branca**, exatamente como
           você fez com nome de tabela no M03.

           ⚠️ Rejeite qualquer chave que comece com `$` vinda de fora.
        """
        # TODO
        raise NotImplementedError

    def contar(self, filtros: dict | None = None) -> int:
        # TODO
        # 💡 `count_documents({})` varre a coleção. Para o total
        #    aproximado, `estimated_document_count()` é instantâneo.
        raise NotImplementedError

    # ── Agregações ───────────────────────────────────────────
    def facetas(self) -> dict:
        """Contadores para os filtros laterais de uma listagem.

        Deve devolver, em UMA consulta (`$facet`):
          • contagem por categoria
          • faixas de preço (`$bucket`)
          • tags mais comuns
          • total de produtos ativos
        """
        # TODO
        raise NotImplementedError

    def inventario_atributos(self) -> list[dict]:
        """Quais atributos existem em `specs`, e onde.

        🎯 ESTA É A CONSULTA MAIS IMPORTANTE DE UM BANCO SEM SCHEMA.

           Num banco relacional, `\\d tabela` responde "quais campos
           existem". Aqui, a única fonte de verdade é o próprio dado.

           Use `$objectToArray` + `$unwind` + `$group` (aula 05_03).

        Returns:
            [{"atributo": "ram_gb", "produtos": 12, "categorias": [...],
              "tipos": ["int"]}, ...]

        💡 Rode isto ao herdar qualquer base MongoDB de outra pessoa.
        """
        # TODO
        raise NotImplementedError

    def resumo_por_categoria(self) -> list[dict]:
        """Contagem, preço médio, estoque e valor imobilizado."""
        # TODO
        raise NotImplementedError

    def sem_giro(self, skus_vendidos: set[str]) -> list[dict]:
        """Produtos que nunca venderam.

        ⚠️ Repare na assinatura: a lista de SKUs vendidos vem de FORA,
           porque os pedidos estão no PostgreSQL.

           **Esse é o custo concreto da persistência poliglota:** o que
           era um `LEFT JOIN ... WHERE IS NULL` (M03) agora exige duas
           consultas e uma junção em Python.

           Documente isso em `docs/ARQUITETURA_DADOS.md`. É o tipo de
           coisa que se descobre tarde demais quando não é discutida.
        """
        # TODO
        raise NotImplementedError

    # ── Qualidade ────────────────────────────────────────────
    def verificar_integridade(self, skus_referenciados: set[str]) -> dict:
        """Encontra inconsistências entre os dois bancos.

        Deve reportar:
          • SKUs referenciados por pedidos que NÃO existem no catálogo
          • Produtos com preço abaixo do custo
          • Produtos ativos sem estoque
          • Documentos que violam o $jsonSchema (se aplicado depois)
          • Categorias com grafias divergentes

        🎯 Sem chave estrangeira entre os bancos, esta função é a
           ÚNICA rede de segurança. Rode-a periodicamente — no M09 ela
           vira um job agendado com alerta.
        """
        # TODO
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: conectar, criar índices, inserir 3 produtos de categorias
    #       diferentes e imprimir o inventário de atributos.
    pass
