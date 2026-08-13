"""Contratos de entrada e saída da API — Pydantic.

🎯 A DISTINÇÃO MAIS IMPORTANTE DESTE MÓDULO

    atlas/orm/modelos.py   SQLAlchemy  →  o que vai ao DISCO
    atlas/api/esquemas.py  Pydantic    →  o que trafega na REDE

São coisas diferentes que por acaso têm campos parecidos. Misturá-las é
exatamente como o `custo` de um produto acaba visível para o marketplace
concorrente.

🔒 REGRA: todo esquema de RESPOSTA é uma lista de permissão explícita.
   Se um campo não está declarado aqui, ele não sai daqui — mesmo que a
   função de rota devolva o objeto inteiro do banco.

Convenção de nomes:

    XBase        campos comuns
    XCriar       entrada do POST   (sem id, sem datas)
    XAtualizar   entrada do PATCH  (TUDO opcional)
    XResposta    saída             (com id e derivados, sem dado interno)
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

# ═══════════════════════════════════════════════════════════════════════
#  Erros
# ═══════════════════════════════════════════════════════════════════════


class Erro(BaseModel):
    """Formato ÚNICO de erro da API.

    💭 Por que padronizar? Porque quem consome a sua API vai escrever
       um `tratarErro(resposta)` só. Se cada rota inventa um formato,
       esse código vira uma árvore de `if`.
    """

    codigo: str
    mensagem: str

    # TODO (opcional): incluir `id_correlacao` para o suporte cruzar
    #       a reclamação do cliente com a linha do log.


class ErroValidacao(BaseModel):
    """Resposta do 422, no mesmo formato dos demais erros."""

    codigo: str = "validacao_falhou"
    mensagem: str = "Os dados enviados são inválidos"
    # TODO: lista de {"campo": "...", "erro": "..."}
    campos: list[dict] = []


# ═══════════════════════════════════════════════════════════════════════
#  Autenticação
# ═══════════════════════════════════════════════════════════════════════


class Token(BaseModel):
    """Resposta do login.

    ⚠️ Os nomes `access_token` e `token_type` são exigidos pela
       especificação OAuth2 — não traduza para português. É a única
       parte da API onde isso acontece.
    """

    access_token: str
    token_type: str = "bearer"
    # TODO: incluir expira_em_minutos, para o cliente saber quando renovar.


class UsuarioResposta(BaseModel):
    """Quem está logado.

    🔒 `senha_hash` NÃO está aqui. Nem `senha`. Nem nunca.
    """

    model_config = ConfigDict(from_attributes=True)

    # TODO: email, nome, papel


# ═══════════════════════════════════════════════════════════════════════
#  Produtos
# ═══════════════════════════════════════════════════════════════════════


class ProdutoBase(BaseModel):
    """Campos comuns a entrada e saída."""

    # TODO: nome (3..120), categoria, preco (> 0)
    #       Adicione um field_validator que colapse espaços do nome.


class ProdutoCriar(ProdutoBase):
    """Corpo do POST /produtos."""

    # TODO: sku (padrão XX-YYYY, sempre maiúsculo), custo (>= 0), estoque (>= 0)
    #
    # ⚠️ O validador que normaliza o sku precisa de mode="before".
    #    Com o mode padrão ("after"), o `pattern` do Field roda ANTES e
    #    rejeita "  nb-dell-15  " sem nunca dar chance à normalização.
    #
    # TODO: model_validator(mode="after") garantindo preco >= custo.
    #       Por que de MODELO e não de campo? Porque a regra precisa
    #       enxergar os dois valores ao mesmo tempo.


class ProdutoAtualizar(BaseModel):
    """Corpo do PATCH /produtos/{sku} — tudo opcional.

    🔴 Na rota, use `model_dump(exclude_unset=True)`. Sem isso, os
       campos não enviados chegam como None e SOBRESCREVEM os valores
       existentes: o cliente pediu para mudar o preço e apagou o nome.
    """

    # TODO: nome, categoria, preco, custo, estoque — todos `| None = None`


class ProdutoResposta(ProdutoBase):
    """🔒 O que o mundo pode ver de um produto."""

    model_config = ConfigDict(from_attributes=True)

    # TODO: sku, estoque, disponivel (derivado de estoque > 0)
    #
    # 🔒 NÃO inclua: custo, fornecedor, observacao_interna, margem.
    #    Se a diretoria precisa da margem, ela usa ProdutoInterno abaixo,
    #    numa rota que exige papel admin.


class ProdutoInterno(ProdutoResposta):
    """🔒 O MESMO produto, com os campos que só o admin vê.

    Este esquema existe para deixar a exceção EXPLÍCITA e auditável.
    A auditoria do `openapi.json` vai encontrá-lo — e você poderá
    apontar a rota que o usa e o papel que ela exige.
    """

    # TODO: custo, margem_pct


class PaginaProdutos(BaseModel):
    """Resposta paginada.

    💭 Por que envelopar em vez de devolver a lista pura? Porque o
       cliente precisa saber o total para desenhar a paginação. Uma
       lista nua obriga a mandar essa informação num cabeçalho, que é
       mais fácil de esquecer.
    """

    total: int
    pagina: int
    por_pagina: int
    itens: list[ProdutoResposta] = []


# ═══════════════════════════════════════════════════════════════════════
#  Pedidos
# ═══════════════════════════════════════════════════════════════════════


class ItemEntrada(BaseModel):
    """Um item do corpo do POST /pedidos."""

    # TODO: sku, quantidade (> 0, <= 1000)
    #
    # 💭 Repare que o cliente NÃO manda o preço. O preço é do catálogo,
    #    no momento da compra. Aceitar preço do cliente é convidar
    #    alguém a comprar um notebook por R$ 0,01.


class PedidoCriar(BaseModel):
    """Corpo do POST /pedidos."""

    # TODO: cliente_email, canal (site|app|marketplace), itens (1..50)
    #
    # TODO: model_validator recusando SKU repetido na mesma lista.


class ItemResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # TODO: sku, nome, quantidade, preco_unitario, subtotal


class PedidoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # TODO: id, cliente_email, canal, status, criado_em, itens, total


# ═══════════════════════════════════════════════════════════════════════
#  Relatórios
# ═══════════════════════════════════════════════════════════════════════


class LinhaFaturamento(BaseModel):
    """Uma linha do relatório de faturamento.

    💡 Este esquema é o mesmo cálculo que você já fez em SQL no M03
       (`dados/consultas/faturamento_por_categoria.sql`) e em Python no
       M01. Agora ele ganha uma terceira apresentação: JSON via HTTP.

       Os três devem dar o MESMO número. Se não derem, um deles tem bug —
       e descobrir qual é um ótimo exercício.
    """

    # TODO: categoria, pedidos, itens, receita, ticket_medio


class ResumoFaturamento(BaseModel):
    # TODO: periodo_inicio, periodo_fim, receita_total, linhas
    pass


# ═══════════════════════════════════════════════════════════════════════
#  Infra
# ═══════════════════════════════════════════════════════════════════════


class Saude(BaseModel):
    """Resposta de `/saude` — usada por Docker, Kubernetes e balanceador.

    ⚠️ Não exponha versão de biblioteca, hostname ou caminho de arquivo
       aqui. Essa rota é pública e é a primeira que um varredor lê.
    """

    status: str = "ok"
    versao: str
    ambiente: str
    # TODO (M08+): incluir a checagem real do banco. Um /saude que
    #       responde "ok" sem tocar no banco engana o orquestrador.
    banco: str | None = None
    verificado_em: datetime | None = Field(default=None)
