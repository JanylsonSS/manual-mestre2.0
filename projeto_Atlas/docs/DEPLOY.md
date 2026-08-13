# Deploy do Atlas

> **Status:** 🚧 esqueleto. Preencha conforme implementar.
>
> Este documento explica **como** e **por quê**. O que fazer quando
> quebra está no `RUNBOOK.md` — separado de propósito, porque são
> leituras diferentes em momentos diferentes.

---

## Como publicar

```bash
git push origin main
```

<!-- TODO: descreva o que acontece depois. Algo como:

     1. o CI roda (qualidade, segurança, testes, auditoria)
     2. se passar, o CD aguarda aprovação no ambiente `producao`
     3. aprovado, o deploy.sh envia, migra, troca o symlink, recarrega
     4. verifica /saude por até 60s
     5. se falhar, reverte sozinho
-->

### Publicar à mão (quando o pipeline estiver fora)

```bash
./scripts/deploy.sh producao
```

### Reverter

```bash
ssh atlas-prod /opt/atlas/rollback.sh
```

---

## Ambientes

<!-- TODO: preencha.

     | Ambiente | Onde | Dados | Quem publica |
     |----------|------|-------|--------------|
     | desenvolvimento | | | |
     | homologação | | | |
     | produção | | | |

     🔴 E responda: os três rodam o MESMO artefato? Se você reconstrói
        a imagem para cada um, não testou o que subiu — testou um
        parente.
-->

---

## Estrutura no servidor

```
/opt/atlas/
├── releases/          últimos 5
├── compartilhado/
│   ├── .env           🔑 config, fora do release
│   └── uploads/
└── atual -> releases/...
```

<!-- TODO: explique por que `.env` e `uploads/` ficam fora do release.
     (Dica: sobrevivem a deploy E a rollback.) -->

---

## Decisões registradas

<!-- 🔴 Esta seção é a razão de o arquivo existir. -->

### Por que este servidor / plataforma?

<!-- TODO: VPS, PaaS ou orquestrador? Com números:
     custo mensal, tempo de operação, o que você deixou de fazer para
     manter isso.

     💭 A progressão sensata é PaaS ou VPS + Compose até doer, e só
        então orquestrador. "Até doer" tem sinais concretos: mais de
        3 serviços com escala independente, necessidade de
        auto-escala, ou mais de um deploy por dia por pessoa
        diferente.
-->

### Quantos workers, e por quê?

<!-- TODO: 🔴 não use a fórmula `(2 × núcleos) + 1` sem pensar.

     Ela é para workers SÍNCRONOS. Com `UvicornWorker`, cada worker já
     atende milhares de conexões pelo event loop — multiplicar por 2
     só gasta memória.

     E `os.cpu_count()` devolve os núcleos do HOST, não os do cgroup.
     Num container com `--cpus=0.5` numa máquina de 64 núcleos, a
     fórmula dá 129 workers.

     Declare o número em `WEB_CONCURRENCY` e ajuste MEDINDO.
     Registre aqui o número e a medição que o justificou.
-->

### Deploy automático em produção: sim ou não?

<!-- TODO: 🔴 responda com critérios, não com opinião.

     ✅ Automatize se: a suíte é confiável · o rollback é de um
        comando · existe homologação · o deploy é reversível

     🔴 Não automatize se: os testes são poucos · não há rollback ·
        a migração é destrutiva

     Se a resposta for "ainda não", registre O QUE precisa mudar para
     virar sim. Sem isso, "ainda não" vira "nunca".
-->

### Migrações: como e quando

<!-- TODO: registre a sua política.

     🔴 A ordem: migração ANTES do código, e COMPATÍVEL — o código
        velho precisa funcionar com o schema novo.

     ✅ adicionar coluna/tabela/índice
     🔴 renomear · remover · mudar tipo · NOT NULL sem default

     Para renomear sem queda: três deploys.

     E onde ela roda? (Serviço separado no compose, initContainer,
     passo do pipeline — NUNCA no start-up da aplicação com várias
     instâncias.)
-->

### Backup

<!-- TODO: 🔴 e a pergunta que importa não é "existe backup?".

     É: QUANDO FOI A ÚLTIMA VEZ QUE VOCÊ RESTAUROU UM?

     Registre:
       · o que é copiado, com que frequência, para onde
       · quanto tempo o backup fica guardado
       · 🔴 a data do último teste de RESTAURAÇÃO
       · quanto tempo a restauração levou

     Backup não testado não é backup — é esperança com custo de
     armazenamento.
-->

---

## Segredos

<!-- TODO: onde mora cada um?

     | Segredo | Desenvolvimento | Produção |
     |---------|-----------------|----------|
     | ATLAS_SECRET_KEY | .env local | ? |
     | senha do Postgres | .env local | ? |
     | chave de deploy (SSH) | ~/.ssh | GitHub Secrets |
     | credencial da transportadora (M07) | .env local | ? |

     🔴 E o procedimento de ROTAÇÃO: como você troca um segredo sem
        derrubar o sistema? Quem tem acesso? Com que frequência?
-->

---

## Monitoramento

<!-- TODO:
     · onde ficam os logs, e por quanto tempo
     · qual painel de métricas
     · quais alertas existem e para onde vão
     · 🎯 qual é a métrica de NEGÓCIO que você acompanha
-->

---

## Diagrama

```
    git push
       │
       ▼
   ┌────────┐   ┌────────┐   ┌───────────┐
   │   CI   │──►│   CD   │──►│  servidor │
   └────────┘   └────────┘   └───────────┘
                                   │
                          ┌────────┴────────┐
                          │ nginx :443 (TLS)│
                          └────────┬────────┘
                                   ▼
                          gunicorn :8000
                                   │
                    ┌──────────────┼──────────────┐
                    ▼              ▼              ▼
                postgres        mongo          redis
```

<!-- TODO: ajuste para a SUA arquitetura real. -->
