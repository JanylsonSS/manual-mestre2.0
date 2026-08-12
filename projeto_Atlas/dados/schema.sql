-- ═══════════════════════════════════════════════════════════════
--  Atlas — Schema relacional da Aurora Comércio
--  Módulo 03 · SQLite
--
--  Este arquivo é o ESQUELETO. Você deve completá-lo.
--
--  Como aplicar:
--      sqlite3 dados/atlas.db < dados/schema.sql
--  ou, pelo Python:
--      conexao.executescript(Path("dados/schema.sql").read_text())
--
--  ⚠️ Antes de escrever qualquer CREATE TABLE, desenhe o diagrama ER
--     em docs/MODELAGEM.md. Cinco minutos de desenho economizam
--     horas de refatoração.
-- ═══════════════════════════════════════════════════════════════


-- ── Configuração da conexão ──────────────────────────────────
-- 🔴 O SQLite vem com chaves estrangeiras DESLIGADAS por padrão,
--    por compatibilidade histórica. Sem esta linha, todas as suas
--    FKs viram decoração e o banco aceita pedidos de clientes
--    inexistentes.
PRAGMA foreign_keys = ON;

-- WAL: leitores não bloqueiam o escritor. Primeira configuração
-- que se liga em qualquer SQLite de produção.
PRAGMA journal_mode = WAL;


-- ═══════════════════════════════════════════════════════════════
--  TABELA: categorias
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar a tabela `categorias` com:
--   - id           PK artificial (INTEGER PRIMARY KEY autoincrementa sozinho)
--   - nome         texto obrigatório e ÚNICO
--   - margem_alvo  real, padrão 0.25, com CHECK entre 0 e 1
--
-- 💭 Pergunta a responder em docs/MODELAGEM.md:
--    por que `nome` é UNIQUE mas NÃO é a chave primária?


-- ═══════════════════════════════════════════════════════════════
--  TABELA: produtos
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar a tabela `produtos` com:
--   - id            PK artificial
--   - sku           texto obrigatório e ÚNICO
--   - nome          texto obrigatório
--   - categoria_id  FK -> categorias(id)
--   - preco         real, obrigatório, CHECK >= 0
--   - custo         real, obrigatório, CHECK >= 0
--   - estoque       inteiro, padrão 0, CHECK >= 0
--   - ativo         inteiro, padrão 1, CHECK IN (0,1)   [SQLite não tem BOOLEAN]
--   - deletado_em   texto, opcional (soft delete)
--   - CHECK de tabela: preco >= custo
--
-- ⚠️ Qual ação referencial para categoria_id?
--    RESTRICT impede apagar uma categoria que tem produtos.
--    CASCADE apagaria os produtos junto — quase certamente errado.
--    Decida e justifique no documento de modelagem.


-- ═══════════════════════════════════════════════════════════════
--  TABELA: clientes
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar a tabela `clientes` com:
--   - id             PK artificial
--   - nome           obrigatório
--   - email          obrigatório e ÚNICO  [chave natural protegida]
--   - cidade         obrigatório
--   - uf             obrigatório, CHECK: 2 caracteres E maiúsculo
--   - segmento       padrão 'varejo', CHECK IN ('varejo','corporativo')
--   - data_cadastro  obrigatório, padrão date('now')
--   - telefone       opcional
--   - deletado_em    opcional (soft delete)
--
-- 💡 O CHECK de UF: length(uf) = 2 AND uf = upper(uf)
--    Isso garante que ninguém grave 'sp' ou 'Sao Paulo'.


-- ═══════════════════════════════════════════════════════════════
--  TABELA: pedidos
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar a tabela `pedidos` com:
--   - id           PK artificial
--   - cliente_id   FK -> clientes(id)
--   - data_pedido  obrigatório, formato ISO 'AAAA-MM-DD'
--   - status       CHECK IN ('pago','pendente','cancelado')
--   - canal        CHECK IN ('site','app','marketplace')
--   - frete        real, padrão 0, CHECK >= 0
--
-- ⚠️ O SQLite não tem tipo DATE. Guarde como TEXT em ISO 8601
--    ('2026-08-12'): esse formato ordena corretamente como texto,
--    o que 'DD/MM/AAAA' não faz.


-- ═══════════════════════════════════════════════════════════════
--  TABELA: itens_pedido  (resolve o N-N entre pedidos e produtos)
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar a tabela `itens_pedido` com:
--   - id              PK artificial
--   - pedido_id       FK -> pedidos(id)   ON DELETE CASCADE
--   - produto_id      FK -> produtos(id)  ON DELETE RESTRICT
--   - quantidade      inteiro, CHECK > 0
--   - preco_unitario  real, CHECK >= 0
--   - UNIQUE (pedido_id, produto_id)
--
-- 💡 Por que CASCADE em pedido_id e RESTRICT em produto_id?
--    Um item de pedido NÃO EXISTE sem o pedido (composição) —
--    apagar o pedido deve levar os itens junto.
--    Já um produto existe independentemente. Apagá-lo destruiria
--    o histórico de vendas, então o banco deve impedir.
--
-- 💡 Por que UNIQUE (pedido_id, produto_id)?
--    Para que o mesmo produto não apareça duas vezes no mesmo
--    pedido — em vez disso, a quantidade deve ser somada.
--
-- 🔴 PERGUNTA CENTRAL (responda em docs/MODELAGEM.md):
--    Por que esta tabela guarda `preco_unitario` se `produtos`
--    já tem `preco`? Pense no que aconteceria com o relatório de
--    julho se alguém reajustasse o catálogo em agosto.


-- ═══════════════════════════════════════════════════════════════
--  VIEWS
-- ═══════════════════════════════════════════════════════════════
-- TODO: criar `vw_produtos_ativos`
--   Filtra deletado_em IS NULL AND ativo = 1.
--
--   💡 Por que uma view? Porque com soft delete, TODA consulta do
--      sistema precisa lembrar de filtrar os removidos. Esquecer
--      uma é mostrar dado apagado ao usuário. A view embute o
--      filtro de uma vez por todas.

-- TODO: criar `vw_vendas`
--   Junta itens_pedido + pedidos + clientes + produtos + categorias,
--   já com a coluna calculada `total` (quantidade * preco_unitario).
--   Os relatórios consultam esta view em vez de repetir os JOINs.
--
--   Colunas sugeridas:
--     pedido_id, data_pedido, mes, status, canal, frete,
--     cliente_id, cliente, email, cidade, uf, segmento,
--     produto_id, sku, produto, categoria, custo,
--     quantidade, preco_unitario, total, margem


-- ═══════════════════════════════════════════════════════════════
--  Verificação
-- ═══════════════════════════════════════════════════════════════
-- Depois de aplicar, confira com:
--   SELECT type, name FROM sqlite_master ORDER BY type, name;
--   PRAGMA foreign_key_list('itens_pedido');
--   PRAGMA integrity_check;
