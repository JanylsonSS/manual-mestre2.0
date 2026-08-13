# Roteiro — Módulo 08 · Containerizando o Atlas

> **Objetivo:** transformar "dois dias para configurar a máquina" em
> **dois comandos**, em qualquer sistema operacional.

---

## A situação

> *"Contratamos uma desenvolvedora nova. Ela levou dois dias para rodar
> o Atlas. Python errado, PostgreSQL de outra versão, o Mongo não subia
> no Windows, e uma variável de ambiente que ninguém lembrava de
> documentar."*

Hoje o Atlas precisa de: Python 3.10+, PostgreSQL 16, MongoDB 7, Redis,
`gcc`, `libpq-dev` e nove variáveis de ambiente. Cada pessoa monta isso
à mão, do seu jeito, no seu sistema.

**Ao final deste módulo:**

```bash
git clone ...
cp .env.example .env      # e preencher
docker compose up -d
```

---

## 🎯 A boa notícia antes de começar

Antes de escrever uma linha de Dockerfile, confira o que já está pronto:

| Requisito para containerizar | Veio de | Situação |
|------------------------------|---------|----------|
| Configuração por ambiente | M06 (`ConfigAPI`) | ✅ |
| Segredos fora do código | M06 (`.env`) | ✅ |
| Rota de saúde (`/saude`) | M06 | ✅ |
| API sem estado | M06 (sessão por requisição) | ✅ |
| Dependências declaradas | M04 (`pyproject.toml`) | ✅ |
| Log estruturado | M04 | 🔶 falta mandar para stdout |
| Escutar em `0.0.0.0` | — | 🔴 hoje é `127.0.0.1` |
| Tratar `SIGTERM` | — | 🔴 falta |

> 💭 **Seis dos oito já estavam prontos — e você não os fez pensando em
> Docker.** Fez porque eram boas práticas.
>
> 🎯 **Containerizar não é adaptar a aplicação ao Docker. É descobrir
> que uma aplicação bem construída já é containerizável.** O que sobra
> são dois ajustes de dez minutos. Esse é o retorno dos módulos
> anteriores.

---

## Ordem de trabalho

```
1. Preparar a aplicação      ← os dois ajustes que faltam
2. Dockerfile                ← multi-stage, não-root
3. .dockerignore             ← 🔴 antes do primeiro build
4. Compose                   ← os quatro serviços
5. Healthchecks              ← o fim do `sleep 10`
6. Override de dev           ← bind mount e reload
7. Auditoria                 ← o portão de CI
```

---

## Etapa 1 — Preparar a aplicação

### O que fazer

1. **Escutar em `0.0.0.0`.** A porta e o host vêm do ambiente, com
   padrão sensato.

2. **Log para stdout.** O `observabilidade.py` do M04 já escreve JSON —
   só falta mandá-lo para `sys.stdout` em vez de `saida/atlas.jsonl`.

3. **Tratar `SIGTERM`.** O `lifespan` do M06 já fecha o pool; garanta
   que ele é chamado no encerramento.

### Pronto quando

- [ ] `uvicorn --host 0.0.0.0` sobe e responde de outra máquina da rede
- [ ] `python main.py relatorio` imprime o log no terminal, não em arquivo
- [ ] `Ctrl+C` encerra com educação, sem traceback

> 🔴 **Por que log em arquivo não serve num container.** O arquivo vive
> na camada gravável, que morre com o container. Você perde exatamente
> o log de que precisa para entender por que ele morreu.

---

## Etapa 2 — Dockerfile

### O que fazer

Implemente o `Dockerfile` (o esqueleto está na raiz, com os TODOs).

### 🔑 A regra que ordena tudo

```
DO QUE MUDA MENOS PARA O QUE MUDA MAIS

FROM python:3.12-slim        ← muda a cada meses
RUN apt-get install ...      ← muda a cada meses
COPY pyproject.toml ./       ← muda a cada semanas
RUN pip install .            ← 🔑 45 segundos, protegidos
COPY src/ ./src/             ← muda a cada minutos
```

Trocar as duas últimas de lugar faz cada build refazer o `pip install`.
Medido na aula 08_02: **46 s contra 0,5 s** para uma linha de Python
alterada.

### Pronto quando

