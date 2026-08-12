-- ═══════════════════════════════════════════════════════════════
--  Atlas — Índices
--  Módulo 03
--
--  ⚠️ REGRA: nenhum índice entra aqui sem um comentário dizendo
--     QUAL consulta ele acelera. Índice sem justificativa é peso
--     morto: ocupa disco e torna todo INSERT/UPDATE mais lento.
--
--  Aplique DEPOIS do schema.sql e DEPOIS da carga inicial —
--  criar índices antes de uma carga grande deixa a carga mais lenta.
-- ═══════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════════════════════════
--  1. Chaves estrangeiras
-- ═══════════════════════════════════════════════════════════════
-- 📌 O SQLite (como a maioria dos bancos) cria índice automático
--    para PRIMARY KEY e UNIQUE — mas NÃO para FOREIGN KEY.
--    Este é o índice esquecido mais comum e a causa nº 1 de
--    JOIN lento em sistemas reais.

-- TODO: índice em pedidos(cliente_id)
--   Acelera: JOIN pedidos->clientes, e "todos os pedidos do cliente X"

-- TODO: índice em itens_pedido(pedido_id)
--   Acelera: JOIN itens->pedidos (usado em TODOS os relatórios)

-- TODO: índice em itens_pedido(produto_id)
--   Acelera: JOIN itens->produtos, ranking de produtos

-- TODO: índice em produtos(categoria_id)
--   Acelera: agregação por categoria


-- ═══════════════════════════════════════════════════════════════
--  2. Colunas filtradas com frequência
-- ═══════════════════════════════════════════════════════════════

-- TODO: índice em pedidos(data_pedido)
--   Acelera: filtros por período e agrupamento por mês
--
--   ⚠️ Atenção: strftime('%Y-%m', data_pedido) NÃO usa este índice,
--      porque a função é aplicada sobre a coluna. Se o agrupamento
--      mensal for crítico, considere um índice de expressão:
--          CREATE INDEX ... ON pedidos(strftime('%Y-%m', data_pedido));

-- TODO: índice COMPOSTO em pedidos(status, data_pedido)
--   Acelera: "pedidos pagos de julho" — o caso mais comum do Atlas
--
--   💡 A ORDEM importa (regra do prefixo mais à esquerda).
--      Um índice (status, data_pedido) serve para:
--        WHERE status = 'pago'                          ✅
--        WHERE status = 'pago' AND data > '2026-07-01'  ✅
--        WHERE data > '2026-07-01'                      ❌
--      Coloque primeiro a coluna usada com IGUALDADE,
--      depois a usada com INTERVALO.


-- ═══════════════════════════════════════════════════════════════
--  3. Índices parciais
-- ═══════════════════════════════════════════════════════════════
-- Indexam só um subconjunto das linhas: menores, mais rápidos e
-- mais baratos de manter.

-- TODO: índice parcial em pedidos(data_pedido) WHERE status = 'pago'
--   Como ~80% dos relatórios só olham pedidos pagos, um índice que
--   contém APENAS eles é bem menor que um índice completo.

-- TODO: índice parcial em produtos(categoria_id) WHERE deletado_em IS NULL
--   Só os produtos vivos entram — que são os únicos consultados.


-- ═══════════════════════════════════════════════════════════════
--  4. Índices que você NÃO deve criar (e por quê)
-- ═══════════════════════════════════════════════════════════════
-- ❌ produtos(ativo)
--    Só tem dois valores (0 e 1). O índice não consegue eliminar
--    quase nada — o banco vai preferir varrer a tabela. Baixa
--    cardinalidade = índice inútil.
--
-- ❌ categorias(qualquer coisa)
--    A tabela tem meia dúzia de linhas. Varrê-la é mais rápido
--    que consultar um índice.
--
-- ❌ clientes(nome)
--    Não filtramos por nome exato em lugar nenhum. E busca por
--    "contém" (LIKE '%x%') não usa índice de qualquer forma.


-- ═══════════════════════════════════════════════════════════════
--  Verificação
-- ═══════════════════════════════════════════════════════════════
-- TODO: para CADA índice criado acima, rode um EXPLAIN QUERY PLAN
--       antes e depois, e cole o resultado em docs/MODELAGEM.md.
--
--   Exemplo:
--     EXPLAIN QUERY PLAN
--     SELECT * FROM pedidos WHERE status = 'pago'
--       AND data_pedido >= '2026-07-01';
--
--   O que procurar na saída:
--     SCAN tabela                     -> 🔴 varreu tudo
--     SEARCH tabela USING INDEX ...   -> ✅ usou o índice
--     USING COVERING INDEX            -> ✅✅ nem tocou na tabela
--
-- Listar tudo que existe:
--   SELECT name, tbl_name FROM sqlite_master WHERE type = 'index';
--   PRAGMA index_list('pedidos');
