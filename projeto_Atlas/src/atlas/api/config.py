"""Configuração da API, vinda do ambiente.

💭 Por que não usar `atlas/config.py`?

   Aquele arquivo guarda constantes de DOMÍNIO (cortes da curva ABC,
   formato de data, largura do relatório) — valores que fazem parte da
   regra de negócio e são iguais em qualquer máquina.

   Este guarda configuração de INFRAESTRUTURA: URL do banco, chave
   secreta, origens de CORS. São valores que mudam entre a sua máquina,
   a homologação e a produção — e alguns deles são segredos.

   Misturar os dois é o que leva senha de banco para dentro do Git.

🔴 REGRA: nenhum valor real mora neste arquivo. Só o nome da variável,
   a validação e, no máximo, um default seguro para desenvolvimento.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigAPI(BaseSettings):
    """Configuração lida do ambiente e do arquivo `.env`.

    Precedência (o primeiro que existir vence):
      1. variável de ambiente do processo
      2. arquivo .env
      3. default declarado aqui
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ATLAS_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── Identificação ───────────────────────────────────────────────
    # TODO: definir titulo, versao e ambiente.
    #       `ambiente` deve aceitar apenas: desenvolvimento | homologacao | producao
    titulo: str = "Atlas API"
    versao: str = "1.0.0"
    ambiente: str = "desenvolvimento"

    # ── Banco ───────────────────────────────────────────────────────
    # TODO: reaproveitar a URL que você montou no M05.
    #       Dica: aceite tanto ATLAS_DB_URL completa quanto as partes
    #       (host/porta/usuário/senha), com a URL completa vencendo.
    db_url: str = "sqlite:///./dados/atlas.db"

    # ── Segurança 🔴 ────────────────────────────────────────────────
    # TODO: `secret_key` NÃO pode ter default utilizável.
    #       Use Field(min_length=32) para que a aplicação se RECUSE a
    #       subir sem uma chave de verdade. Falhar ao subir é melhor do
    #       que assinar tokens que qualquer um forja.
    #
    #       Gere a sua com:
    #           python -c "import secrets; print(secrets.token_urlsafe(48))"
    secret_key: str = Field(default="", min_length=0)  # TODO: min_length=32, sem default

    algoritmo: str = "HS256"

    # TODO: minutos de validade do token. Faixa razoável: 5 a 1440.
    token_expira_minutos: int = 60  # TODO: Field(ge=5, le=1440)

    # ── CORS ────────────────────────────────────────────────────────
    # TODO: listar as origens do front. Em produção, NUNCA ["*"].
    origens_permitidas: list[str] = []

    # ── Paginação ───────────────────────────────────────────────────
    pagina_tamanho_padrao: int = 20
    pagina_tamanho_maximo: int = 100

    # ------------------------------------------------------------------
    # Validadores
    # ------------------------------------------------------------------
    @field_validator("secret_key")
    @classmethod
    def chave_nao_pode_ser_exemplo(cls, valor: str) -> str:
        """Recusa as chaves de exemplo que circulam em tutoriais.

        🔴 Já houve incidente real por causa disso: alguém copia a chave
           do README, publica, e todo mundo que leu o README consegue
           forjar tokens de admin.
        """
        # TODO: recusar valores como "segredo", "changeme", "secret",
        #       "gere-uma-chave-aleatoria-longa" e a chave do .env.example.
        return valor

    @field_validator("ambiente")
    @classmethod
    def ambiente_conhecido(cls, valor: str) -> str:
        # TODO: aceitar apenas os três ambientes previstos.
        return valor

    # ------------------------------------------------------------------
    # Derivados
    # ------------------------------------------------------------------
    @property
    def producao(self) -> bool:
        # TODO: True quando ambiente == "producao"
        return False

    @property
    def docs_habilitados(self) -> bool:
        """Em produção você pode querer esconder /docs.

        💭 Isto é *segurança por obscuridade* — vale pouco sozinho, mas
           reduz a superfície para varredura automatizada. Não substitui
           autenticação.
        """
        # TODO: decidir e justificar num comentário.
        return True


@lru_cache
def obter_config() -> ConfigAPI:
    """Instância única por processo.

    🔑 O `lru_cache` faz a leitura do ambiente acontecer UMA vez. Também
       é o ponto de substituição nos testes:

           obter_config.cache_clear()
           # ou, melhor:
           app.dependency_overrides[obter_config] = lambda: ConfigAPI(...)
    """
    return ConfigAPI()


if __name__ == "__main__":
    # `python -m atlas.api.config` mostra a configuração efetiva.
    # 🔴 CUIDADO: nunca imprima a chave secreta inteira. Mostre o tamanho
    #    e os primeiros caracteres, no máximo.
    # TODO: imprimir ambiente, db_url (sem a senha!), tamanho da chave.
    pass
