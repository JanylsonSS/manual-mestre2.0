"""Integrações com serviços de terceiros — Módulo 07.

No M06 você era o **servidor**: definia o contrato e escolhia quando
falhar. Aqui você é o **cliente**, e não controla nada — nem a
disponibilidade, nem a latência, nem o formato que o parceiro vai mudar
sem avisar.

Todo código desta pasta parte dessa premissa.

    atlas/integracoes/
    ├── cliente_http.py     base resiliente (timeout, retry, disjuntor)
    ├── transportadora.py   Veloz: cotação e rastreio
    ├── gateway.py          pagamento: cobrança
    └── cache.py            cache-aside sobre Redis

🧭 AS REGRAS DESTA CAMADA

  1. Nenhum módulo daqui levanta `HTTPException`. Eles levantam exceções
     de `atlas.excecoes`; quem traduz para HTTP é `atlas.api`.

  2. Nenhum `httpx.Client` sem `timeout`. Sem exceção.

  3. Credenciais vêm de `atlas.api.config` (que lê o ambiente). Nunca
     literais — e credencial de terceiro é ainda mais sensível que a
     sua, porque dá acesso a um sistema que não é seu.

  4. Falha de parceiro não pode virar `500`. Degrade: valor estimado,
     resposta em cache, ou `503` com `Retry-After`.

💭 A pergunta que orienta o desenho: *"o que a Aurora faz quando este
   serviço estiver fora por 10 minutos?"* Se a resposta for "para de
   vender", o desenho está errado.
"""

__all__: list[str] = []
