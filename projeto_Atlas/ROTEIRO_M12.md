# Roteiro — Módulo 12 · A suíte de testes

> **Objetivo:** trocar o medo de mexer no código por uma pergunta com
> resposta em 30 segundos.

Sem notebooks — só projeto. Você já aprendeu pytest no **M07 · Aula
03**; aqui a suíte deixa de ser três arquivos e vira a rede de
segurança do sistema inteiro.

---

## A situação

> *"Ninguém quer mexer no cálculo de frete. Funciona. Se quebrar, a
> gente só descobre quando o cliente reclamar."*
>
> *"A gente tem 70% de cobertura. Mas mês passado subiu um bug de
> arredondamento que ninguém pegou."*

Duas frases, e a segunda é a mais interessante:

| O que acontece | Problema | Etapa |
|----------------|----------|-------|
| Ninguém mexe no que funciona | Sem rede de segurança | 1–3 |
| 70% de cobertura e bug passou | 🔑 Cobertura não mede o que importa | 5 |
| Teste falha e ninguém sabe por quê | Dependência de ordem | 4 |
| Suíte demora 8 min | Não roda durante o trabalho | 2 |

> 💭 O segundo item é o assunto de verdade deste módulo. É fácil ter
> uma suíte grande; é difícil ter uma suíte que **pega bug**. Os dois
> se parecem muito de fora — mesma cobertura, mesmo CI verde — e a
> diferença só aparece no dia do incidente.

---

## Ordem de trabalho

```
1. Estruturar          ← unidade / integração, e a regra de cada uma
2. Escrever            ← camada por camada, do mais barato ao mais caro
3. Ligar ao CI         ← com piso de cobertura
4. Provar isolamento   ← 🔑 cada teste sozinho
5. Testar os testes    ← 🔑🔑 mutação: quebre o código de propósito
```

> 🔴 As etapas 4 e 5 são o módulo. As três primeiras qualquer tutorial
> ensina — e produzem exatamente a suíte de 70% que deixou o bug de
> arredondamento passar.

---

## Etapa 1 — Estruturar

**Pastas:** `tests/unidade/` e `tests/integracao/` (já criadas)

### A regra de cada pasta

| Pasta | Regra | Alvo de tempo |
|-------|-------|---------------|
| `unidade/` | 🔴 **nada toca disco, banco ou rede** | < 10 ms por teste |
| `integracao/` | banco e HTTP dublado; **nunca rede real** | < 1 s por teste |

Os arquivos do M07 (`test_seguranca.py`, `test_integracoes.py`) ficam
onde estão — mova-os depois, se quiser.

### Como saber se vazou I/O para `unidade/`

```bash
pytest tests/unidade --durations=10
```

Qualquer coisa acima de ~20 ms merece investigação. Um único teste com
banco nessa pasta contamina o tempo de todos — e o valor dela é ser
rápida o bastante para rodar a cada `Ctrl+S`.

### ✅ Pronto quando

- [ ] `pytest tests/unidade` roda em menos de 2 segundos
- [ ] Nenhum teste de `unidade/` usa a fixture `sessao`
- [ ] `pytest -m "not lento"` é o seu comando do dia a dia

---

## Etapa 2 — Escrever

Os esqueletos estão prontos, com os casos que importam já apontados.
Preencha na ordem: `unidade/` primeiro (barato e exato), depois
`integracao/`.

### 🔑 Três hábitos que decidem se a suíte serve

**1. Teste comportamento, não implementação.**

```python
assert calcular_total(pedido)._cache_usado is True   # ❌
assert calcular_total(pedido) == Decimal("1234.50")  # ✅
```

O primeiro quebra quando você refatora sem mudar comportamento — que é
exatamente quando a suíte deveria ficar quieta e te dar confiança.

**2. Nunca calcule o esperado com a fórmula do código.**

```python
(100, 100 * TAXA)   # ❌ testa que a fórmula é ela mesma
(100, 118.00)       # ✅ número conferido à mão
```

O primeiro passa **mesmo com a fórmula errada**.

**3. Teste os limites, não os casos típicos.**

