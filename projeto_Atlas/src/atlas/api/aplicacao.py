"""Montagem da aplicação FastAPI.

Este arquivo faz UMA coisa: junta as peças. Nenhuma regra de negócio,
nenhuma consulta, nenhuma validação de domínio.

    criar_app()
      ├── lifespan          abre e fecha recursos
      ├── middlewares       CORS, rastreio, cabeçalhos de segurança
      ├── handlers          exceção de domínio → status HTTP
      └── include_router    autenticacao, produtos, pedidos, relatorios

💭 Por que uma FÁBRICA e não um `app = FastAPI()` no topo?

   Porque um módulo executa uma vez só. Com `app` no nível do módulo,
   todo teste compartilha a mesma instância e a mesma configuração —
   e você não consegue subir uma app de teste com outro banco sem
   truques de monkeypatch.

   Com a fábrica, cada teste chama `criar_app(config_de_teste)` e
   recebe uma aplicação limpa.

Subir:
    uvicorn "atlas.api.aplicacao:criar_app" --factory --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

# TODO: importar Request, status
# TODO: importar CORSMiddleware de fastapi.middleware.cors
# TODO: importar JSONResponse de fastapi.responses
# TODO: importar RequestValidationError de fastapi.exceptions
# TODO: importar obter_config e os routers
# TODO: importar as exceções de atlas.excecoes


# ═══════════════════════════════════════════════════════════════════════
#  Ciclo de vida
# ═══════════════════════════════════════════════════════════════════════
@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    """Roda UMA vez ao subir e UMA vez ao descer.

    Antes do `yield`: abrir recursos — testar a conexão com o banco,
    aquecer cache, validar que a configuração faz sentido.

    Depois: fechar tudo com educação (`motor.dispose()`).

    ⚠️ `Base.metadata.create_all()` é aceitável em aula e em teste. Em
       produção quem cria e altera tabela é o **Alembic** (M05) — o
       `create_all` não sabe fazer migração, só cria o que não existe.
       Ele não vai adicionar uma coluna nova numa tabela existente, e
       você vai passar uma tarde procurando o motivo.

    💡 Uma checagem de conexão aqui faz a aplicação morrer no start-up
       quando o banco está fora — que é MUITO melhor do que subir
       saudável e devolver 500 na primeira requisição do cliente.
    """
    # TODO: startup
    yield
    # TODO: shutdown


# ═══════════════════════════════════════════════════════════════════════
#  Tradução: exceção de domínio → status HTTP
# ═══════════════════════════════════════════════════════════════════════
#
# 🎯 ESTE MAPA É A FRONTEIRA. Acima dele, HTTP. Abaixo, domínio puro.
#
# É o que permite `atlas/servicos.py` não importar `fastapi`: os
# serviços levantam as exceções que você criou lá no M01 e a tradução
# acontece aqui, num lugar só.
#
# TODO: preencher com as exceções de atlas/excecoes.py
#
# MAPA_STATUS = {
#     RecursoNaoEncontrado:  404,
#     RecursoJaExiste:       409,
#     EstoqueInsuficiente:   409,
#     RegraDeNegocioViolada: 422,
#     PermissaoNegada:       403,
# }
#
# ⚠️ 409 vs 422: use 409 quando o problema é o ESTADO do servidor (SKU
#    já existe, estoque acabou) e 422 quando é o CONTEÚDO enviado
#    (preço abaixo do custo). O corpo estava bem formado nos dois casos
#    — por isso nenhum é 400.


def criar_app(config=None) -> FastAPI:
    """Monta e devolve a aplicação.

    Args:
        config: permite injetar uma configuração de teste. Se None,
            usa `obter_config()`.
    """
    # TODO: config = config or obter_config()

    app = FastAPI(
        # TODO: title, version, lifespan
        # TODO: docs_url=None quando config.producao, se você decidiu esconder
        lifespan=ciclo_de_vida,
    )

    # ═══════════════════════════════════════════════════════════════════
    #  Middlewares
    # ═══════════════════════════════════════════════════════════════════
    #
    # ⚠️ A ORDEM É AO CONTRÁRIO DO QUE PARECE.
    #
    #    O ÚLTIMO `add_middleware` fica MAIS PERTO da rota; o primeiro
    #    fica MAIS EXTERNO. Um `@app.middleware("http")` é açúcar para
    #    `add_middleware`, então os decoradores entram na mesma pilha.
    #
    #    Consequência prática: o CORS precisa ser o mais EXTERNO. Senão
    #    uma resposta de erro gerada por outro middleware sai sem os
    #    cabeçalhos CORS — e o front-end vê "blocked by CORS policy"
    #    escondendo o erro real, que era um 500 qualquer.
    #
    # TODO: CORSMiddleware com config.origens_permitidas
    #
    # 🔴 NUNCA allow_origins=["*"] junto com allow_credentials=True. Os
    #    navegadores recusam essa combinação — e com razão: seria abrir
    #    a API autenticada para qualquer site do mundo.
    #
    # ⚠️ E lembre: CORS instrui o NAVEGADOR. `curl`, Postman e qualquer
    #    script Python o ignoram completamente. Quem protege a API é a
    #    autenticação; o CORS protege o USUÁRIO de um site malicioso
    #    usar as credenciais dele contra você.

    # TODO: middleware de rastreio — X-Request-ID e X-Tempo-ms
    #
    #    Preserve o `X-Request-ID` que o cliente enviou, se houver. Isso
    #    permite seguir uma requisição atravessando vários serviços.
    #
    # ⚠️ Middleware é `async` e roda para TODAS as requisições, inclusive
    #    as que nem casam com uma rota. Nada de I/O bloqueante aqui —
    #    você atrasaria o sistema inteiro.

    # TODO: middleware de cabeçalhos de segurança
    #    X-Content-Type-Options: nosniff
    #    X-Frame-Options: DENY
    #    Referrer-Policy: no-referrer
    #    Strict-Transport-Security  ← só em produção, e só sob HTTPS

    # ═══════════════════════════════════════════════════════════════════
    #  Handlers de exceção
    # ═══════════════════════════════════════════════════════════════════
    #
    # TODO: um handler para a exceção BASE do Atlas, consultando MAPA_STATUS.
    #       Um handler por exceção também funciona, mas o mapa evita
    #       esquecer de registrar a próxima exceção que você criar.
    #
    # TODO: handler para RequestValidationError, padronizando o 422 no
    #       MESMO formato dos outros erros. O formato nativo do FastAPI
    #       é ótimo, mas diferente do seu — e quem consome a API não
    #       quer tratar dois formatos.
    #
    # TODO: 🔴 handler global para Exception:
    #
    #         detalhe completo  → LOG (com o id de correlação)
    #         mensagem genérica → RESPOSTA
    #
    #       Traceback numa resposta de API é vazamento de informação:
    #       revela caminhos de arquivo, versões de biblioteca, estrutura
    #       do projeto e, às vezes, trechos de código com credenciais.
    #
    #       O id de correlação é o que liga os dois: o cliente reporta
    #       "deu erro, id req-a1b2c3" e você acha a linha exata no log.

    # ═══════════════════════════════════════════════════════════════════
    #  Rotas
    # ═══════════════════════════════════════════════════════════════════
    # TODO: app.include_router(autenticacao.roteador)
    # TODO: app.include_router(produtos.roteador)
    # TODO: app.include_router(pedidos.roteador)
    # TODO: app.include_router(relatorios.roteador)

    # TODO: GET /saude — pública, com response_model=Saude
    #
    # ⚠️ Não exponha versão de biblioteca, hostname nem caminho aqui.
    #    Esta rota é pública e é a primeira que um varredor automático lê.

    return app


# ⚠️ Uma instância de módulo é conveniente para `uvicorn
#    atlas.api.aplicacao:app`, mas ela cria a app na IMPORTAÇÃO — o que
#    significa ler a configuração no import. Se você mantiver as duas
#    formas, saiba que os testes devem usar a fábrica.
#
# TODO: descomente se quiser a forma curta do uvicorn.
# app = criar_app()
