# ═══════════════════════════════════════════════════════════════
#  Atlas API — imagem de produção
#  Módulo 08
#
#  Construir:  docker build -t atlas-api:1.2.0 .
#  Rodar:      docker run -p 8000:8000 --env-file .env atlas-api:1.2.0
#
#  🔴 Antes de escrever qualquer linha, releia a regra que ordena
#     tudo o que vem abaixo:
#
#         DO QUE MUDA MENOS PARA O QUE MUDA MAIS
#
#     A imagem base muda a cada meses. As dependências, a cada
#     semanas. O seu código, a cada minutos. Se o código vier antes
#     das dependências, todo `docker build` refaz o `pip install`
#     inteiro — 45 segundos que você paga dezenas de vezes por dia.
# ═══════════════════════════════════════════════════════════════


# ─────────────────────── ESTÁGIO 1: construir ───────────────────
# 💭 Por que dois estágios?
#
#    Para INSTALAR o psycopg você precisa de `gcc` e `libpq-dev`.
#    Para RODAR o Atlas, não. Um estágio separado deixa o compilador
#    para trás: a imagem final fica ~5× menor e sem uma ferramenta de
#    compilação à disposição de quem conseguir entrar nela.

# TODO: escolha e FIXE a imagem base.
#   🔴 Nunca `:latest` — ele não significa "a mais nova", é só a tag
#      padrão. Uma imagem de dois anos atrás pode estar marcada assim.
#   💡 `python:3.12-slim` é o ponto de partida sensato.
#      Alpine parece tentador (51 MB), mas usa `musl` no lugar da
#      `glibc` — as wheels do PyPI não servem, o pip compila tudo do
#      zero, e o build fica 5 a 10× mais lento.
FROM python:3.12-slim AS construtor

# TODO: instale as dependências de sistema necessárias para compilar.
#   ⚠️ TRÊS regras numa linha só:
#      1. `update` e `install` no MESMO RUN — em RUNs separados o
#         Docker reaproveita a lista de pacotes velha e o install
#         falha com "package not found" que some ao limpar o cache
#      2. `--no-install-recommends` — corta dezenas de MB
#      3. `rm -rf /var/lib/apt/lists/*` na MESMA camada — limpar num
#         RUN seguinte não diminui nada (a camada anterior guarda)
#
#   RUN apt-get update && apt-get install -y --no-install-recommends \
#           gcc libpq-dev \
#       && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 🔑 A LINHA MAIS IMPORTANTE DO ARQUIVO
#
#    Copie SÓ o arquivo de dependências, e ANTES do código. É isso
#    que põe o `pip install` numa camada que o seu código não
#    invalida.
#
# TODO: COPY do pyproject.toml (e do lock, se você usar um)
# TODO: RUN pip install --no-cache-dir --prefix=/instalado .
#   💡 `--no-cache-dir`: o cache do pip não tem o que fazer na imagem
#   💡 `--prefix=/instalado`: junta tudo num lugar só, fácil de copiar
#      para o próximo estágio


# ─────────────────────── ESTÁGIO 2: rodar ───────────────────────
# TODO: MESMA imagem base do estágio 1 (sem o `AS`)
FROM python:3.12-slim

# TODO: só a biblioteca de RUNTIME do Postgres — `libpq5`, não
#   `libpq-dev`. Headers e compilador ficaram no estágio anterior.

# 🔴 USUÁRIO SEM PRIVILÉGIO
#
#    Por padrão o processo roda como root. "Mas é root só dentro do
#    container" — depende:
#      · com daemon padrão, escapar do container é escapar como root
#      · com volume montado, ele escreve no host como root e você
#        fica com arquivos que não consegue apagar
#
# TODO: RUN useradd --create-home --uid 1000 atlas
#   💡 UID 1000 é o primeiro usuário comum no Linux. Casar o UID de
#      dentro com o de fora evita dor de cabeça em bind mount.

WORKDIR /app

# TODO: COPY --from=construtor /instalado /usr/local
# TODO: COPY --chown=atlas:atlas src/ ./src/
#   ⚠️ O `--chown` importa: sem ele os arquivos ficam de root e o
#      usuário `atlas` pode não conseguir lê-los.

# TODO: USER atlas
#   ⚠️ DEPOIS de tudo que instala. Um `apt-get` depois do USER falha.

# TODO: variáveis de ambiente
#   ENV PYTHONUNBUFFERED=1 \
#       PYTHONDONTWRITEBYTECODE=1 \
#       PYTHONPATH=/app/src
#
#   🔴 `PYTHONUNBUFFERED=1` NÃO é opcional. Sem ele o Python
#      bufferiza o stdout, e os seus logs só aparecem quando o buffer
#      enche — ou nunca, se o container morrer antes. É a causa nº 1
#      de "o container morreu e não tem nada no log".

# TODO: EXPOSE 8000
#   💭 `EXPOSE` não publica nada — é documentação. Quem publica é o
#      `-p` do run ou o `ports:` do compose.

# TODO: HEALTHCHECK
#   ⚠️ NÃO use `curl`: ele não existe na imagem slim, e o healthcheck
#      falha para sempre sem dizer por quê. Use o Python que já está lá.
#   🔑 `--start-period` é o parâmetro que quase ninguém configura e o
#      que mais causa confusão: sem carência, uma app que leva 20 s
#      para subir é marcada `unhealthy` e reiniciada — em laço.
#
#   HEALTHCHECK --interval=30s --timeout=3s --start-period=15s --retries=3 \
#       CMD ["python", "-c", "import httpx,sys; sys.exit(0 if httpx.get('http://127.0.0.1:8000/saude').status_code==200 else 1)"]

# 🔴 FORMA JSON, NUNCA FORMA SHELL
#
#    CMD uvicorn ...            → vira `/bin/sh -c "uvicorn ..."`
#                                  PID 1 = sh, e o sh NÃO repassa sinais
#    CMD ["uvicorn", ...]       → PID 1 = uvicorn
#
#    Na forma shell, o `docker stop` manda SIGTERM para o `sh`, o
#    uvicorn nunca fica sabendo, o Docker espera 10 segundos e mata
#    com SIGKILL. Conexões cortadas no meio, e todo `stop` demorando
#    10 segundos.
#
# TODO: ENTRYPOINT ["python", "-m", "uvicorn"]
# TODO: CMD ["atlas.api.aplicacao:criar_app", "--factory", \
#            "--host", "0.0.0.0", "--port", "8000"]
#
#   🔴 `0.0.0.0`, NUNCA `127.0.0.1`.
#      Dentro do container, `127.0.0.1` é o loopback DAQUELE namespace
#      de rede. Um servidor escutando lá é inalcançável de fora,
#      mesmo com `-p 8000:8000` — e o erro é um "connection refused"
#      sem nenhuma pista. É o erro nº 1 de quem containeriza a
#      primeira aplicação.


# ═══════════════════════════════════════════════════════════════
#  Quando terminar, audite:
#
#      python scripts/auditar_containers.py
#
#  Alvo: zero achados 🔴.
# ═══════════════════════════════════════════════════════════════