Se a regra é "acima de R$ 1.000 ganha 10%", teste `999.99`, `1000.00`
e `1000.01`. O caso de R$ 5.000 não distingue `>` de `>=` — e é
exatamente essa confusão que a etapa 5 vai caçar.

### ⚠️ E afirme a mensagem, não só a exceção

```python
with pytest.raises(ValorInvalido, match="quantidade"):
    validar(linha)
```

Sem o `match`, o teste passa quando a função rejeita pelo motivo
**errado** — e você fica com uma mensagem inútil em produção achando
que testou.

### ✅ Pronto quando

- [ ] Toda regra de negócio com dinheiro tem teste de limite
- [ ] Todo caminho de erro tem teste (não só o caminho feliz)
- [ ] O teste do M01 continua valendo: os números batem
- [ ] 🔴 O teste da transação existe: pedido com 3º item sem estoque
      não altera o estoque dos dois primeiros

---

## Etapa 3 — Ligar ao CI

**Arquivos:** `pyproject.toml` e `.github/workflows/ci.yml`

### O que fazer

Descomente o `addopts` com cobertura e defina o piso:

```toml
addopts = "-q --strict-markers --strict-config -ra --durations=10 \
           --cov=atlas --cov-report=term-missing --cov-fail-under=70"
```

### 🔴 Sobre o número do piso

Escolha o piso **abaixo** da cobertura que você já tem, e suba aos
poucos. Piso acima do atual deixa o CI vermelho no dia 1, e a primeira
reação da equipe é baixar o piso — aí ele nunca mais sobe.

E não persiga 95%. Uma equipe com meta de 95% escreve testes sem
asserção para bater a meta:

```python
def test_nao_verifica_nada():
    calcular_total(pedido)      # 100% de cobertura, zero asserções
```

A suíte fica mais lenta sem ficar mais segura.

> 🔑 Olhe o `--cov-report=term-missing`, não o número. Ele diz **quais
> linhas** faltam, e as que importam quase sempre são os ramos de
> erro — o `except` que ninguém testa e onde se esconde o pior.

### ✅ Pronto quando

- [ ] O job de testes roda no CI e reprova quando um teste quebra
- [ ] O piso de cobertura está ligado e é realista
- [ ] Você **quebrou um teste de propósito** e viu o CI vermelho

---

## Etapa 4 — 🔑 Provar isolamento

> Um teste que depende da ordem é pior do que nenhum: ele falha em
> situações sem relação com o bug, e a equipe aprende a ignorá-lo.

### Rodar a suíte duas vezes não prova nada

Você já viu isso falhar. No M07, a bateria "rode a suíte duas vezes"
não detectou nada — estado de módulo é recriado a cada processo, e a
ordem é sempre a mesma. Só a execução **individual** pegou o teste
acoplado.

```bash
# ✅ cada teste sozinho, num processo próprio
pytest --collect-only -q | grep "::" | while read id; do
  pytest "$id" -q >/dev/null 2>&1 || echo "FALHA SOZINHO: $id"
done
```

Ou use `python scripts/testar_os_testes.py --ordem`.

### E instale o `pytest-randomly`

```bash
pip install pytest-randomly
```

Ele embaralha a ordem a cada execução. Testes que só passavam na ordem
"certa" começam a falhar.

> ⚠️ Ele vai quebrar coisas na primeira vez. **Não desinstale.** Cada
> falha é uma dependência de ordem que já existia e que você não
> estava vendo. A suíte não piorou — ficou honesta.

### As duas causas quase sempre são

| Causa | Sintoma |
|-------|---------|
| Estado de módulo (cache, contador, singleton) | passa sozinho, falha em grupo |
| Banco não recriado entre testes | `UNIQUE constraint failed` no segundo teste |

### ✅ Pronto quando

- [ ] Todo teste passa quando rodado **sozinho**
- [ ] A suíte passa com `pytest-randomly` em três execuções seguidas
- [ ] Nenhum teste depende de outro ter rodado antes

---

## Etapa 5 — 🔑🔑 Testar os testes

**Arquivo:** `scripts/testar_os_testes.py` (esqueleto)

### A pergunta que cobertura não responde

