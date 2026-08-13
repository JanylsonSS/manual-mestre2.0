# Roteiro — Módulo 09 · Deploy e CI/CD

> **Objetivo:** tirar você do caminho crítico. Ao final, `git push` faz
> o resto — e se algo quebrar, o sistema avisa antes do cliente.

---

## A situação

> *"O deploy é assim: eu entro no servidor com a senha de root, faço
> `git pull`, mato o processo com `kill`, e subo de novo com `nohup`.
> Se der errado, eu... não sei."*
>
> *"E a gente descobre que o site caiu quando um cliente liga."*

Cada frase dessa é um problema com nome:

| O que fazem | Problema | Etapa |
|-------------|----------|-------|
| `ssh root@` com senha | Login privilegiado, sem chave | 2 |
| `git pull` | Build em produção | 4 |
| `kill` | Corta requisições em andamento | 1 |
| `nohup ... &` | Ninguém reinicia se cair | 5 |
| (sem rollback) | Restaurar backup de 3 dias | 6 |
| (cliente avisa) | Sem monitoramento | 8 |

---

## Ordem de trabalho

```
1. Preparar a aplicação      ← os ajustes de produção
2. Acesso ao servidor        ← chave, usuário, endurecimento
3. Proxy e TLS
4. Estrutura de deploy       ← releases + symlink
5. systemd
6. Rollback                  ← 🔴 antes de precisar
7. Pipeline
8. Observabilidade
```

> 💭 **Repare que o rollback vem antes do pipeline.** Automatizar
> deploy sem ter rollback é automatizar o risco.

---

## Etapa 1 — Preparar a aplicação

### O que fazer

Rode a auditoria 12-factor da aula 09_01 no seu projeto e conserte os
🔴.

Os que costumam sobrar:

| Fator | O que falta | Onde mexer |
|-------|-------------|------------|
| 11 · Logs | Ainda escreve em `saida/atlas.jsonl` | `observabilidade.py` (M04) |
| 9 · Descartabilidade | Não trata `SIGTERM` | `lifespan` (M06) |
| 6 · Sem estado | Cache ou contador em memória | mover para Redis (M07) |

### Pronto quando

- [ ] Log em JSON no **stdout**
- [ ] `Ctrl+C` encerra sem traceback
- [ ] Escuta em `0.0.0.0`, porta do ambiente
- [ ] 🔴 Nada guardado entre requisições no processo
- [ ] Número de workers vem de `WEB_CONCURRENCY`

### 🔴 Prove o fator 6

Suba com `gunicorn -w 3`, chame uma rota que incrementa um contador em
memória 12 vezes, e veja três contadores independentes.

Se o seu Atlas passar nesse teste, é porque você já tinha movido o
estado para o Redis no M07 — e naquele momento não era sobre deploy.

---

## Etapa 2 — Acesso ao servidor

### O que fazer

```bash
ssh-keygen -t ed25519 -C "deploy@atlas"
ssh-copy-id -i ~/.ssh/atlas_deploy.pub deploy@SEU_IP
```

Depois crie o usuário `deploy`, o `sudoers.d` mínimo, e endureça o
`sshd_config`.

### Pronto quando

- [ ] Entra por chave, sem senha
- [ ] `PermitRootLogin no` e `PasswordAuthentication no`
- [ ] O usuário `deploy` só pode `systemctl restart/reload atlas`
- [ ] `~/.ssh/config` com `atlas-prod` configurado

### ⚠️ Antes de reiniciar o sshd

**Abra uma segunda sessão SSH e deixe-a aberta.** Se você errar a
configuração, ela é a sua única forma de voltar atrás — a sessão já
aberta sobrevive ao restart, uma nova não conseguiria entrar.

Todo mundo aprende isso da forma difícil, uma vez. Não seja essa
pessoa.

---

## Etapa 3 — Proxy e TLS

### Pronto quando

- [ ] HTTPS funcionando, HTTP redirecionando
- [ ] `certbot renew --dry-run` passa
- [ ] Os quatro `proxy_set_header`
- [ ] 🔴 `--forwarded-allow-ips` restrito ao proxy
- [ ] `client_max_body_size` definido

### 🔴 Prove o IP forjado

```bash
curl -H "X-Forwarded-For: 203.0.113.42" https://atlas.aurora.com.br/auth/eu
```

Se o seu log registrar `203.0.113.42`, qualquer um forja o próprio IP —
e o seu limitador de taxa (M07) e a auditoria não valem nada.

---

## Etapa 4 — Estrutura de deploy

```
/opt/atlas/
├── releases/20260813-143022-9f8e7d/
├── compartilhado/
│   ├── .env               🔑 config FORA do release
│   └── uploads/
└── atual -> releases/...  🎯 um symlink
```

### Pronto quando

- [ ] `rsync` envia sem `.env`, `.venv/`, `.git/`, `tests/`
- [ ] 🎯 A troca do symlink usa `mv -T` (atômico)
- [ ] O `.env` de cada release aponta para `compartilhado/`
- [ ] A limpeza preserva os 5 últimos **e o ativo**

### 🔴 O detalhe que quase todo mundo erra

`ln -sfn` **não é atômico** — ele remove e recria, e há uma janela de
microssegundos em que `atual` não aponta para nada. Sob carga, alguém
cai nela, e o bug acontece uma vez a cada dez mil requisições.

Use `mv -T`, que usa `rename()`: ou é o antigo, ou é o novo.

---

## Etapa 5 — systemd

### Pronto quando

- [ ] `systemd-analyze verify infra/atlas.service` limpo
- [ ] `systemctl reload atlas` não derruba conexões
- [ ] `TimeoutStopSec` **maior** que o `--graceful-timeout`
- [ ] `StartLimitBurst` evita laço de reinício
- [ ] O log aparece no `journalctl`