- [ ] `docker build` termina sem erro
- [ ] `docker images` mostra **menos de 250 MB**
- [ ] `docker history` não mostra `gcc`
- [ ] Mudar uma linha em `src/` e reconstruir leva **menos de 5 s**
- [ ] `docker run ... id` **não** devolve `uid=0`

### 🔴 As cinco armadilhas

| Erro | Sintoma |
|------|---------|
| `CMD` em forma de shell | `docker stop` demora 10 s |
| `--host 127.0.0.1` | `connection refused` mesmo com `-p` |
| Sem `PYTHONUNBUFFERED=1` | Container morre sem nada no log |
| `USER` antes dos `apt-get` | O build falha por falta de permissão |
| `curl` no `HEALTHCHECK` | Sempre `unhealthy` na imagem slim |

---

## Etapa 3 — `.dockerignore`

### O que fazer

O arquivo já está pronto na raiz — **leia-o inteiro** e confira que
cobre o seu projeto.

### Pronto quando

```bash
docker build . 2>&1 | head -1
# Sending build context to Docker daemon   1.4MB    ← e não 400MB
```

- [ ] A primeira linha é `.env`
- [ ] `.venv/`, `.git/`, `__pycache__/` estão lá
- [ ] O contexto enviado é de poucos MB

> 🔴 **Ter `.env` no `.gitignore` não protege aqui.** São arquivos
> diferentes. É uma das formas mais comuns de vazar credencial: o
> `COPY . /app` leva o arquivo para uma camada, e a camada vai para o
> registro.

---

## Etapa 4 — Compose

### O que fazer

Complete o `docker-compose.yml`: descomente e preencha os serviços
`api`, `redis` e `migracao`.

### 🔴 Os dois erros que todo mundo comete

**1. `localhost` para achar o banco**

```yaml
❌ ATLAS_DB_URL: postgresql://atlas:senha@localhost:5432/atlas
✅ ATLAS_DB_URL: postgresql://atlas:${SENHA}@postgres:5432/atlas
#                                            ^^^^^^^^ NOME DO SERVIÇO
```

Dentro do container, `localhost` é o **próprio container**. O erro é
`connection refused`, e confunde porque a mesma URL funcionava fora.

**2. Publicar a porta do banco**

O banco **não** precisa de `ports:`. A API o alcança pela rede interna
do compose. Publicá-lo expõe o Postgres para a sua rede — e num
servidor, possivelmente para a internet.

Se você quiser usar o DBeaver, amarre ao loopback:
`"127.0.0.1:5432:5432"`.

### Pronto quando

- [ ] `docker compose up -d` sobe tudo
- [ ] `docker compose ps` mostra todos `healthy`
- [ ] Nenhum segredo literal no YAML
- [ ] Todo serviço com estado tem volume
- [ ] `docker compose down && up -d` preserva os dados

---

## Etapa 5 — Healthchecks

### 🔴 `depends_on` mente

```yaml
❌ depends_on: [postgres]
```

Isso garante que o **container iniciou** — o que leva milissegundos. O
Postgres leva de 2 a 30 segundos para aceitar conexão.

A API sobe, tenta conectar, leva `connection refused` e morre. Com
`restart: unless-stopped` ela reinicia até dar certo — e "funciona",
com uma cascata de erros em toda subida. **Na sua máquina rápida passa
na primeira; no CI, não.**

```yaml
✅ depends_on:
     postgres: {condition: service_healthy}
```

⚠️ **Só funciona se o `postgres` tiver `healthcheck`.**

### Pronto quando

- [ ] Os quatro serviços têm `healthcheck`
- [ ] Todos os `depends_on` usam `service_healthy`
- [ ] Cada healthcheck tem `start_period`
- [ ] Uma subida do zero **não** produz nenhum `connection refused`

> 🔑 **`start_period` é o parâmetro esquecido.** Sem ele, uma aplicação
> que leva 20 s para subir é marcada `unhealthy` nos primeiros 20 s — e
> com `restart` ligado, reiniciada. Laço infinito.
>
> Regra prática: `start_period` ≥ 2× o tempo normal de partida.

---

## Etapa 6 — Override de desenvolvimento

### O que fazer

