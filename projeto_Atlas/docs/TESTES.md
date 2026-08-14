# Estratégia de testes do Atlas

> *"Temos medo de mexer no código."*

---

## O que a suíte é para

Não é para provar que o código está certo. É para **tornar a mudança
barata**.

O medo de mexer no código é racional quando qualquer alteração pode
quebrar algo em silêncio. A suíte existe para transformar esse medo
numa pergunta com resposta em 30 segundos: *"quebrei alguma coisa?"*

> 🔑 O valor de um teste não está em ter passado. Está em **ter
> falhado** no dia em que alguém quebrou o que ele protege.
>
> Um teste que nunca falhou em toda a vida do projeto pode estar
> protegendo algo — ou pode não estar testando nada. Do lado de fora,
> os dois casos são idênticos. É por isso que este módulo termina
> quebrando o código de propósito.

---

## Os três tipos, e o que decide entre eles

Esqueça a pirâmide desenhada. O que importa na prática são duas
perguntas: **quão rápido roda** e **quanta confiança dá**.

| Tipo | Roda em | Cobre | Quando falha, você sabe |
|------|---------|-------|-------------------------|
| **Unidade** | < 10 ms | uma função, sem I/O | exatamente onde está o bug |
| **Integração** | 10 ms – 1 s | camadas conversando | que a junção quebrou |
| **Ponta a ponta** | segundos | o caminho do usuário | que algo quebrou, não onde |

E o trade-off que decide a proporção:

```
      confiança  ▲                    ● ponta a ponta
   (se passou,   │              ● integração
    funciona)    │      ● unidade
                 └──────────────────────────►  custo
                                              (tempo + manutenção)
```

**A regra prática:** escreva o teste no nível mais barato que
consiga pegar o erro que você tem medo de cometer.

> 💭 Por que não fazer tudo em ponta a ponta, já que dá mais
> confiança? Porque uma suíte de 400 testes E2E leva 40 minutos, e uma
> suíte de 40 minutos não roda a cada mudança — roda antes do deploy,
> quando o custo de descobrir o erro já é dez vezes maior. Velocidade
> não é conforto: é o que determina **quando** você descobre o
> problema.

### No Atlas

| Camada | Tipo predominante | Por quê |
|--------|-------------------|---------|
| `modelos`, `regras`, `metricas` | unidade | lógica pura, sem I/O — teste barato e exato |
| `repositorio`, `orm` | integração | SQL só se prova contra um banco |
| `servicos` | integração | é onde as regras encontram os dados |
| `api/rotas` | integração (TestClient) | contrato HTTP: status, corpo, autorização |
| `dados/` (pipeline) | integração | idempotência e portão de qualidade |
| fluxo do pedido | 1–2 ponta a ponta | o caminho que não pode quebrar nunca |

---

## O que testar (e o que não)

### Teste comportamento, não implementação

```python
# ❌ acopla ao COMO
def test_calcular():
    assert calcular_total(pedido)._cache_usado is True

# ✅ verifica o QUE
def test_total_soma_itens_e_frete():
    assert calcular_total(pedido) == Decimal("1234.50")
```

O primeiro quebra quando você refatora sem mudar comportamento — que é
exatamente quando a suíte deveria ficar quieta e te dar confiança.
Testes assim treinam a equipe a apagar teste em vez de consertar
código.

### Não teste

- Bibliotecas de terceiros (o SQLAlchemy tem os testes dele)
- Getters e setters triviais
- Configuração estática

### 🔑 Teste, sempre

| O quê | Por quê |
|-------|---------|
| Todo bug que apareceu em produção | um bug sem teste volta |
| Os limites (0, 1, vazio, negativo, nulo) | é onde mora o erro |
| O caminho de erro, não só o feliz | ninguém testa o `except`, e é onde se esconde o pior |
| Toda propriedade de segurança | autorização, vazamento, injeção |
| Toda regra de negócio com dinheiro | o erro aqui não é bug, é prejuízo |

> 💡 **Bug encontrado = teste escrito primeiro.** Escreva o teste que
> reproduz o bug, veja-o falhar, e só então conserte. Se você
> consertar primeiro, nunca vai saber se o teste realmente pegava.

---

## Isolamento

> Um teste que depende da ordem é pior do que nenhum teste: ele falha
> em situações sem relação com o bug, e a equipe aprende a ignorá-lo.

### Como se prova isolamento

Rodar a suíte inteira **não prova nada** — estado de módulo é
recriado por processo, e a ordem é sempre a mesma.

```bash
# ❌ isto NÃO detecta dependência de ordem
pytest && pytest

# ✅ isto detecta: cada teste sozinho, num processo próprio
pytest --collect-only -q | while read id; do pytest "$id" -q || echo "FALHA SOZINHO: $id"; done

# ✅ e isto detecta acoplamento entre testes
pytest -p no:randomly --lf   # ou instale pytest-randomly e rode várias vezes
```

