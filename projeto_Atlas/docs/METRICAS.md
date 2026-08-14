# Dicionário de métricas do Atlas

> O documento que encerra a discussão sobre "qual número é o certo".

---

## Por que este arquivo existe

Numa reunião, o financeiro diz que julho fechou em R$ 1,84 milhão. O
painel do Atlas mostra R$ 1,79 milhão. Começa a discussão sobre qual
sistema está com bug.

Quase nunca é bug. É que **"faturamento" é duas coisas diferentes** e
ninguém escreveu qual é qual:

| | Atlas | Financeiro |
|---|---|---|
| Pedidos cancelados | exclui | exclui |
| Pedidos pendentes | exclui | **inclui** (regime de competência) |
| Frete | exclui | **inclui** |
| Fuso do fechamento | UTC | Brasília |

Nenhum dos dois está errado. Os dois respondem perguntas diferentes.

Sem este arquivo, essa reunião se repete todo mês, dura 40 minutos, e
termina com alguém prometendo "conferir depois". Com ele, dura dois
minutos.

> 🔑 **A regra:** nenhum número entra no painel sem uma entrada aqui.
> Se você não consegue escrever a definição, você não entendeu a
> métrica bem o bastante para publicá-la.

---

## Gabarito de uma entrada

Copie este bloco para cada métrica nova.

```markdown
## <nome da métrica>

**Pergunta que responde:** <em português, para um humano>

**Cálculo:** <a fórmula, sem ambiguidade>

**Filtros aplicados:** <quais linhas entram>

**NÃO inclui:** <🔑 o mais importante — o que fica de fora>

**Fuso horário:** <em que fuso o período é fechado>

**Granularidade:** <por dia? mês? cidade? SKU?>

**Fonte:** <arquivo do ouro que a contém>

**Diverge de:** <qual outro sistema mostra número diferente, e por quê>

**Decidido por:** <nome> em <data>
```

> 💭 O campo **NÃO inclui** parece redundante e é o que mais resolve
> discussão. "Faturamento é a soma das vendas" não diz se frete entra.
> "NÃO inclui frete, impostos nem descontos posteriores" diz.

---

## Métricas do Atlas

_(preencha uma seção por métrica — os títulos abaixo são o mínimo)_

### faturamento

**Pergunta que responde:** _(preencha)_

**Cálculo:** _(preencha — ex.: `SUM(quantidade × preco_unitario)`)_

**Filtros aplicados:** _(preencha — ex.: `status = 'pago'`)_

**NÃO inclui:** _(preencha — frete? impostos? devolução?)_

**Fuso horário:** _(preencha — 🔴 um pedido de 31/07 às 22h em Brasília
é 01/08 em UTC. Em qual mês ele entra?)_

**Fonte:** `dados/lago/ouro/faturamento_por_cidade.parquet`

**Diverge de:** _(preencha)_

**Decidido por:** _(preencha)_

---

### margem

**Cálculo:** _(preencha)_

> 🔴 **A armadilha aritmética.** Estas duas contas dão números
> diferentes e as duas se chamam "margem":
>
> ```
> média das margens individuais  →  30%
> margem sobre o total           →  18%
> ```
>
> `(receita_total − custo_total) / receita_total` é quase sempre a que
> responde à pergunta do negócio. Escreva **qual das duas** você usou.

**NÃO inclui:** _(preencha — custo de frete? de aquisição de cliente?)_

**Decidido por:** _(preencha)_

---

### ticket médio

**Cálculo:** _(preencha)_

> ⚠️ Média por **pedido** ou por **cliente**? São métricas diferentes e
> ambas se chamam "ticket médio". E a média é sensível a outlier: uma
> venda corporativa de R$ 400 mil move o ticket médio do mês inteiro.
> Considere publicar a **mediana** junto, ou pelo menos saber a
> resposta quando perguntarem.

---

### curva ABC

**Cálculo:** _(preencha — participação acumulada no faturamento)_

**Cortes:** A até _(80%?)_, B até _(95%?)_, C o resto

> 💭 Os cortes 80/95 são convenção, não lei. Se a Aurora usa outros,
> use os dela — e escreva aqui que foram escolhidos, não herdados.

---

### taxa de rejeição (qualidade)

**Cálculo:** `linhas em quarentena / linhas lidas`

**Por que está aqui:** porque o número absoluto não significa nada. 400
rejeições é muito ou pouco? O que importa é a **tendência**:

| Padrão | Leitura |
|--------|---------|
| 0,02% todo dia | ruído normal da origem |
| 0,02% → 14% num dia | 🔴 a origem mudou algo. Investigue. |

**Fonte:** manifestos + `dados/lago/quarentena/`

---

## Métricas que a Aurora pede e o Atlas **não** calcula

_(preencha)_

Tão importante quanto documentar o que existe. Quando alguém perguntar
"cadê a taxa de recompra?", a resposta tem que estar escrita — com o
motivo (não temos o dado? não foi priorizado? não é confiável?).

---

## Histórico de mudanças de definição

🔴 **Toda mudança de definição muda números do passado.** Alguém já
usou o número antigo numa apresentação. Registre.

| Data | Métrica | Mudança | Motivo | Quem |
|------|---------|---------|--------|------|
| _(preencha)_ | | | | |

> Quando mudar uma definição, **reprocesse o histórico** e avise quem
> usa o painel — antes, não depois.

---

*Atlas · Aurora Comércio · Módulo 10*
