# Runbook — Atlas

> **Status:** 🚧 esqueleto. Preencha **antes** de precisar.
>
> 💭 Este documento tem um leitor específico: **você, às 3h da manhã,
> com sono, com o site fora e o telefone tocando.**
>
> Escreva para essa pessoa. Frases curtas, comandos prontos para
> copiar, nenhuma explicação teórica. A teoria fica no `DEPLOY.md`.

---

## Antes de tudo

```bash
# 1. Está fora mesmo, ou é só comigo?
curl -sS -o /dev/null -w "%{http_code}\n" https://atlas.aurora.com.br/saude

# 2. O que os logs dizem?
ssh atlas-prod 'journalctl -u atlas -n 100 --no-pager'

# 3. O serviço está de pé?
ssh atlas-prod 'systemctl status atlas'
```

<!-- TODO: adicione o que for específico do SEU ambiente:
     painel de monitoramento, canal do time, quem acionar. -->

---

## 🔴 Regra de ouro

**Restabeleça primeiro. Investigue depois.**

Se houve deploy nos últimos 30 minutos, o rollback é a primeira
hipótese — não a última:

```bash
ssh atlas-prod /opt/atlas/rollback.sh
```

Ele leva segundos. Investigar com o site no ar é infinitamente melhor
do que investigar com o site fora.

---

## Incidente 1 — <!-- TODO: o mais provável -->

<!-- TODO: preencha com o incidente que você considera mais provável.

     Sugestão de estrutura:

     ### Sintoma
     O que a pessoa vê. Mensagem de erro exata, se houver.

     ### Diagnóstico rápido
     Os 2 ou 3 comandos que confirmam a hipótese.

     ### Correção
     Comandos prontos para copiar.

     ### Se não resolver
     Qual é a próxima hipótese.

     ─────────────────────────────────────────────────────────

     Candidatos, com o que você já sabe de cada um:

     · Banco fora do ar
       → a API responde 500; `pool_pre_ping` (M05) reconecta sozinho
         quando ele voltar

     · Certificado vencido
       → 🔴 previsível e evitável: monitore a data (M09_01)

     · Disco cheio
       → o Postgres para de aceitar escrita; olhe log e WAL primeiro

     · OOMKilled (M08)
       → `Exited (137)`; confirme com
         `docker inspect <c> --format '{{.State.OOMKilled}}'`

     · Deploy ruim
       → rollback, e só então investigue

     · Migração incompatível (M09_02)
       → 🔴 o rollback do CÓDIGO não desfaz o banco

     · Parceiro externo fora (M07)
       → o disjuntor deveria degradar em vez de derrubar; se derrubou,
         o desenho está errado
-->

---

## Incidente 2 — <!-- TODO -->

---

## Incidente 3 — <!-- TODO -->

---

## Comandos que você vai querer ter à mão

```bash
# ── Estado ──
ssh atlas-prod 'systemctl status atlas'
ssh atlas-prod 'journalctl -u atlas -f'
ssh atlas-prod 'journalctl -u atlas -p err --since "1 hour ago"'
ssh atlas-prod 'df -h && free -m'

# ── Qual versão está no ar? ──
ssh atlas-prod 'readlink /opt/atlas/atual'

# ── Reverter ──
ssh atlas-prod /opt/atlas/rollback.sh

# ── Recarregar sem derrubar ──
ssh atlas-prod 'sudo systemctl reload atlas'

# ── Banco ──
ssh atlas-prod 'docker compose exec postgres pg_isready -U atlas'
ssh atlas-prod 'docker compose exec postgres psql -U atlas -c "\l+"'

# ── Certificado ──
echo | openssl s_client -connect atlas.aurora.com.br:443 2>/dev/null \
    | openssl x509 -noout -dates
```

---

## Depois do incidente

<!-- TODO: adote o hábito do POST-MORTEM SEM CULPA.

     Perguntas que valem a pena:
       1. O que aconteceu, na linha do tempo?
       2. Quanto tempo até DESCOBRIR? E até RESOLVER?
       3. O monitoramento avisou, ou o cliente avisou?
       4. Que verificação teria pegado isso ANTES?
       5. O que muda no código, no pipeline ou neste runbook?

     🔑 O item 3 é o mais revelador. Se o cliente avisou primeiro,
        o problema não foi só o incidente — foi o monitoramento.

     💭 "Sem culpa" não é gentileza: é o que faz as pessoas contarem o
        que realmente aconteceu. Num ambiente que procura culpado,
        você recebe relatos editados — e conserta o problema errado.
-->

---

## Contatos

<!-- TODO:
     | Quem | Quando acionar | Como |
     |------|----------------|------|
     | ...  | ...            | ...  |

     E o mais importante: quem decide comunicar o cliente, e a partir
     de quanto tempo de indisponibilidade.
-->

---

## O pipeline de dados falhou (M10)

Este runbook cobre a **API fora do ar**. Falha do pipeline é outro
tipo de incidente, e tem outro documento: **`PIPELINE.md`**, seção 5.

A diferença importa mais do que parece:

| | API fora | Pipeline falhou |
|---|---|---|
| Quem percebe | o cliente, agora | ninguém, até de manhã |
| Urgência | 🔴 imediata | alta, mas você tem horas |
| Pior erro | demorar a agir | 🔴 **agir rápido demais** |

> 💭 **Por que a pressa é o inimigo aqui.** A API fora é visível e
> urgente: reverta primeiro, entenda depois. O pipeline é o oposto —
> o painel continua mostrando o dado de ontem, e ninguém está
> esperando. Forçar o portão às 3h para "resolver logo" publica um
> número errado que vai circular numa reunião antes que alguém note.
>
> Relatório de ontem com data de ontem é um inconveniente.
> Relatório de hoje com número errado é uma decisão errada.

**Só isto, agora:**

```bash
# o pipeline chegou a rodar?
journalctl -u atlas-pipeline -n 100 --no-pager

# qual verificação reprovou, e com que números?
grep portao /var/log/atlas/pipeline.jsonl | tail -5
```

Depois abra `PIPELINE.md` § 5 e siga. **Não rode com `--forcar`** sem
ter entendido por que o portão reprovou.
