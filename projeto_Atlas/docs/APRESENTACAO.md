# Apresentando o Atlas

> Como mostrar o sistema — para a Aurora, numa entrevista, ou num
> portfólio.

---

## O erro que quase todo mundo comete

Abrir a apresentação por `src/`.

Ninguém se impressiona com estrutura de pastas. Quem assiste — cliente,
entrevistador, colega — está fazendo uma pergunta diferente da que
você está respondendo:

| Você quer mostrar | Eles querem saber |
|---|---|
| o que você construiu | que problema isso resolve |
| como está organizado | o que acontece quando quebra |
| as tecnologias | por que essas, e não outras |

> 🔑 A regra que organiza tudo aqui: **comece pela dor, termine na
> falha.** O meio é o sistema.

---

## O roteiro de 10 minutos

Cronometre. Dez minutos é o que você tem antes de alguém interromper —
e a interrupção é boa, mas você quer chegar ao item 5 antes dela.

### 1 · A dor (30 s)

> *"A Aurora vendia bem e não sabia quanto vendia por cidade. Toda
> segunda alguém passava a tarde somando planilha, e o número nunca
> batia. Apresentaram um número errado para um investidor — tinha
> pedido cancelado no meio."*

Sem slide. Sem código. Só a frase.

### 2 · A resposta, rodando (2 min)

```bash
python main.py relatorio --todos
```

Mostre o número aparecendo. **Depois** mostre o arquivo de rejeições:

> *"E estas 14 linhas não entraram. Aqui está o motivo de cada uma."*

> 💡 O arquivo de rejeições impressiona mais que o relatório. O
> relatório qualquer script gera; o arquivo de rejeições mostra que
> você pensou no dado ruim — e todo mundo que já trabalhou com dado
> sabe que ele é a regra, não a exceção.

### 3 · A API (2 min)

Suba e abra o `/docs`:

```bash
uvicorn atlas.api.aplicacao:criar_app --factory --reload
```

Faça **duas** requisições, nesta ordem:

1. Uma que funciona.
2. 🔑 Uma que é **recusada** — o usuário de leitura tentando ver
   margem, e levando 403.

A segunda vale mais que a primeira. Qualquer CRUD faz a primeira.

### 4 · O pipeline (2 min)

```bash
python scripts/rodar_pipeline.py 2026-03-12
sha256sum dados/lago/ouro/*.parquet
python scripts/rodar_pipeline.py 2026-03-12
sha256sum dados/lago/ouro/*.parquet   # os MESMOS hashes
```

> *"Rodar duas vezes o mesmo dia produz exatamente o mesmo resultado.
> É isso que torna seguro reprocessar março em novembro, quando a
> regra de negócio mudar."*

### 5 · 🔑 O que acontece quando quebra (3 min)

**Este é o item que diferencia.** Reserve tempo para ele.

Escolha **um** e execute ao vivo:

| Demonstração | O que dizer |
|---|---|
| Derrube a transportadora e faça um pedido | *"O checkout continua. Frete estimado, aviso honesto."* |
| Duplique linhas e rode o pipeline | *"O portão reprova. O painel continua com o dado de ontem — que é melhor que o número errado de hoje."* |
| `from atlas.repositorio import ...` numa rota | *"O CI fica vermelho. A arquitetura não é um documento, é uma regra."* |
| Troque um `>` por `>=` numa regra | *"Um teste falha. Cobertura não pegaria isso."* |

### 6 · O fecho (30 s)

> *"A pergunta é a mesma do primeiro dia: quanto vendemos por cidade.
> O que mudou é o que acontece quando algo dá errado."*

---

## Os três slides, se precisar de slides

Só três. Mais que isso e você está apresentando slides, não o sistema.

**1 · Antes e depois**

| | Antes | Depois |
|---|---|---|
| Relatório | tarde de segunda | de madrugada, sozinho |
| Confiança | "acho que bate" | portão de qualidade |
| Mudar código | medo | suíte + mutação |
| Subir versão | ritual de sexta | `git push` |

**2 · O desenho** — as duas entradas (API e pipeline) e as camadas.
Gere com `python scripts/verificar_camadas.py --grafo`, que produz
Mermaid: um diagrama gerado do código está sempre certo; um desenhado
à mão está errado desde o segundo commit.

**3 · Uma decisão, com o custo** — pegue um ADR e mostre a seção de
consequências **negativas**.

> 💭 Este terceiro slide é contra-intuitivo e é o que mais funciona.
> Quem entrevista já viu cem apresentações em que tudo foi ótimo.
> "Escolhi dois bancos, e o preço foi não ter chave estrangeira entre
> pedido e produto — por isso existe a reconciliação" mostra
> julgamento, que é o que não dá para ensinar rápido.

---

## Perguntas que você vai receber

| Pergunta | Onde está a resposta |
|---|---|
| *"Por que dois bancos?"* | ADR 0001 |
| *"Por que JWT e não sessão?"* | ADR 0002 |
| *"Como você sabe que os testes prestam?"* | 🔑 mutação (M12) |
| *"E se o pipeline falhar de madrugada?"* | `docs/PIPELINE.md` § 5 |
| *"Quanto disso é seu?"* | seja exato — veja abaixo |
| *"Escala para quanto?"* | 🔑 veja abaixo |

### Sobre "escala para quanto?"

A resposta honesta é quase sempre *"não sei, não medi nesse volume"* —
e **essa é uma boa resposta**, se vier acompanhada de duas coisas:

1. o que você **mediu** (o M10 tem números reais de pandas, Polars e
   DuckDB nos mesmos dados);
2. onde está o próximo gargalo e como você saberia
   (*"a extração vai pesar primeiro; está documentado no ADR 0004 com
   o gatilho de quando revisitar"*).

Inventar um número é a pior saída. Quem perguntou provavelmente já
sabe a ordem de grandeza.

### Sobre "quanto disso é seu?"

Diga a verdade, e diga com precisão:

> *"Segui um manual de estudos que dava a estrutura em esqueleto —
> assinaturas e comentários — e implementei. Os erros que encontrei no
> caminho estão documentados: o `StaticPool` do SQLite em teste, o
> executável disfarçado de CSV que passou pela validação, o CI que
> ficou verde com bytecode velho."*

Isso é mais forte que "fiz sozinho", e verificável. **Falar dos erros
que você encontrou é o sinal mais confiável de que você realmente
construiu** — quem só seguiu tutorial não tem essa lista.

---

## Preparação

### Uma hora antes

- [ ] `python scripts/verificar_release.py` — tudo verde
- [ ] Banco com dados **plausíveis** (nomes reais, valores reais)
- [ ] Terminal com fonte grande e tema claro
- [ ] `docs/` aberto numa aba, para responder rápido
- [ ] Os comandos num arquivo, para copiar — não digite ao vivo

### ⚠️ Ensaie a demonstração de falha

É a única parte que pode dar errado de um jeito que você não previu —
justamente porque quebra o sistema de propósito. Rode antes. Duas
vezes.

### E tenha um plano B

Se a demo ao vivo travar (rede, porta ocupada, container que não
sobe), tenha a saída **gravada em texto** num arquivo. Mostrar o log de
uma execução real é 90% do valor, e leva 10 segundos.

> 💡 Não peça desculpa e não conserte ao vivo. *"A demo travou, aqui
> está a saída de quando rodei há pouco"* e siga. Quem assiste se
> importa muito menos com isso do que você imagina — e ficar
> depurando em público queima o tempo do item 5, que é o que importa.

---

*Atlas · Aurora Comércio · Módulo 13*
