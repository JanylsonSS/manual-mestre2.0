#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
#  Ponto de entrada do container da API — Módulo 08
#
#  Usado no Dockerfile como:
#      ENTRYPOINT ["/app/scripts/entrada.sh"]
#      CMD ["uvicorn", "atlas.api.aplicacao:criar_app", "--factory", \
#           "--host", "0.0.0.0", "--port", "8000"]
#
#  💭 QUANDO VOCÊ PRECISA DE UM ENTRYPOINT EM SCRIPT?
#
#     Quase nunca. Se o compose já usa `depends_on: service_healthy`
#     e as migrações rodam num serviço separado com
#     `service_completed_successfully`, o container da API pode
#     simplesmente executar o uvicorn — e é mais simples assim.
#
#     Este script é para os casos em que você NÃO controla o
#     orquestrador: um PaaS que só te dá um comando, um Kubernetes
#     sem init container, uma máquina onde tudo sobe junto.
#
#  🔴 E ele tem uma armadilha própria, tratada na última linha.
# ═══════════════════════════════════════════════════════════════
set -euo pipefail
#   -e  aborta no primeiro erro
#   -u  variável não definida é erro (pega typo em nome de env)
#   -o pipefail  erro no meio de um pipe não é engolido

# ───────────────────────────────────────────────────────────────
# 1. Esperar as dependências
# ───────────────────────────────────────────────────────────────
# TODO: implementar uma espera com TETO.
#
#   ⚠️ NUNCA `sleep 10`. É um chute: curto demais numa máquina lenta,
#      desperdício numa rápida, e sempre errado quando o banco
#      precisa aplicar migrações ou recuperar o WAL.
#
#   🔴 E NUNCA um laço infinito. Se o banco nunca subir, o container
#      fica "iniciando" para sempre e o seu monitoramento não acusa
#      nada — o pior tipo de falha, a silenciosa. Ponha um teto e
#      SAIA COM ERRO.
#
#   esperar_porta() {
#       local host="$1" porta="$2" limite="${3:-60}"
#       ...
#   }
#
#   💡 Sem `nc` na imagem slim? Use o Python que já está lá:
#      python -c "import socket,sys; socket.create_connection(('$host',$porta),2)"

# ───────────────────────────────────────────────────────────────
# 2. Migrações
# ───────────────────────────────────────────────────────────────
# TODO (opcional, e pense antes):
#
#   if [ "${ATLAS_RODAR_MIGRACOES:-nao}" = "sim" ]; then
#       alembic upgrade head
#   fi
#
#   🔴 CUIDADO: se você subir 3 réplicas da API, as 3 tentam migrar ao
#      mesmo tempo. O Alembic tem trava, mas o desenho correto é rodar
#      a migração num passo SEPARADO, antes do deploy — nunca no
#      start-up de um serviço que escala.
#
#   💭 Por isso o padrão-ouro é o serviço `migracao` com
#      `profiles: ["ferramentas"]` no compose, e a API dependendo dele
#      com `service_completed_successfully`.

# ───────────────────────────────────────────────────────────────
# 3. Conferir a configuração antes de subir
# ───────────────────────────────────────────────────────────────
# TODO: falhe CEDO e com mensagem clara.
#
#   : "${ATLAS_SECRET_KEY:?ATLAS_SECRET_KEY não definida}"
#
#   💭 Falhar ao subir é melhor do que subir errado: a mensagem
#      aparece na hora, no log do deploy, com o nome da variável.
#      Sem isso, você descobre no primeiro login que falha — e a
#      mensagem aponta para o lugar errado. Mesma lição do M06.

# ───────────────────────────────────────────────────────────────
# 4. Entregar o controle
# ───────────────────────────────────────────────────────────────
# 🔴 `exec` NÃO É OPCIONAL.
#
#    Sem ele, o `bash` continua sendo o PID 1 e o uvicorn vira filho.
#    O `docker stop` manda SIGTERM para o PID 1 — o bash — que não
#    repassa. O uvicorn nunca sabe que deve encerrar, o Docker espera
#    10 segundos e mata com SIGKILL.
#
#    Sintomas: todo `docker stop` demorando 10 segundos, conexões
#    cortadas no meio, transações abandonadas.
#
#    Com `exec`, o processo SUBSTITUI o shell: o uvicorn vira o PID 1
#    e recebe o sinal diretamente.
#
# TODO: exec "$@"
