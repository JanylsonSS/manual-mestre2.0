# Containers do Atlas

> **Status:** 🚧 esqueleto. Preencha conforme implementar.
>
> Este documento registra **decisões**, não descrições. O Dockerfile já
> diz o que faz; aqui você explica *por quê* — para o você de daqui a
> seis meses, e para quem entrar na equipe.

---

## Como subir

```bash
cp .env.example .env      # e preencher
docker compose up -d
docker compose ps         # todos devem estar `healthy`
```

Depois: <http://127.0.0.1:8000/docs>

### Comandos do dia a dia

```bash
docker compose logs -f api                    # acompanhar
docker compose exec api sh                    # entrar
docker compose exec postgres psql -U atlas    # o banco
docker compose up -d --build api              # reconstruir
docker compose --profile ferramentas run --rm migracao
docker compose down                           # derrubar (MANTÉM os dados)
docker compose down -v                        # 🔴 APAGA OS VOLUMES
```

---

## Decisões registradas

<!-- 🔴 Esta seção é a razão de o arquivo existir. Preencha-a. -->

### Imagem base

<!-- TODO: qual você escolheu e por quê?

     python:3.12 (1 GB) · slim (130 MB) · alpine (51 MB) · distroless

     ⚠️ Se escolheu Alpine, meça: com Python ele costuma sair MAIS
        LENTO e às vezes MAIOR, porque `musl` invalida as wheels do
        PyPI e o pip compila tudo do zero.

     Registre o tamanho final medido com `docker images`.          -->

### Multi-stage: quantos estágios, e o que cada um faz

<!-- TODO -->

### Tamanho da imagem

<!-- TODO: preencha com números reais.

     | Versão | Tamanho | O que mudou |
     |--------|---------|-------------|
     | primeira tentativa | | |
     | com multi-stage | | |
     | com .dockerignore | | |                                      -->

### Usuário e permissões

<!-- TODO: qual UID, e por quê esse número?

     💭 UID 1000 é o primeiro usuário comum no Linux. Casar o UID de
        dentro com o de fora evita problema de permissão em bind
        mount. Se você escolheu outro, registre o motivo.           -->

### Onde ficam os segredos

<!-- TODO: 🔴 responda com precisão.

     · em desenvolvimento: .env + env_file?
     · em produção: qual mecanismo? (M09)
     · algum segredo é necessário em tempo de BUILD?
       Se sim, você usou `--mount=type=secret`?                     -->

### Volumes: o que persiste e o que pode sumir

<!-- TODO: para CADA serviço, responda:
     "se este container for destruído, o que se perde?"

     | Serviço | Volume | O que se perde sem ele |
     |---------|--------|------------------------|
     | postgres | | |
     | mongo | | |
     | redis | | 💭 cache reconstrói; idempotência do M07 não |
     | api | (nenhum) | nada — e é assim que deve ser |            -->

### Healthchecks: por que estes valores

<!-- TODO: justifique o `start_period` de cada serviço.

     Regra prática: ≥ 2× o tempo normal de partida. MEÇA o seu:
     `docker compose up` e cronometre até o primeiro `healthy`.     -->

### Limites de recurso

<!-- TODO: quanto de CPU e memória para cada serviço, e com base em quê?

     ⚠️ Não chute. Suba, rode uma carga representativa, olhe o
        `docker stats`, e ponha o limite acima do pico observado com
        uma folga. Limite apertado demais vira `OOMKilled` em
        produção, no pior momento.                                  -->

---

## O que NÃO está containerizado, e por quê

<!-- TODO: 🔴 esta seção vale mais que a lista do que está.

     Toda arquitetura tem partes de fora. Documentá-las é a diferença
     entre uma decisão e um esquecimento.

     Exemplos do tipo de coisa a registrar:
       · o proxy reverso (é do M09)
       · backup dos volumes — existe? é testado?
       · os notebooks do manual
       · os dados brutos em `dados/brutos/`                         -->

---

## Solução de problemas

| Sintoma | Causa provável | Onde olhar |
|---------|----------------|------------|
| `connection refused` do host | Escutou em `127.0.0.1` | `CMD` do Dockerfile |
| `connection refused` para o banco | Usou `localhost` | `environment` do compose |
| Container morre sem log | Falta `PYTHONUNBUFFERED=1` | `ENV` do Dockerfile |
| `docker stop` demora 10 s | `CMD` em shell, ou falta `exec` | `CMD`/`entrada.sh` |
| Sempre `unhealthy` | `curl` não existe na imagem | `HEALTHCHECK` |
| Reinicia em laço | Sem `start_period` | `healthcheck` do compose |
| `Exited (137)` | 🔴 OOM — o cgroup matou | `docker inspect ... OOMKilled` |
| `Exited (143)` | `SIGTERM` — encerramento normal | (não é erro) |
| Build refaz tudo | `COPY .` antes das dependências | ordem do Dockerfile |
| Dados sumiram | Sem volume, ou `down -v` | `volumes:` do compose |

### O primeiro comando quando algo não sobe

```bash
docker compose config
```

Ele mostra o YAML final, com as variáveis já substituídas. **Metade dos
problemas é uma variável vazia que você não percebeu** — o Compose
substitui por string vazia em silêncio.

Use `${VAR:?mensagem}` nos segredos para que ele falhe em vez de
silenciar.

---

## Auditoria

```bash
python scripts/auditar_containers.py
echo $?     # 0 = aprovado
```

<!-- TODO: quando o script estiver pronto, cole aqui a saída de uma
     execução aprovada. Ela serve de referência para quem for mexer
     depois.                                                        -->

> 🔴 **E teste o verificador.** Quebre o Dockerfile de propósito
> (`:latest`, sem `USER`, segredo em `ENV`) e confirme que ele reprova.
> Um verificador que nunca reprova ninguém não está verificando nada.
