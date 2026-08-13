"""API HTTP do Atlas — Módulo 06.

Esta camada é a **porta de entrada** do sistema. Ela não contém regra de
negócio: traduz HTTP para chamadas de `atlas.servicos` e de volta.

    HTTP  →  rotas/  →  servicos.py  →  repositorio.py  →  banco
                ↑                                            │
                └────────── esquemas.py (Pydantic) ──────────┘

⚠️ Regra de ouro do módulo: **`atlas.servicos` não pode importar `fastapi`.**
   Se você precisar de `HTTPException` dentro de um serviço, o desenho
   está errado — levante uma exceção de `atlas.excecoes` e traduza-a
   num handler de `aplicacao.py`.

Para subir a API:

    uvicorn atlas.api.aplicacao:app --reload

Ou, com a fábrica:

    uvicorn "atlas.api.aplicacao:criar_app" --factory --reload
"""

# TODO: reexportar `criar_app` aqui quando ela existir, para permitir
#       `from atlas.api import criar_app`.
# from atlas.api.aplicacao import criar_app

__all__: list[str] = []