> 🔧 Você já viu isto falhar: no M07, a bateria "rode a suíte duas
> vezes" não detectou nada, e só a execução individual pegou o teste
> que dependia de ordem.

### A armadilha do SQLite

`poolclass=StaticPool` é obrigatório com `sqlite:///:memory:`. O banco
em memória pertence à **conexão**; o TestClient roda as rotas noutra
thread, abre outra conexão, e encontra um banco vazio:

```
sqlite3.OperationalError: no such table: produtos
```

Parece problema de modelo. Não é.

E o isolamento por transação (`BEGIN` + `ROLLBACK` por teste) **não
funciona no SQLite** — o `pysqlite` quebra savepoints. No Atlas o
banco é **recriado** por teste; o padrão com transação está
documentado para quando você migrar para PostgreSQL.

---

## Cobertura

⚠️ Cobertura é um **detector de buracos**, não um certificado.

Ela mede linhas **executadas**, não comportamento **verificado**:

```python
def test_nao_verifica_nada():
    calcular_total(pedido)      # 100% de cobertura, zero asserções
```

| Leitura | Significa |
|---------|-----------|
| Cobertura **baixa** | 🔴 há código sem nenhum teste — informação real |
| Cobertura **alta** | nada, por si só |

Use como **piso** (`--cov-fail-under=70`), nunca como meta. Uma equipe
com meta de 95% escreve testes sem asserção para bater a meta — e a
suíte fica mais lenta sem ficar mais segura.

> 🔑 Olhe o relatório, não o número. `--cov-report=term-missing` mostra
> **quais linhas** faltam. As que importam quase sempre são os ramos
> de erro.

---

## 🔑 O teste dos testes

Se cobertura não prova que os testes funcionam, o que prova?

**Quebrar o código de propósito e exigir que a suíte falhe.**

```
1. altere uma linha do código (troque + por -, > por >=, remova um filtro)
2. rode a suíte
3. a suíte DEVE ficar vermelha
4. se ficou verde, aquela linha não está testada — não importa a cobertura
```

Isso se chama **teste de mutação**, e é a única medida honesta de
qualidade de suíte que existe. `scripts/testar_os_testes.py` faz isso
de forma automatizada no Atlas.

### O exemplo mínimo, medido

```python
# regra.py
def desconto(total):
    if total > 1000:              # ← a mutação: > vira >=
        return total * 0.10
    return 0.0
```

Dois testes, e a diferença entre eles é tudo:

```python
def test_caso_tipico():           # ❌ sem asserção
    desconto(5000)

def test_limite():                # ✅ testa o limite
    assert desconto(1000.00) == 0.0
    assert desconto(1000.01) > 0
```

Trocando `>` por `>=` e rodando cada um:

| Teste | Cobertura | Mutante |
|-------|-----------|---------|
| `test_caso_tipico` | **75%** | 🔴 **sobreviveu** |
| `test_limite` | 75% | 🟢 morto |

**Mesma cobertura. Resultados opostos.** O primeiro teste executa a
linha e não confere nada; o segundo testa exatamente onde `>` e `>=`
divergem.

> 🔑 É por isso que "teste o limite, não o caso típico" não é
> preciosismo: `desconto(5000)` não distingue as duas versões da
> regra. Só `desconto(1000.00)` distingue.

> 💭 É o mesmo movimento que atravessa o manual inteiro: no M09 o
> portão de segredos passou porque a palavra estava no arquivo, e só
> plantar um segredo de verdade revelou. No M10, a bateria de
> idempotência aprovava um pipeline que não gerava arquivo nenhum. No
> M11, a regra de camadas aprovava SQL dentro de uma rota.
>
> Em todos os casos, o defeito só apareceu ao **atacar a própria
> verificação**. Testes não são exceção.

---

## Marcadores

```bash
pytest                          # tudo
pytest -m "not lento"           # o ciclo rápido, durante o trabalho
pytest -m integracao            # só o que precisa de banco
pytest -m seguranca             # antes de um deploy
```

🔴 `--strict-markers` está ligado: `@pytest.mark.lentoo` (com erro de
digitação) vira **erro**, não um teste silenciosamente ignorado.

---

## Preencha: o estado da sua suíte

_(preencha depois de rodar)_

| Métrica | Valor | Meta |
|---------|-------|------|
| Testes | | |
| Tempo da suíte rápida (`-m "not lento"`) | | < 10 s |
| Tempo da suíte completa | | < 2 min |
| Cobertura | | piso de _(preencha)_ |
| Mutantes sobreviventes | | 🔑 _(preencha — e explique cada um)_ |

> ⚠️ **Mutante sobrevivente que você não consegue explicar é um
> buraco de teste.** Mutante sobrevivente que você consegue explicar
> ("essa linha é log, mudá-la não muda comportamento") é normal —
> anote o motivo e siga.

---

*Atlas · Aurora Comércio · Módulo 12*
