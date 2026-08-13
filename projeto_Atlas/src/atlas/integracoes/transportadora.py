"""Transportadora Veloz — cotação de frete e rastreamento.

💭 O caso de negócio: hoje a Aurora cota frete por telefone e rastreia
   entrega abrindo o site da transportadora. Isso vira duas chamadas.

🔴 E o requisito que define este módulo: **o checkout não pode cair
   junto com a transportadora.** Quando a Veloz ficou 8 minutos fora, a
   Aurora ficou 8 minutos sem vender. Isso não pode se repetir.
"""

from __future__ import annotations

from atlas.integracoes.cliente_http import ClienteHTTP


class TransportadoraIndisponivel(Exception):
    """Erro de DOMÍNIO.

    🔑 Repare que não é `HTTPException`. Este módulo não sabe o que é
       HTTP do lado servidor — quem traduz para 503 (ou para uma
       resposta degradada) é `atlas.api`.

       É o mesmo princípio do M06: o domínio não conhece a apresentação.
    """


class CotacaoRecusada(ValueError):
    """A Veloz recusou os dados (CEP inválido, peso acima do limite).

    ⚠️ Erro NOSSO, não deles. Não se repete: 422 vai ser 422 de novo.
    """


class ClienteVeloz(ClienteHTTP):
    """Cliente da Transportadora Veloz."""

    NOME = "transportadora-veloz"

    def __init__(self, url_base: str, cliente_id: str, segredo: str, **kwargs):
        super().__init__(url_base, **kwargs)
        # 🔴 `cliente_id` e `segredo` vêm de ConfigAPI (que lê o ambiente).
        #    Nunca literais aqui. Credencial de terceiro é ainda mais
        #    sensível que a sua: ela dá acesso a um sistema que não é seu,
        #    e o vazamento é um problema contratual, não só técnico.
        self._id = cliente_id
        self._segredo = segredo
        # TODO: guardar token e instante de expiração
        self.renovacoes = 0

    # ------------------------------------------------------------------
    def _autenticar(self) -> None:
        """Troca id+segredo por um token de vida curta (client credentials).

        A Veloz usa HTTP Basic no `POST /v1/auth/token` e devolve
        `{"access_token": ..., "expires_in": <segundos>}`.

        TODO: implementar, guardando o token e `agora + expires_in - margem`.
        """
        raise NotImplementedError

    def cabecalhos_de_autenticacao(self) -> dict[str, str]:
        """Renova sozinho quando necessário.

        🎯 O objetivo: nenhuma linha de quem chama `cotar()` deve saber
           que existe token, expiração ou renovação. Quando a Veloz
           trocar Basic por mTLS, você muda UM arquivo.
        """
        # TODO: se não há token ou ele está perto de expirar, _autenticar()
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Operações
    # ------------------------------------------------------------------
    def cotar(self, peso_kg: float, cep_destino: str) -> dict:
        """Devolve `{"valor", "prazo_dias", "servico"}`.

        Erros esperados:
          · 422            → CotacaoRecusada (não repetir)
          · rede / 5xx     → TransportadoraIndisponivel (após as tentativas)

        TODO: implementar sobre `self.pedir("POST", "/v1/cotacoes", json=...)`.
        """
        raise NotImplementedError

    def cotar_com_estimativa(self, peso_kg: float, cep_destino: str) -> dict:
        """🔴 A degradação que salva o checkout.

        Quando a Veloz está fora, NÃO devolva erro. Devolva uma
        estimativa própria e marque a resposta:

            {"valor": ..., "prazo_dias": ..., "estimado": True,
             "aviso": "valor sujeito a confirmação"}

        💭 Por quê? Porque o cliente prefere comprar com um frete
           aproximado a não conseguir comprar. E a Aurora prefere vender
           com 3% de erro no frete a não vender.

        ⚠️ Mas seja honesto na interface: `estimado: True` precisa
           aparecer para o usuário e ficar registrado no pedido, para o
           financeiro reconciliar depois.

        TODO: implementar usando `cotar()` e capturando
              TransportadoraIndisponivel. A fórmula da estimativa mora
              em `atlas/regras.py` — não invente números aqui.
        """
        raise NotImplementedError

    def entregas(self, desde: str | None = None):
        """Gerador de todas as entregas (paginado).

        🔴 Use CURSOR, não offset. Esta é uma sincronização de dados: se
           a Veloz inserir uma entrega enquanto você lê, o offset faz
           você ler um registro duas vezes — silenciosamente.

        TODO: implementar com `paginar()`.
        """
        raise NotImplementedError

    def rastrear(self, codigo: str) -> dict:
        """Situação de uma entrega.

        💡 Candidato natural a cache: a mesma tela consulta o mesmo
           código repetidamente, e o dado muda no máximo algumas vezes
           por dia. TTL de uns minutos economiza quase todas as chamadas.
        """
        raise NotImplementedError


def sincronizar_entregas(cliente: ClienteVeloz, repositorio) -> dict:
    """Importa as entregas para o banco do Atlas.

    🔴 REQUISITO: RETOMÁVEL E IDEMPOTENTE.

       Esta função roda de madrugada, sem ninguém olhando. Ela precisa
       de duas propriedades:

       1. **Idempotente** — rodar duas vezes dá o mesmo resultado que
          rodar uma. Use UPSERT (`ON CONFLICT`), como no M03.

       2. **Retomável** — se morrer na página 40 de 100, a próxima
          execução continua de onde parou. Guarde o cursor a cada lote
          confirmado, não só no fim.

    ⚠️ Guarde o cursor DEPOIS de confirmar o lote no banco. Se guardar
       antes, um erro entre as duas operações faz você pular registros —
       e ninguém percebe, porque não houve erro.

    Devolve `{"lidas": n, "novas": n, "atualizadas": n, "erros": n}`.

    TODO: implementar.
    """
    raise NotImplementedError
