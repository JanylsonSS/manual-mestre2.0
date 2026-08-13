"""Login e identidade.

🔴 Esta é a rota mais atacada de qualquer API. Trate-a assim.
"""

from fastapi import APIRouter

# TODO: importar Depends, HTTPException, status
# TODO: importar OAuth2PasswordRequestForm de fastapi.security
# TODO: importar os esquemas Token e UsuarioResposta

roteador = APIRouter(prefix="/auth", tags=["Autenticação"])


# ═══════════════════════════════════════════════════════════════════════
#  POST /auth/token
# ═══════════════════════════════════════════════════════════════════════
#
# Assinatura esperada:
#
#     @roteador.post("/token", response_model=Token)
#     def entrar(formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
#                sessao: SessaoDep):
#
# ⚠️ `Depends()` VAZIO significa "use a própria classe anotada como
#    dependência". O FastAPI instancia OAuth2PasswordRequestForm a
#    partir do form-data.
#
# 🔴 Por que form-data e não JSON? Porque a especificação OAuth2 manda.
#    É chato, mas é o que faz o botão "Authorize" do /docs funcionar e
#    o que todo cliente OAuth espera. Exige o pacote `python-multipart`.
#
# 🔴 Os campos se chamam `username` e `password` — não traduza. Aqui o
#    `username` é o e-mail do funcionário.
#
# ═══ AS TRÊS REGRAS DESTA ROTA ═══
#
# 1. MENSAGEM IDÊNTICA para "e-mail não existe" e "senha errada".
#    Diferenciar entrega ao atacante a lista de quem tem conta na
#    empresa — que é meio caminho para um ataque direcionado.
#
#    Monte UM objeto de exceção e levante o mesmo nos dois casos.
#
# 2. TEMPO PARECIDO nos dois casos.
#    Se o e-mail não existe você pula o bcrypt e responde em 1 ms; se
#    existe, gasta 300 ms conferindo. Essa diferença é mensurável e
#    revela exatamente o que a regra 1 tentou esconder.
#
#    A defesa: rode um hash descartável contra um hash fixo quando o
#    usuário não existir.
#
# 3. NUNCA logue o corpo desta requisição.
#    Um `logging.info("payload: %s", corpo)` numa rota de login manda a
#    senha de todo mundo para o arquivo de log — que costuma ter menos
#    proteção que o banco.
#
# TODO: implementar `entrar`.


# ═══════════════════════════════════════════════════════════════════════
#  GET /auth/eu
# ═══════════════════════════════════════════════════════════════════════
#
#     @roteador.get("/eu", response_model=UsuarioResposta)
#     def quem_sou_eu(usuario: UsuarioDep):
#         return usuario
#
# 💡 Rota de duas linhas, e das mais úteis: é como o front descobre o
#    papel do usuário para decidir quais botões desenhar.
#
# 🔒 O `response_model` é o que impede o `senha_hash` de sair junto,
#    já que `usuario` é o registro inteiro do banco.
#
# TODO: implementar `quem_sou_eu`.


# ═══════════════════════════════════════════════════════════════════════
#  Ideias para depois (não são requisito do M06)
# ═══════════════════════════════════════════════════════════════════════
#
#  POST /auth/refresh   troca um token de longa duração por um curto,
#                       para não obrigar o usuário a relogar de hora em hora
#
#  POST /auth/sair      revogação: exige guardar o claim `jti` numa
#                       lista de tokens invalidados (Redis, no M07)
#
#  POST /auth/senha     troca de senha — exige a senha ATUAL, sempre
#
# 💭 Repare que revogação exige estado no servidor. Essa é a troca do
#    JWT: ele é sem estado (rápido, escalável) até você precisar
#    cancelá-lo — e aí não é mais.