Complete o `docker-compose.override.yml`: bind mount de `src/`,
`--reload`, portas dos bancos no loopback.

### Pronto quando

- [ ] Editar um arquivo em `src/` recarrega a API sem rebuild
- [ ] `docker compose config` mostra a mesclagem correta
- [ ] O `prod` (sem override) **não** tem `--reload` nem bind mount

---

## Etapa 7 — Auditoria

### O que fazer

Implemente o `scripts/auditar_containers.py`.

### Pronto quando

```bash
python scripts/auditar_containers.py
echo $?     # 0
```

- [ ] Zero achados 🔴
- [ ] 🔴 **E ele REPROVA quando deve** — veja abaixo

### 🔴 Teste o seu verificador

Antes de confiar nele, quebre o projeto de propósito:

```bash
# troque a tag por :latest        → deve acusar
# tire o USER do Dockerfile       → deve acusar
# ponha ENV SECRET_KEY=abc123     → deve acusar
# tire o volume do postgres       → deve acusar
# use depends_on em lista         → deve avisar
```

> 💭 **Um verificador que nunca reprova ninguém não está verificando
> nada** — e é pior que nenhum, porque dá sensação falsa de segurança.
> Isso vale para o linter, para o teste e para a auditoria.

---

## ✅ Checklist final

### Imagem

- [ ] Multi-stage; o compilador não está na final
- [ ] Menos de 250 MB
- [ ] Base com versão fixa, nunca `:latest`
- [ ] 🔴 Roda como usuário não-root
- [ ] 🔴 Nenhum segredo em `ENV`, `ARG` ou `COPY`
- [ ] `PYTHONUNBUFFERED=1`
- [ ] `HEALTHCHECK` sem `curl`
- [ ] 🔴 `CMD`/`ENTRYPOINT` em JSON
- [ ] 🔴 Escuta em `0.0.0.0`

### Compose

- [ ] Sem `version:`
- [ ] Toda imagem com versão fixa
- [ ] 🔴 Nenhum segredo literal
- [ ] Serviços com estado têm volume
- [ ] Bancos não publicados na rede
- [ ] 🔴 `condition: service_healthy`
- [ ] `restart: unless-stopped`

### Operação

- [ ] `up -d` do zero funciona sem erro
- [ ] `down` + `up -d` preserva os dados
- [ ] `docker compose stop api` leva menos de 2 s
- [ ] Log aparece em `docker compose logs`
- [ ] `docs/CONTAINERS.md` registra as decisões

---

## Erros que você provavelmente vai cometer

| Sintoma | Causa |
|---------|-------|
| `connection refused` do host | Escutou em `127.0.0.1` |
| `connection refused` para o banco | Usou `localhost` no lugar do nome do serviço |
| Container morre sem log | Faltou `PYTHONUNBUFFERED=1` |
| `docker stop` demora 10 s | `CMD` em forma de shell, ou faltou `exec` no entrypoint |
| Sempre `unhealthy` | `curl` não existe na imagem |
| Reinicia em laço | Sem `start_period` |
| `Exited (137)` | 🔴 OOM — o cgroup cumpriu o limite |
| Build refaz tudo sempre | `COPY .` antes das dependências |
| Imagem de 1,4 GB | Sem multi-stage |
| Dados sumiram | Sem volume, ou `down -v` |
| Segredo na imagem | Faltou `.env` no `.dockerignore` |
| Mudei o código e nada mudou | Faltou `--build` |

---

## Se você quiser ir além

1. **BuildKit e cache mount** — `RUN --mount=type=cache,target=/root/.cache/pip`
2. **Imagem multi-arquitetura** — `docker buildx build --platform linux/amd64,linux/arm64`
3. **Distroless** — sem shell; ótimo para segurança, doloroso para depurar
4. **`docker scout` / Trivy** — varredura de vulnerabilidade na imagem
5. **`hadolint`** — o linter consagrado de Dockerfile
6. **Assinatura de imagem** (cosign) — provar que a imagem é a que você construiu
7. **`.env` → gerenciador de segredos** — Vault, AWS Secrets Manager (M09)

> 📖 **Antes de publicar qualquer imagem**, leia o
> [Docker Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html)
> da OWASP. As regras deste roteiro cobrem os itens mais comuns; ele
> cobre o resto.
