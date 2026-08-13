"""Hash de senha e emissão/verificação de token.

🔴 TRÊS REGRAS QUE NÃO SE NEGOCIAM

   1. A senha em texto puro nunca é gravada, nunca é logada, nunca
      aparece numa resposta. Ela existe na memória por milissegundos.

   2. Hash de senha é bcrypt, scrypt ou Argon2 — nunca sha256/md5.
      SHA-256 foi feito para ser rápido; senha precisa do contrário.

   3. JWT é ASSINADO, não criptografado. Qualquer um lê a carga.
      Nunca coloque CPF, endereço, saldo ou chave de API lá dentro.

Este módulo não conhece HTTP. Ele levanta `TokenInvalido`; quem traduz
para 401 é `dependencias.py`.
"""

from datetime import datetime, timedelta, timezone

# TODO: escolher e instalar a biblioteca de hash.
#       Opção A: bcrypt          (pip install bcrypt)
#       Opção B: hashlib.scrypt  (biblioteca padrão, zero dependência)
#       Opção C: argon2-cffi     (o mais moderno)
#
#       Se escolher a B, você precisa gerar e guardar o sal você mesmo —
#       o bcrypt já o embute no hash. Documente sua escolha aqui.


class TokenInvalido(Exception):
    """Token ausente, malformado, expirado ou com assinatura inválida.

    ⚠️ Uma exceção só para todos esses casos é PROPOSITAL: a resposta ao
       cliente deve ser a mesma. Detalhar qual foi o problema ajuda quem
       está tentando adivinhar um token válido.
    """


# ---------------------------------------------------------------------------
# Senha
# ---------------------------------------------------------------------------
def gerar_hash(senha: str) -> str:
    """Devolve o hash da senha, pronto para gravar no banco.

    Requisitos:
      - sal aleatório por chamada (a mesma senha → hashes diferentes)
      - custo ajustável (bcrypt: rounds=12 é um bom ponto de partida)

    ⚠️ O bcrypt ignora silenciosamente o que passa de 72 bytes. Se você
       permite senhas longas, valide o tamanho antes ou use Argon2.
    """
    # TODO: implementar.
    raise NotImplementedError


def conferir_senha(senha: str, hash_guardado: str) -> bool:
    """Compara a senha informada com o hash gravado.

    🔴 Use a função de comparação da própria biblioteca (`checkpw`,
       `hmac.compare_digest`). Um `==` comum vaza informação pelo tempo
       de execução — quanto mais bytes iniciais coincidem, mais demora.

    ⚠️ Deve devolver False para um hash corrompido, nunca estourar.
    """
    # TODO: implementar.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------
def criar_token(assunto: str, papel: str, minutos: int | None = None) -> str:
    """Emite um JWT assinado.

    Claims esperados:
      sub    quem é (o e-mail do usuário)
      papel  leitor | operador | admin
      exp    quando expira      ← obrigatório
      iat    quando foi emitido
      iss    quem emitiu        ("atlas-api")

    💭 Por que `exp` é obrigatório? Porque um token sem expiração é uma
       senha permanente que o usuário não sabe que tem. Se vazar, só
       trocar a chave secreta resolve — invalidando todos os outros.
    """
    # TODO: implementar usando obter_config() para chave e algoritmo.
    raise NotImplementedError


def ler_token(token: str) -> dict:
    """Valida a assinatura E a expiração, devolvendo a carga.

    🔴 Passe `algorithms=[...]` explicitamente no decode. Aceitar o
       algoritmo que vem no cabeçalho do token é a vulnerabilidade
       clássica do JWT: o atacante manda `alg: none` e a verificação
       é pulada.

    ⚠️ Valide também o `iss`, se você o emite. Um token legítimo de
       OUTRO sistema que use a mesma chave não deve valer aqui.
    """
    # TODO: implementar. Converta as exceções da biblioteca em TokenInvalido.
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def agora_utc() -> datetime:
    """Sempre UTC. Sempre com fuso.

    💡 Você aprendeu isso no M04: `datetime.utcnow()` devolve um datetime
       *ingênuo* (sem fuso) que parece UTC e se comporta como local em
       comparações. É uma das piores armadilhas do Python.
    """
    return datetime.now(timezone.utc)


def expira_em(minutos: int) -> datetime:
    """Instante de expiração, a partir de agora."""
    return agora_utc() + timedelta(minutes=minutos)


if __name__ == "__main__":
    # Roteiro de conferência manual:
    #   1. gerar_hash("teste") duas vezes → hashes DIFERENTES
    #   2. conferir_senha("teste", h1) e conferir_senha("teste", h2) → True
    #   3. conferir_senha("errada", h1) → False
    #   4. criar_token(...) → dividir por "." e decodificar a carga em
    #      base64 SEM CHAVE, para você ver com os próprios olhos que
    #      JWT não esconde nada.
    # TODO: escrever essa conferência.
    pass
