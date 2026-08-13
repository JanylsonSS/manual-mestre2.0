"""Catálogo de produtos.

🎯 Cada rota aqui tem DOIS contratos:
   - de acesso  (qual papel pode chamar)   → a dependência
   - de saída   (quais campos saem)        → o response_model

Os dois são declarativos. Nenhum `if usuario.papel == ...` no corpo.
"""

from fastapi import APIRouter

# TODO: importar status; os esquemas; e as dependências
#       (SessaoDep, UsuarioDep, OperadorDep, AdminDep,
#        PaginacaoDep, OrdenacaoDep, filtros_produto)

roteador = APIRouter(prefix="/produtos", tags=["Produtos"])


# ═══════════════════════════════════════════════════════════════════════
#  GET /produtos  — autenticado
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.get("", response_model=PaginaProdutos)
#     def listar(usuario: UsuarioDep, sessao: SessaoDep,
#                pag: PaginacaoDep, ord_: OrdenacaoDep,
#                filtros: Annotated[dict, Depends(filtros_produto)]):
#
# ⚠️ ORDEM DAS ROTAS. Se você criar um `GET /produtos/destaques`,
#    declare-o ANTES de `GET /produtos/{sku}`. O FastAPI casa a primeira
#    rota compatível: com a ordem invertida, "destaques" chega como se
#    fosse um sku e você recebe um 404 confuso.
#
# 🔴 A contagem total precisa de uma consulta separada (`SELECT COUNT`),
#    não de `len(lista_paginada)`. Parece óbvio escrito assim; erra-se
#    muito na prática.
#
# TODO: implementar `listar`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /produtos/{sku}  — autenticado
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.get("/{sku}", response_model=ProdutoResposta,
#                   responses={404: {"model": Erro}})
#
# 💡 O `responses={}` não muda o comportamento — ele documenta. Quem lê
#    o /docs passa a saber que 404 é uma resposta prevista, e o gerador
#    de cliente cria o tipo certo.
#
# TODO: implementar `obter`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /produtos/{sku}/interno  — 🔒 admin
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.get("/{sku}/interno", response_model=ProdutoInterno)
#     def ver_interno(sku: str, admin: AdminDep, sessao: SessaoDep):
#
# 🎯 O MESMO produto, outro contrato de saída. Esta é a resposta certa
#    para "a diretoria precisa ver a margem": não é adicionar `custo`
#    ao ProdutoResposta e filtrar com um `if`, é uma rota separada com
#    um esquema separado e uma exigência de papel.
#
#    A diferença aparece na auditoria: um esquema chamado ProdutoInterno
#    numa rota que exige admin é uma decisão registrada. Um `if` no meio
#    de uma função é uma decisão esquecida.
#
# TODO: implementar `ver_interno`.


# ═══════════════════════════════════════════════════════════════════════
#  POST /produtos  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.post("", response_model=ProdutoResposta,
#                    status_code=status.HTTP_201_CREATED,
#                    responses={409: {"model": Erro}})
#
# 🔴 201, não 200. E, se quiser ser rigoroso, com um cabeçalho
#    `Location: /produtos/{sku}` apontando para o recurso criado.
#
# 🔴 SKU duplicado é 409 (Conflict), não 400 nem 422. O corpo está
#    perfeitamente bem formado — o problema é o ESTADO do servidor.
#
# ⚠️ Há uma corrida aqui: dois POSTs simultâneos com o mesmo SKU podem
#    passar os dois pelo "já existe?" antes de qualquer um inserir. A
#    checagem em Python não basta — quem garante é a constraint UNIQUE
#    no banco (você a criou no M03). Capture o IntegrityError e traduza
#    para 409.
#
# TODO: implementar `criar`.


# ═══════════════════════════════════════════════════════════════════════
#  PATCH /produtos/{sku}  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
# 🔴 `dados.model_dump(exclude_unset=True)`. Sem isso, mudar só o preço
#    apaga o nome — os campos não enviados chegam como None.
#
# ⚠️ Sutileza: `exclude_unset` diferencia "não enviou" de "enviou null".
#    Se o cliente manda {"observacao": null} querendo LIMPAR o campo,
#    `exclude_unset` preserva essa intenção; `exclude_none` a perderia.
#
# ⚠️ Corpo vazio ({}) merece 400 com "nenhum campo enviado" — devolver
#    200 sem alterar nada esconde um bug do cliente.
#
# TODO: implementar `atualizar`.


# ═══════════════════════════════════════════════════════════════════════
#  DELETE /produtos/{sku}  — 🔒 admin
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.delete("/{sku}", status_code=status.HTTP_204_NO_CONTENT)
#
# ⚠️ 204 significa "sem conteúdo" — a função não pode devolver nada.
#    Se você retornar um dicionário, o FastAPI reclama.
#
# 💭 QUESTÃO DE DESENHO: um produto com pedidos históricos pode ser
#    apagado? Se apagar, os pedidos antigos ficam órfãos e o relatório
#    de faturamento do ano passado muda.
#
#    A resposta quase sempre é EXCLUSÃO LÓGICA: uma coluna `ativo` que
#    vira False. O produto some das listagens e continua existindo para
#    os pedidos que o referenciam.
#
#    Decida, implemente e escreva a justificativa em docs/API.md.
#
# TODO: implementar `remover`.


# ═══════════════════════════════════════════════════════════════════════
#  PATCH /produtos/{sku}/estoque  — 🔐 operador
# ═══════════════════════════════════════════════════════════════════════
#
# Recebe um `delta` (positivo entra, negativo sai).
#
# 💭 Por que `delta` e não `estoque` absoluto? Porque duas pessoas
#    ajustando ao mesmo tempo com valor absoluto sobrescrevem uma à
#    outra ("perdi 10 unidades"), enquanto dois deltas somam
#    corretamente. É o mesmo raciocínio de `UPDATE ... SET x = x - 1`
#    em vez de ler, calcular e gravar.
#
# 🔴 O resultado nunca pode ficar negativo → 409 com quanto há disponível.
#
# TODO: implementar `ajustar_estoque`.
