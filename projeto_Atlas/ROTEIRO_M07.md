# Roteiro — Módulo 07 · Integrações e Testes

> **Objetivo:** conectar o Atlas ao mundo — transportadora, gateway de
> pagamento, cache — e construir a suíte de testes que dá coragem para
> mexer em tudo isso.

---

## A situação

A Atlas API v1 está no ar. Ela lê e escreve no banco da Aurora, valida
entrada, autentica usuário e não vaza `custo`. Ótimo.

E é uma ilha.

| Quem | O que disse na reunião |
|------|------------------------|
| **Chefe** | *"A transportadora caiu 8 minutos e o nosso checkout caiu junto. Oito minutos sem vender."* |
| **Financeiro** | *"O cliente paga o boleto e espera até 5 minutos para o pedido liberar. A gente pergunta ao gateway de 5 em 5 minutos."* |
| **Suporte** | *"A tela de estoque consulta o banco a cada 2 segundos, para 30 pessoas. É a mesma pergunta, 900 vezes por minuto."* |
| **Você** | *"Precisamos mudar o cálculo de frete e ninguém quer mexer."* |

Quatro dores, quatro respostas: **resiliência**, **webhook**, **cache**
e **testes**.

---

## Ordem de trabalho

```
1. Testes primeiro          ← contra-intuitivo, e é de propósito
2. Cliente HTTP base
3. Transportadora + degradação
4. Webhooks
5. Cache
6. A suíte completa
```

> 💭 **Por que testes antes das integrações?**
>
> Porque integração é o código mais difícil de testar **depois**. Se
> você escrever o cliente da transportadora primeiro, vai acabar com
> `httpx.post` no meio de uma função de 60 linhas — e testar aquilo
> exigirá reescrever tudo.
>
> Escrever o teste primeiro força o desenho testável: cliente separado,
> exceções de domínio, dependências injetadas.

---

## Etapa 1 — A base de testes

### O que fazer

1. Instale:

   ```bash
   pip install pytest pytest-cov respx fakeredis
   ```

2. Configure o `pyproject.toml`:

   ```toml
   [tool.pytest.ini_options]
   testpaths = ["tests"]
   addopts = "-q --strict-markers"
   markers = [
       "lento: demora mais de 1 segundo",
       "integracao: precisa de serviço externo real",
       "seguranca: verifica uma propriedade de segurança",
   ]
   ```

3. Implemente `tests/conftest.py`: fixtures `sessao`, `cliente`,
   `catalogo`, `usuarios`, `cache_teste`.

4. Escreva o teste que **prova o isolamento**:

   ```python
   def test_banco_comeca_vazio(cliente):
       assert cliente.get("/produtos").json() == []
   ```

### Pronto quando

- [ ] `pytest` roda e sai com código 0
- [ ] `test_banco_comeca_vazio` passa mesmo depois de outro teste criar produtos
- [ ] 🔴 **Cada teste passa também quando rodado sozinho**

### 🔴 A verificação que quase ninguém faz

```bash
# 1. a suíte inteira
pytest

# 2. cada teste, isolado
pytest --collect-only -q | grep :: | while read t; do
  pytest -q --tb=no "$t" >/dev/null || echo "🔴 só passa acompanhado: $t"
done
```

Rodar a suíte duas vezes **não** detecta dependência de ordem: um estado
guardado num módulo Python é recriado a cada processo. O que denuncia é
rodar cada teste sozinho.

> ⚠️ **`poolclass=StaticPool`.** Se aparecer
> `sqlite3.OperationalError: no such table: produtos`, é isto. Um banco
> `:memory:` pertence à conexão, e o TestClient roda as rotas noutra
> thread.

---

## Etapa 2 — O cliente HTTP base

### O que fazer

Implemente `atlas/integracoes/cliente_http.py`: timeouts, retry com
backoff e jitter, disjuntor, métricas.

### Pronto quando