---

## Etapa 6 — 🔴 Rollback (antes do pipeline)

### Pronto quando

- [ ] `rollback.sh` volta em **um comando**
- [ ] Ele verifica a saúde depois
- [ ] Você **cronometrou**: menos de 60 segundos

### O teste que vale

1. Faça um deploy que quebra de propósito
2. Cronometre do "descobri" até o "voltou"
3. Se passar de 60 segundos, simplifique

> 💭 **Rollback é a operação que você faz sob pressão.** Ela tem que
> ser trivial — e você precisa ter feito pelo menos uma vez com calma
> para confiar nela com pressa.

---

## Etapa 7 — Pipeline

### O que fazer

Complete `.github/workflows/ci.yml` e `cd.yml`.

### Pronto quando

- [ ] O CI roda a cada push
- [ ] Ordem por custo crescente
- [ ] 🔴 O portão de segredos barra um segredo plantado
- [ ] O CD só roda com CI verde
- [ ] `environment: producao` exige aprovação
- [ ] 🔴 `if: failure()` reverte sozinho

### 🔴 O teste que ninguém faz

**Para cada portão, quebre o código de propósito e confirme que ele
reprova:**

```bash
# 1. commite um segredo         → o CI deve barrar
# 2. quebre um teste            → o CI deve barrar
# 3. ponha :latest no Dockerfile → a auditoria deve barrar
# 4. quebre a sintaxe de um .py  → o lint deve barrar
```

> 🔴 **Um portão que você nunca viu reprovar é um portão aberto.**
>
> Ao testar as baterias desta lista, desliguei o portão de segredos
> trocando o `grep` por um `echo`. A verificação estática continuou
> dizendo *"o CI tem portão de segredos"* — porque a palavra estava lá.
> Só executá-lo revelou que ele não fazia nada.

---

## Etapa 8 — Observabilidade

### Pronto quando

- [ ] Log JSON com id de correlação em toda linha
- [ ] 🔴 Nenhum dado pessoal no log (LGPD)
- [ ] `/metricas` com os quatro sinais
- [ ] 🎯 Ao menos **uma métrica de negócio**
- [ ] Alertas só para o que exige ação imediata
- [ ] Alerta de certificado a vencer

### 🎯 A métrica que mais importa

Se você só puder monitorar uma coisa: **pedidos por hora**.

Um deploy pode manter latência, erro e CPU perfeitos e mesmo assim
zerar as vendas — um botão que sumiu, um formulário que não envia. Os
quatro sinais dizem que o *sistema* está bem; só a métrica de negócio
diz que a *empresa* está bem.

### 🔴 O simulacro

Derrube o banco de propósito, com a API no ar. Cronometre:

- Quanto tempo até você **descobrir**?
- Quanto tempo até **resolver**?

Se você descobriu porque olhou, e não porque foi avisado, o
monitoramento ainda não existe.

---

## ✅ Checklist final

### Aplicação
- [ ] 12 fatores auditados, 🔴 resolvidos
- [ ] Log no stdout, sem dado pessoal
- [ ] Encerra com educação
- [ ] Sem estado no processo

### Servidor
- [ ] SSH só por chave, root sem login
- [ ] Usuário de deploy com sudo mínimo
- [ ] HTTPS com renovação testada
- [ ] 🔴 `forwarded_allow_ips` restrito
- [ ] `--reload` desligado

### Deploy
- [ ] `releases/` + symlink atômico
- [ ] Migração antes do código, e compatível
- [ ] 🔴 Rollback em menos de 60 segundos
- [ ] Deploy verifica a saúde e reverte sozinho

### Pipeline
- [ ] CI com 4+ portões
- [ ] 🔴 **Cada portão testado**
- [ ] CD só com CI verde e aprovação
- [ ] Nenhum segredo impresso

### Observabilidade
- [ ] Quatro sinais + métrica de negócio
- [ ] Alertas que exigem ação
- [ ] 🔴 `RUNBOOK.md` com três incidentes
- [ ] 🔴 **Restauração de backup testada**

---

## Erros que você provavelmente vai cometer

| Sintoma | Causa |
|---------|-------|
| `connection refused` do host | Escutou em `127.0.0.1` |
| Laço de redirecionamento | Falta `X-Forwarded-Proto` |
| Rate limit não funciona | `X-Forwarded-For` forjável |
| Deploy corta requisições | `restart` em vez de `reload` |
| `docker stop` demora 10s | `CMD` shell, ou falta `exec` |
| Site fora sem aviso | Certificado venceu |
| Contador conta errado | Estado em memória com N workers |
| Teste passa com código quebrado | 🔴 Bytecode velho — limpe `__pycache__` |
| Segredo no log | `set -x`, `curl -v`, ou substring |
| Rollback não resolve | A migração destruiu dado |
| Deploy pela metade | Faltou `set -e` no script |
| Ninguém viu o alerta | Fadiga de alerta |

---

## Se você quiser ir além

1. **Blue/green** — dois ambientes completos, troca de tráfego instantânea
2. **Canário** — 5% do tráfego na versão nova antes de promover
3. **Feature flags** — publicar código desligado, ligar depois
4. **OpenTelemetry** — rastrear uma requisição atravessando serviços
5. **Terraform** — a infraestrutura também versionada
6. **Chaos engineering** — derrubar coisas de propósito, em horário combinado

> 📖 **Leitura:** o [Google SRE Book](https://sre.google/books/) é
> gratuito e é a referência sobre os quatro sinais, orçamento de erro e
> post-mortem sem culpa.
