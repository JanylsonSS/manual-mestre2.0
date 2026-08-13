"""Pedidos.

🔴 Este é o arquivo mais importante do módulo — e o único cujo erro
   custa dinheiro de verdade.
"""

from fastapi import APIRouter

# TODO: importar status, esquemas e dependências

roteador = APIRouter(prefix="/pedidos", tags=["Pedidos"])


# ═══════════════════════════════════════════════════════════════════════
#  POST /pedidos  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.post("", response_model=PedidoResposta,
#                    status_code=status.HTTP_201_CREATED,
#                    responses={409: {"model": Erro}})
#     def criar(dados: PedidoCriar, operador: OperadorDep, sessao: SessaoDep):
#         pedido = servicos.criar_pedido(sessao, dados)
#         return servicos.montar_resposta_pedido(pedido)
#
# Repare no tamanho: duas linhas. TODA a lógica abaixo mora em
# `atlas/servicos.py` — que não importa `fastapi` e por isso pode ser
# chamado também por um worker de fila ou pela CLI.
#
# ═══ 🔴 O REQUISITO QUE DEFINE ESTA ROTA: ATOMICIDADE ═══
#
# Um pedido com 3 itens onde o TERCEIRO não tem estoque **não pode**
# alterar o estoque dos dois primeiros.
#
# Por que isso é fácil de errar? Porque o laço natural é:
#
#     for item in dados.itens:
#         produto = buscar(item.sku)
#         produto.estoque -= item.quantidade      # ← já mexeu
#         if produto.estoque < 0: raise ...        # ← tarde demais
#
# As duas primeiras iterações já baixaram o estoque. Se você levantar a
# exceção agora e não desfizer, o sistema "perdeu" mercadoria: o cliente
# recebeu um erro, o pedido não existe, e o estoque está errado.
#
# 💭 E o pior: NADA falha. Não há exceção, não há log, não há alerta.
#    A descoberta acontece no inventário do fim do mês, quando já não dá
#    para saber qual pedido causou.
#
# ═══ O DESENHO CORRETO ═══
#
#   1. VALIDE TUDO antes de alterar QUALQUER coisa.
#      Percorra os itens acumulando problemas numa lista, sem escrever.
#
#   2. Se houver problemas → `sessao.rollback()` e levante a exceção de
#      domínio com TODOS eles de uma vez.
#      (Devolver um problema por vez força o cliente a N tentativas.)
#
#   3. Só então aplique as baixas e faça UM `commit`.
#
# 🔑 Quem chama `commit` é o SERVIÇO, nunca o repositório. Só o serviço
#    sabe que "criar pedido" significa *baixar estoque de 3 produtos E
#    inserir 4 linhas*, tudo ou nada. Se o repositório commitasse a cada
#    `add`, essa atomicidade seria impossível de obter.
#
# ⚠️ AINDA FALTA UMA COISA: mesmo com a transação, dois pedidos
#    simultâneos do último item podem ambos ler `estoque = 1` e ambos
#    passar na validação. A transação garante *tudo ou nada*, não
#    *exclusividade*.
#
#    As saídas são um `SELECT ... FOR UPDATE` (bloqueio pessimista), uma
#    coluna de versão (otimista) ou uma CHECK constraint `estoque >= 0`
#    no banco. Escolha uma e escreva a justificativa em docs/API.md.
#
# TODO: implementar `criar`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /pedidos  — autenticado
# ═══════════════════════════════════════════════════════════════════════
#
# Filtros: status, cliente_email, período. Com paginação.
#
# 🔴 O PROBLEMA N+1 MORA AQUI. Listar 20 pedidos e acessar
#    `pedido.itens` de cada um dispara 1 consulta para os pedidos + 20
#    para os itens + 20×N para os produtos. Em desenvolvimento, com 3
#    pedidos, ninguém percebe. Em produção, a página trava.
#
#    A correção você viu no M05:
#
#        select(Pedido).options(
#            selectinload(Pedido.itens).selectinload(ItemPedido.produto))
#
#    Meça: rode com `echo=True` no engine, conte as consultas com e sem.
#
# TODO: implementar `listar`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /pedidos/{pedido_id}  — autenticado
# ═══════════════════════════════════════════════════════════════════════
#
# 🔴 PERGUNTA DE SEGURANÇA QUE VOCÊ PRECISA RESPONDER:
#
#    Qualquer usuário autenticado pode ver QUALQUER pedido, só trocando
#    o número na URL?
#
#    Se sim, você tem uma **BOLA** — Broken Object Level Authorization —
#    o item nº 1 do OWASP API Security Top 10. É a falha mais comum em
#    APIs reais, e a mais fácil de explorar: um laço de 1 a 100000.
#
#    Autenticação responde "quem é você". Autorização de OBJETO responde
#    "este registro é seu". São coisas diferentes, e a segunda é quase
#    sempre esquecida.
#
#    Na Aurora, provavelmente todo funcionário pode ver todo pedido — e
#    está tudo bem, DESDE QUE seja uma decisão consciente e escrita.
#    Registre-a em docs/API.md.
#
# TODO: implementar `obter`, e documentar a decisão de autorização.


# ═══════════════════════════════════════════════════════════════════════
#  PATCH /pedidos/{pedido_id}/status  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
# 💭 Nem toda transição é válida. `cancelado → pago` não deveria existir,
#    e `pago → cancelado` precisa DEVOLVER o estoque.
#
#    Uma máquina de estados explícita:
#
#        TRANSICOES = {
#            "pendente":  {"pago", "cancelado"},
#            "pago":      {"enviado", "cancelado"},
#            "enviado":   {"entregue"},
#            "entregue":  set(),
#            "cancelado": set(),
#        }
#
#    ...transforma "achei que não podia" em 409 com mensagem clara.
#    Isso é regra de negócio: mora em `atlas/regras.py`, não aqui.
#
# TODO: implementar (opcional, mas recomendado).