- [ ] Nenhum `httpx.Client` do projeto sem `timeout`
- [ ] `422` não é repetido; `503` é
- [ ] A espera cresce exponencialmente **e tem jitter**
- [ ] 🔴 `POST` sem `Idempotency-Key` **não** é repetido
- [ ] O disjuntor falha em microssegundos quando aberto

### 🔴 Verifique você mesmo

```bash
# nenhum cliente sem timeout
grep -rn "httpx.Client(" src/ | grep -v timeout      # deve sair vazio

# nenhum segredo literal
grep -rnE '(secret|senha|password|token|api_key)\s*=\s*["'"'"'][^"'"'"']{8,}' src/
```

> 🔴 **A decisão que define este arquivo:** repetir um `POST` sem chave
> de idempotência pode cobrar o cliente duas vezes.
>
> O caso perigoso é o `ReadTimeout`: você enviou "cobre R$ 500" e não
> recebeu resposta. Foi cobrado? **Não há como saber.** Repetir pode
> duplicar; não repetir pode não cobrar.

---

## Etapa 3 — Transportadora e degradação

### O que fazer

1. `ClienteVeloz` com renovação automática de token.
2. `cotar()` e `entregas()` (paginado por **cursor**).
3. 🔴 `cotar_com_estimativa()` — a degradação.
4. `sincronizar_entregas()` — idempotente e retomável.

### Pronto quando

- [ ] O token renova **antes** de expirar, com margem
- [ ] Quem chama `cotar()` não sabe que existe token
- [ ] 🔴 **Com a Veloz fora, o checkout continua funcionando**
- [ ] A sincronização rodada duas vezes não duplica nada
- [ ] Morrendo no meio, ela retoma de onde parou

### 🔴 O teste que define esta etapa

```python
@respx.mock
def test_checkout_sobrevive_a_transportadora_fora():
    respx.post(URL).mock(side_effect=httpx.ConnectError("fora"))
    resultado = cliente.cotar_com_estimativa(2.0, "13010-000")
    assert resultado["estimado"] is True
    assert resultado["valor"] > 0
```

> 💭 **Degradar é melhor do que quebrar.** O cliente prefere comprar com
> um frete aproximado a não conseguir comprar. Mas seja honesto:
> `estimado: True` precisa aparecer na tela e ficar registrado no
> pedido, para o financeiro reconciliar depois.

---

## Etapa 4 — Webhooks

### O que fazer

1. `conferir_webhook()` — assinatura e timestamp.
2. `ja_processado()` — idempotência no Redis.
3. `POST /webhooks/gateway` — valida, confirma rápido, processa depois.

### Pronto quando

- [ ] Sem assinatura → `401`
- [ ] Assinatura forjada → `401`
- [ ] Timestamp de 1 hora atrás → `401`
- [ ] 🔴 **Mesmo evento 4 vezes → processado 1 vez**, e as 4 respondem 2xx
- [ ] A resposta sai em menos de 200 ms
- [ ] A idempotência sobrevive a reiniciar a API

### As quatro obrigações

| # | Obrigação | Contra o quê |
|---|-----------|--------------|
| 1 | Ler o corpo **cru** (`await requisicao.body()`) | assinatura que não bate |
| 2 | HMAC com `hmac.compare_digest` | falsificação e ataque de tempo |
| 3 | Timestamp dentro da janela | reenvio malicioso |
| 4 | `id` do evento já visto | reenvio **legítimo** |

> 🔴 **Reenvio não é hipótese — é o funcionamento normal.** O gateway
> espera a sua confirmação; se ela não chegar, ele reenvia. A Stripe
> reenvia por até 3 dias.
>
> 🔴 **E responda 2xx ao repetido.** Para o gateway, "já recebi" é
> sucesso. Um erro faria ele reenviar para sempre.

---

## Etapa 5 — Cache

### O que fazer

Implemente `atlas/integracoes/cache.py` e aplique nas leituras caras.

### Pronto quando

- [ ] Chaves no formato `atlas:recurso:v1:id`
- [ ] TTL diferente por tipo de dado, cada um justificado
- [ ] Invalidação em **todos** os caminhos de escrita
- [ ] 🔴 Proteção contra estouro (trava distribuída + jitter no TTL)
- [ ] Um teste que falha se algum caminho de escrita esquecer de invalidar

