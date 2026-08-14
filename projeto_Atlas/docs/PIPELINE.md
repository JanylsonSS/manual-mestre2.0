# Pipeline de dados do Atlas

> Documento operacional. Quem for acordado às 3h da manhã lê este
> arquivo primeiro.
>
> ⚠️ **Este é um gabarito.** As seções marcadas com `_(preencha)_` só
> você pode responder — elas dependem de decisões que você tomou ao
> construir o pipeline. Um documento com o gabarito intacto é pior que
> nenhum: ele dá a impressão de que existe documentação.

---

## 1. O que este pipeline faz

Uma frase, sem jargão, que um gerente entenda:

> _(preencha — algo como: "toda madrugada, junta os pedidos do banco,
> do CSV do parceiro e da API da transportadora, confere, e publica os
> agregados que alimentam o painel da Aurora.")_

**Horário:** _(preencha)_
**Duração típica:** _(preencha — meça, não estime)_
**Duração máxima aceitável:** _(preencha — depois disso, alerte)_

---

## 2. Desenho

```
   banco (réplica) ─┐
   CSV do parceiro ─┼─→ bronze ─→ prata ─→ [PORTÃO] ─→ ouro ─→ painel
   API transport.  ─┘                          │
                                               └─→ alerta + ouro de ontem
                                                    continua no ar
```

| Camada | O que é | Pode apagar? | Retenção |
|--------|---------|--------------|----------|
| bronze | cru, como chegou | 🔴 **não** | _(preencha)_ |
| prata | limpo e validado | sim, derivável | _(preencha)_ |
| ouro | agregado | sim, derivável | _(preencha)_ |
| quarentena | rejeitados | sim, após análise | _(preencha)_ |
| estado | marcas d'água | 🔴 **não** | permanente |

> 💭 A coluna "pode apagar" é a que mais importa numa emergência de
> disco cheio às 3h da manhã. Sem ela, alguém apaga o bronze.

---

## 3. Decisões que você precisa registrar

Estas não têm resposta certa. Têm resposta **sua**, e ela precisa
estar escrita — porque daqui a seis meses ninguém vai lembrar por que
o pipeline faz o que faz, inclusive você.

### 3.1 Dinheiro é `Decimal` ou centavos em `int`?

_(preencha e justifique)_

Contexto: `float` acumula erro em milhões de linhas e o fechamento não
bate por centavos inexplicáveis. Parquet não guarda `Decimal` de forma
portátil em toda ferramenta.

### 3.2 A quarentena é JSONL ou Parquet?

_(preencha)_

JSONL é fácil de `grep` às 3h da manhã. Parquet é fácil de agregar
depois. Você vai fazer mais qual das duas coisas?

### 3.3 `extrair_api` é crítica?

_(preencha)_

Se sim, a API do parceiro cair significa não ter relatório nenhum. Se
não, significa relatório sem os dados de frete. **É decisão da Aurora,
não sua** — mas é você que precisa perguntar e anotar a resposta aqui,
com data e nome de quem decidiu.

### 3.4 Margem de segurança da marca d'água

Valor atual: `MARGEM_SEGURANCA = 15 minutos` _(confirme ou ajuste)_

Como você chegou nesse número: _(preencha — o critério é a maior
duração de transação observada na origem, com folga)_

### 3.5 O que conta como nulo

`isna()` não pega `""`, `"None"`, `"NULL"`, `"N/A"`, nem `0` num campo
de id. A lista que o Atlas trata como nulo: _(preencha)_

---

## 4. Operação

### Rodar

```bash
python scripts/rodar_pipeline.py                 # ontem
python scripts/rodar_pipeline.py 2026-03-12      # um dia
python scripts/rodar_pipeline.py 2026-03-01 2026-03-31   # intervalo
```

### Códigos de saída

| Código | Significado | O que fazer |
|--------|-------------|-------------|
| 0 | sucesso | nada |
| 1 | tarefa crítica falhou | ver seção 5 |
| 2 | trava ocupada | normal se outra rodada está em curso |
| 3 | portão de qualidade reprovou | 🔴 ver seção 5.3 |

### Onde olhar

| O quê | Onde |
|-------|------|
| Log da rodada | _(preencha)_ |
| Marcas d'água | `dados/lago/estado/marca_<fonte>.json` |
| Manifestos | `dados/lago/bronze/origem=*/data_ingestao=*/_manifesto.json` |
| Rejeitados | `dados/lago/quarentena/` |

---

## 5. Quando quebra

### 5.1 O pipeline não rodou

1. A trava ficou presa? Veja se há processo vivo. Se não houver e a
   trava existir, ela é órfã — libere.
2. O agendador disparou? `systemctl list-timers` (M09).
3. O disco encheu? `df -h`. **Não apague o bronze.**

### 5.2 Uma fonte falhou

- A marca d'água **não avança** quando a extração falha. Rodar de novo
  busca a mesma janela. É seguro.
- Se a origem ficou dias fora, o próximo lote vem grande e a
  verificação de volume vai reclamar. É o comportamento correto —
  confirme que o volume grande é legítimo antes de forçar.

### 5.3 🔴 O portão reprovou

**Não force.** O portão reprovou porque algo mudou.

1. Leia qual verificação falhou e com que números.
2. Se foi **volume**: a origem mudou um filtro? Houve feriado?
3. Se foi **unicidade**: a origem começou a mandar duplicata? Quantas?
4. Se foi **coerência**: pergunte à Aurora antes de relaxar a regra.

O ouro de ontem continua no ar. O painel mostra dado de ontem, e isso
é **muito melhor** do que mostrar o número errado de hoje. Você tem
tempo para investigar direito.

> ⚠️ Se você já forçou o portão mais de uma vez, a regra provavelmente
> está errada — conserte a regra em vez de contornar. Um portão que se
> contorna toda semana não existe.

### 5.4 O número está errado mas o portão passou

O caso mais difícil, e o motivo da camada bronze existir.

1. Ache a rodada: `_manifesto.json` tem a janela e o `sha256`.
2. Leia o **bronze** daquele dia — o dado como chegou.
3. Refaça a conta à mão para uma linha.
4. A divergência está na origem, na transformação ou na definição da
   métrica? As três acontecem. A terceira é a mais comum, e se resolve
   em `docs/METRICAS.md`, não no código.

---

## 6. Reprocessar

```bash
python scripts/rodar_pipeline.py 2026-03-01 2026-03-31
```

Antes de rodar, três perguntas:

1. **É seguro?** Só se o pipeline for idempotente. Prove antes:
   compare os hashes do ouro de duas rodadas do mesmo dia.
2. **Vai pesar na origem?** 90 dias de extração pode derrubar a
   réplica. Rode fora do horário e considere ler do bronze em vez de
   reextrair.
3. **O ouro antigo vai sumir?** Se a regra mudou, o número de março
   **vai mudar**. Alguém já usou esse número numa apresentação.
   Avise antes, não depois.

> 🔑 Reprocessamento sequencial, nunca paralelo. A verificação de
> volume compara com o histórico — que rodadas paralelas estão
> escrevendo ao mesmo tempo.

---

## 7. Como testar que o portão funciona

Uma vez por trimestre, estrague o dado de propósito:

| Estrague | Verificação que deve pegar |
|----------|---------------------------|
| duplique 10 linhas na prata | unicidade |
| zere um preço | faixa |
| corte o lote para 5% | volume 🔑 |
| ponha custo > preço | coerência |
| apague uma coluna obrigatória | obrigatórias |
| entregue lote vazio | completude |

Se alguma **não** pegar, você tem uma verificação decorativa.

> 💭 A pergunta que separa quem tem portão de quem tem a ilusão de um:
> **quando foi a última vez que ele reprovou algo?** Se a resposta for
> "nunca", ele provavelmente não funciona.

---

## 8. Contatos

| Assunto | Quem | Como |
|---------|------|------|
| Origem: banco | _(preencha)_ | |
| Origem: CSV do parceiro | _(preencha)_ | |
| Origem: API transportadora | _(preencha)_ | |
| Definição de métrica | _(preencha)_ | |
| Dono do painel | _(preencha)_ | |

---

*Atlas · Aurora Comércio · Módulo 10*
