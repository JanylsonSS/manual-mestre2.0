"""Routers da API do Atlas.

Cada módulo aqui expõe um objeto `roteador` (`APIRouter`) que
`aplicacao.py` inclui.

💭 Por que quebrar em vários arquivos?

   Porque um `main.py` de 900 linhas não é problema de estética, é de
   acoplamento: mudar o cálculo de margem quebra a rota de pedidos
   porque tudo compartilha o mesmo escopo.

   Com routers, cada arquivo tem um assunto, um `prefix` e uma `tag` —
   e a tag vira o agrupamento do /docs de graça.

🎯 Regra de tamanho: nenhuma função de rota deve passar de ~5 linhas.
   Ela recebe (o FastAPI valida), chama o serviço, devolve (o FastAPI
   filtra). Se estiver maior, tem regra de negócio no lugar errado.
"""

__all__ = ["autenticacao", "pedidos", "produtos", "relatorios"]