### A decisão que importa

Não é *"como evito divergir?"* — é **"por quanto tempo posso divergir
sem causar dano?"**

| Dado | TTL | Por quê |
|------|-----|---------|
| Nome do produto | horas | muda raramente |
| Preço | minutos | promoção precisa entrar |
| **Estoque** | 🔴 segundos | vender o que não tem custa dinheiro |
| Saldo | 🔴 não cacheie | |

> 🧭 **Use TTL *e* invalidação explícita.** A invalidação cuida do caso
> normal; o TTL é a rede de segurança para o caminho que você esqueceu.

---

## Etapa 6 — A suíte completa

### Pronto quando

- [ ] `pytest` sai com código 0
- [ ] Nenhum teste toca a internet
- [ ] Os marcadores dividem a suíte (`-m "not lento"` roda em segundos)
- [ ] Existem testes de segurança, de integração e de regressão
- [ ] 🔴 Cada teste passa sozinho

---

## ✅ Checklist final

### Cliente

- [ ] Um `Client` por serviço, reaproveitado
- [ ] 🔴 **Timeout em todos**
- [ ] Retry só nos status transitórios
- [ ] Backoff exponencial **com jitter**
- [ ] 🔴 **`POST` só repete com `Idempotency-Key`**
- [ ] `Retry-After` obedecido
- [ ] Disjuntor com degradação
- [ ] Paginação com teto
- [ ] Credenciais do ambiente

### Webhook

- [ ] Corpo cru
- [ ] `compare_digest`
- [ ] Janela de timestamp
- [ ] Idempotência persistente
- [ ] Resposta rápida
- [ ] Rota de auditoria

### Cache

- [ ] Chave com namespace e versão
- [ ] TTL justificado por tipo
- [ ] Invalidação em toda escrita
- [ ] Proteção contra estouro

### Testes

- [ ] `conftest.py` com fixtures
- [ ] 🔴 **`StaticPool`**
- [ ] `dependency_overrides`
- [ ] Cada teste passa sozinho
- [ ] `respx` nas integrações
- [ ] Teste de comportamento **ausente** (`call_count`)
- [ ] Marcadores com `--strict-markers`
- [ ] Um teste de regressão por bug encontrado

---

## Erros que você provavelmente vai cometer

| Sintoma | Causa |
|---------|-------|
| `no such table` só nos testes | falta `poolclass=StaticPool` |
| Teste passa junto, falha sozinho | estado vazando entre testes |
| Fixture com `scope="module"` mutável | um teste suja o próximo |
| Assinatura de webhook nunca bate | você reserializou o corpo |
| Gateway reenvia para sempre | você respondeu erro ao repetido |
| Cobrança duplicada | `POST` repetido sem `Idempotency-Key` |
| Chave de idempotência não protege | gerada a cada tentativa |
| API trava sem erro nenhum | cliente HTTP sem timeout |
| Banco cai no pico | estouro de cache |
| Dado velho para sempre | invalidação sem TTL de segurança |
| Sincronização duplica registros | paginação por offset em lista viva |
| Laço infinito na madrugada | paginação sem teto |
| 100% de cobertura e bugs em produção | testes que executam sem verificar |

---

## Se você quiser ir além

1. **`tenacity`** no lugar do retry manual — compare o que ganha e perde
2. **Fila de verdade** (Celery/RQ) no lugar do `BackgroundTasks` — M10
3. **Teste de contrato** contra a API real, num job diário separado
4. **`pytest-randomly`** para embaralhar a ordem dos testes automaticamente
5. **Mutation testing** (`mutmut`) — a resposta honesta a "meus testes servem?"
6. **OpenTelemetry** para rastrear uma requisição atravessando os serviços

> 📖 **Leitura:** *Release It!*, de Michael Nygard, é o livro sobre
> exatamente este módulo — timeouts, disjuntores, falhas em cascata e
> por que sistemas caem em conjunto.
