# Integrações do Atlas

> **Status:** 🚧 esqueleto. Preencha conforme implementar.
>
> Este documento registra **decisões**, não descrições. O código já diz
> o que faz; aqui você explica *por quê* — para o você de daqui a seis
> meses, que não vai lembrar.

---

## Serviços de que dependemos

| Serviço | Para quê | Se cair, a Aurora… |
|---------|----------|--------------------|
| Transportadora Veloz | cotação de frete, rastreio | <!-- TODO --> |
| Gateway de pagamento | cobrança, notificação | <!-- TODO --> |
| Redis | cache, idempotência | <!-- TODO --> |

> 🔴 **Preencha a terceira coluna primeiro.** Ela é o requisito; o resto
> é implementação. Se alguma linha disser *"para de vender"*, o desenho
> está errado e a etapa 3 do roteiro é sobre consertar isso.

---

## Política de resiliência

<!-- TODO: preencha com os valores que você escolheu e o porquê -->

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| `timeout connect` | | |
| `timeout read` | | |
| Tentativas | | |
| Espera base | | |
| Disjuntor: falhas para abrir | | |
| Disjuntor: tempo aberto | | |

### O que repetimos

| Situação | Repete? | Por quê |
|----------|---------|---------|
| `408`, `425`, `5xx` | ✅ | transitório |
| `429` | ⏱️ | obedecendo ao `Retry-After` |
| `400`, `401`, `403`, `404`, `409`, `422` | ❌ | vai falhar de novo |
| `ConnectError`, `ConnectTimeout` | ✅ | nem chegou a sair |
| `ReadTimeout` num `POST` | 🔴 | **só com `Idempotency-Key`** |

> 🔴 **O `ReadTimeout` é o caso ambíguo.** Você enviou e não recebeu
> resposta: foi processado? Não há como saber. Repetir pode duplicar;
> não repetir pode perder.

### Degradação

<!-- TODO: para cada serviço, o que acontece quando o disjuntor abre?

     Frete: valor estimado com aviso? 503 com Retry-After? Bloqueia
     o checkout?

     Registre a decisão E a fórmula da estimativa. -->

---

## Webhooks

### Recebidos

| Origem | Rota | Eventos |
|--------|------|---------|
| Gateway | `POST /webhooks/gateway` | `pagamento.aprovado`, `pagamento.recusado` |

### As quatro verificações

<!-- TODO: descreva como cada uma está implementada no seu código -->

1. **Assinatura HMAC** — `hmac.compare_digest`, nunca `==`
2. **Timestamp** — janela de <!-- TODO --> segundos
3. **Idempotência** — <!-- TODO: Redis com TTL? tabela com UNIQUE? -->
4. **Resposta rápida** — `202` e processamento posterior

### Como testar em desenvolvimento

<!-- TODO: um gateway público não alcança o seu `localhost`. As saídas
     usuais são ngrok / cloudflared / um script que simula o envio.
     Documente a que você usa, com o comando. -->

### O que acontece se uma notificação se perder?

<!-- TODO: 🔴 responda honestamente.

     Webhook é rápido, não é confiável. Existe uma varredura periódica
     das cobranças pendentes? Se não existe, qual é o plano quando o
     financeiro disser "o cliente pagou e o pedido não liberou"? -->

---

## Cache

### Chaves

<!-- TODO: liste as chaves que você usa, no formato
     `atlas:recurso:v1:id`, com o TTL de cada uma -->

| Chave | TTL | Por que este TTL |
|-------|-----|------------------|
| `atlas:produto:v1:<sku>` | | |
| `atlas:estoque:v1:<sku>` | | |
| `atlas:cotacao:v1:<peso>:<cep>` | | |

### Invalidação

<!-- TODO: liste TODOS os caminhos de escrita e qual chave cada um
     invalida. Este inventário é o que impede o caminho esquecido. -->

| Operação | Invalida |
|----------|----------|
| `POST /produtos` | |
| `PATCH /produtos/{sku}` | |
| `DELETE /produtos/{sku}` | |
| `PATCH .../estoque` | |
| webhook de pagamento | |
| carga noturna | |

### Estouro de cache

<!-- TODO: qual defesa você implementou?
     trava distribuída (SET NX EX) · TTL com jitter · recomputação
     antecipada — ou uma combinação -->

---

## Testes

### Como rodar

```bash
pytest                          # tudo
pytest -m "not lento"           # o que roda em segundos
pytest -m seguranca             # só as verificações de segurança
pytest --cov=atlas --cov-report=term-missing
```

### O que NÃO é testado, e por quê

<!-- TODO: 🔴 esta seção vale mais do que a lista do que é testado.

     Toda suíte tem buracos. Documentá-los é a diferença entre um risco
     conhecido e uma surpresa. Exemplos do tipo de coisa a registrar:

       · o comportamento sob concorrência real (dois pedidos do último item)
       · a API real da transportadora (só testamos o dublê)
       · migrações do Alembic aplicadas em ordem
       · o que acontece com o Redis fora do ar                     -->

---

## Decisões registradas

### Por que `respx` e não `unittest.mock`?

<!-- TODO -->

### Por que a chave de idempotência é por operação, não por tentativa?

<!-- TODO -->

### Por que cursor e não offset na sincronização?

<!-- TODO -->

### Por que degradar em vez de devolver erro?

<!-- TODO -->