Cobertura diz quais linhas **rodaram**. Não diz se alguém **conferiu**
o resultado. A pergunta certa é:

> **Se eu quebrar esta linha, algum teste fica vermelho?**

E o jeito de responder é quebrar de verdade:

```
1. troque um operador   (+ vira -, > vira >=, and vira or)
2. rode a suíte
3. VERMELHA → 🟢 mutante morto: a linha está protegida
   VERDE    → 🔴 mutante sobreviveu: a linha NÃO está testada
4. desfaça e repita
```

Um mutante que sobrevive é uma mudança de comportamento que **passaria
no seu CI sem ninguém notar**.

### ⚠️ As armadilhas de escrever isso

| Armadilha | O que acontece |
|-----------|----------------|
| `texto.replace(">", ">=")` | troca tudo, o arquivo nem compila, o mutante "morre" e você marca a linha como protegida |
| Não restaurar em `finally` | Ctrl-C deixa o código-fonte mutado no disco |
| Sem timeout | `i < n` → `i > n` num `while` trava o script para sempre |
| Mutar `tests/` | mutantes lá sobrevivem sempre e enchem o relatório de ruído |
| Não conferir a suíte antes | se ela já está vermelha, todo mutante "morre" e o escore dá 100% |

### 💭 Que escore é bom?

Não existe número universal — desconfie de quem der um. O que importa
é **onde** estão os sobreviventes:

| Sobreviveu em | Leitura |
|---------------|---------|
| `formatacao.py` | provavelmente tudo bem |
| `regras.py` | 🔴 regra de negócio sem teste |
| `seguranca.py` | 🔴🔴 pare o que está fazendo |

Um escore de 60% concentrado nas camadas críticas vale mais que 85%
espalhado.

### 🔑 E teste o testador

Apague as asserções de um teste seu e rode o script. **O escore tem
que despencar.** Se não despencar, o script está mentindo — e você
acabou de descobrir isso do jeito barato.

### ⚠️ Onde isso roda

**Não** no CI de cada push: mutação leva de minutos a horas e
transformaria cada PR numa espera. Ponha num job **agendado**
(semanal) ou manual.

O CI de push carrega a suíte e o piso de cobertura. A mutação é a
auditoria periódica que diz se aquele piso significa alguma coisa.

### ✅ Pronto quando

- [ ] O script roda e reporta `arquivo:linha:` de cada sobrevivente
- [ ] Você explicou **cada** sobrevivente em `regras/` e `seguranca/`
- [ ] Apagar asserções derruba o escore
- [ ] O job semanal está no CI

---

## O que você tem no fim

```
projeto_Atlas/
├── tests/
│   ├── conftest.py              ← fixtures compartilhadas
│   ├── unidade/                 ← < 10 ms, sem I/O
│   ├── integracao/              ← banco e HTTP dublado
│   ├── test_seguranca.py        ← M07
│   └── test_integracoes.py      ← M07
├── scripts/
│   └── testar_os_testes.py      ← 🔑 mutação + isolamento
└── docs/TESTES.md               ← a estratégia, e o porquê
```

E a resposta para *"quebrei alguma coisa?"* em 30 segundos.

---

## O fecho

Este módulo tem uma simetria com todos os anteriores, e vale nomear.

No M09, o portão de segredos passou porque a palavra estava no
arquivo. No M10, a bateria de idempotência aprovou um pipeline que não
gerava arquivo nenhum. No M11, a regra de camadas aprovou SQL dentro
de uma rota. Agora, no M12, a suíte com 70% de cobertura deixou passar
o bug de arredondamento.

Quatro módulos, quatro verificações que pareciam funcionar e não
funcionavam. Em todos os casos o defeito só apareceu ao **atacar a
própria verificação** — plantar o segredo, esvaziar o ouro, escrever o
import proibido, mutar a linha.

> 🔑 É a ideia mais transferível do manual inteiro, e ela não é sobre
> teste: **toda salvaguarda precisa ser vista falhando pelo menos uma
> vez.** Até lá, ela é uma esperança com aparência de garantia.

---

*Atlas · Aurora Comércio · Módulo 12*
