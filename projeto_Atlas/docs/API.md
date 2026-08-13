# API do Atlas — referência

> **Status:** 🚧 esqueleto. Preencha conforme implementar.
>
> Este documento é **seu**, não meu. Cada `TODO` abaixo é uma decisão
> que você precisa tomar e registrar — não uma lacuna a ser copiada de
> algum lugar.

---

## Por que documentar se o `/docs` já existe?

O `/docs` (Swagger UI) responde *"quais rotas existem e que campos elas
aceitam"*. Ele é gerado do código e nunca fica desatualizado.

O que ele **não** responde:

- Por que `DELETE` faz exclusão lógica em vez de física
- Por que qualquer funcionário pode ver qualquer pedido
- O que fazer quando o `409` aparece
- Como obter um token na prática

Documentação gerada cobre o **contrato**. Este arquivo cobre as
**decisões**. Os dois são necessários.

---

## Base

| | |
|---|---|
| Base URL (dev) | `http://127.0.0.1:8000` |
| Formato | JSON, UTF-8 |
| Autenticação | Bearer token (JWT) |
| Docs interativos | `/docs` · ReDoc em `/redoc` |
| Especificação | `/openapi.json` |

---

## Autenticação

### Obter um token

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ana@aurora.com.br&password=SUA_SENHA"
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expira_em_minutos": 60
}
```

> ⚠️ **Por que `form-data` e não JSON?** Porque a especificação OAuth2
> exige. É a única rota da API que não recebe JSON — e é o que faz o
> botão **Authorize** do `/docs` funcionar.

### Usar o token

```bash
TOKEN="cole-aqui"
curl http://127.0.0.1:8000/produtos -H "Authorization: Bearer $TOKEN"
```

### Papéis

| Papel | Pode |
|-------|------|
| `leitor` | Consultar produtos e pedidos |
| `operador` | + criar/alterar produtos e pedidos, ajustar estoque |
| `admin` | + apagar produtos, ver custo e margem, ler relatórios |

A hierarquia é cumulativa: `admin` pode tudo que `operador` pode.

---

## Rotas

<!-- TODO: preencher com um exemplo executável por rota, incluindo
     ao menos um caso de ERRO em cada. Um `curl` que só mostra o
     caminho feliz não ajuda quem está depurando às 23h. -->

### `GET /saude` — pública

```bash
curl http://127.0.0.1:8000/saude
```

```json
{"status": "ok", "versao": "1.0.0", "ambiente": "desenvolvimento"}
```

### `GET /produtos` — autenticado

<!-- TODO: documentar os parâmetros -->

| Parâmetro | Tipo | Padrão | Observação |
|-----------|------|--------|------------|
| `pagina` | int ≥ 1 | 1 | |
| `por_pagina` | int 1–100 | 20 | 🔴 o teto é proteção contra DoS |
| `ordenar_por` | enum | `sku` | 🔴 lista branca — ver abaixo |
| `direcao` | `asc`\|`desc` | `asc` | |
| `categoria` | str | — | |
| `preco_min` / `preco_max` | float | — | |
| `busca` | str 2–60 | — | busca no nome |
| `somente_disponiveis` | bool | `false` | |

```bash
curl "http://127.0.0.1:8000/produtos?categoria=Notebooks&ordenar_por=preco&direcao=desc" \
  -H "Authorization: Bearer $TOKEN"
```

<!-- TODO: colar a resposta real -->

### `POST /produtos` — operador

<!-- TODO -->

### `PATCH /produtos/{sku}` — operador

<!-- TODO: mostrar que só os campos enviados mudam -->

### `DELETE /produtos/{sku}` — admin

<!-- TODO -->

### `POST /pedidos` — operador

<!-- TODO: incluir OBRIGATORIAMENTE o exemplo do pedido parcialmente
     inviável, mostrando o 409 e provando que o estoque não mudou -->

### `GET /relatorios/faturamento` — admin

<!-- TODO -->

---

## Erros

Todos os erros seguem o mesmo formato:

```json
{
  "codigo": "estoque_insuficiente",
  "mensagem": "PE-RED-K552: pedido 999, disponível 7"
}
```

| Status | Quando | Exemplo |
|--------|--------|---------|
| `400` | Requisição malformada | Corpo do `PATCH` vazio |
| `401` | **Não sei quem você é** | Sem token, token expirado ou forjado |
| `403` | **Sei quem você é, e você não pode** | Leitor tentando `DELETE` |
| `404` | Recurso não existe | SKU desconhecido |
| `409` | Conflito com o **estado** do servidor | SKU duplicado, estoque insuficiente |
| `422` | O **conteúdo** enviado é inválido | Preço negativo, campo obrigatório ausente |
| `500` | Erro nosso | Você não vai ver detalhe — reporte o `X-Request-ID` |

> 🎯 **`401` vs `403`.** O nome do 401 é infeliz: deveria ser
> *Unauthenticated*. O **401 pede que você se identifique**; o **403 diz
> que identificar-se não vai adiantar**.

> 🎯 **`409` vs `422`.** Nos dois casos o corpo estava bem formado — por
> isso nenhum é `400`. Use `409` quando o problema é o **estado** (já
> existe, acabou) e `422` quando é o **conteúdo** (preço abaixo do custo).

### Erro de validação

```json
{
  "codigo": "validacao_falhou",
  "mensagem": "Os dados enviados são inválidos",
  "campos": [
    {"campo": "preco", "erro": "Input should be greater than 0"},
    {"campo": "itens.0.quantidade", "erro": "Input should be greater than 0"}
  ]
}
```

O `campo` usa notação de caminho: `itens.0.quantidade` é a quantidade do
**primeiro** item. Isso permite ao front destacar exatamente o campo
errado no formulário.

---

## Cabeçalhos

### Enviados pela API

| Cabeçalho | Para quê |
|-----------|----------|
| `X-Request-ID` | Rastrear uma requisição no log |
| `X-Tempo-ms` | Tempo de processamento |
| `X-Content-Type-Options: nosniff` | Impede o navegador de adivinhar o tipo |
| `X-Frame-Options: DENY` | Impede embutir a resposta num iframe |

### Aceitos

| Cabeçalho | Efeito |
|-----------|--------|
| `Authorization: Bearer <token>` | Autenticação |
| `X-Request-ID` | Se você enviar, a API **preserva** o seu valor |

> 💡 Preservar o `X-Request-ID` do cliente permite seguir uma requisição
> atravessando vários serviços. Quando o app reclama de lentidão, ele
> manda o id e você acha a linha exata no log.

---

## Decisões de projeto

<!-- 🔴 Esta seção é a razão de este arquivo existir. Preencha-a. -->

### Exclusão: lógica ou física?

<!-- TODO: decidir e justificar.

     A pergunta real: um produto com pedidos históricos pode ser
     apagado? Se apagar, os pedidos antigos ficam órfãos e o relatório
     de faturamento do ano passado MUDA.

     Registre o que você escolheu e por quê. -->

### Quem pode ver quais pedidos?

<!-- TODO: 🔴 esta é a pergunta do OWASP nº 1 (BOLA).

     Hoje, qualquer usuário autenticado vê qualquer pedido trocando o
     número na URL. Isso é aceitável na Aurora?

     Provavelmente sim — mas precisa ser uma decisão CONSCIENTE e
     ESCRITA, não um esquecimento. Escreva-a aqui. -->

### Concorrência no estoque

<!-- TODO: a transação garante "tudo ou nada", não exclusividade.

     Dois pedidos simultâneos do último item podem ambos ler
     `estoque = 1` e ambos passar na validação.

     Qual defesa você escolheu?
       - SELECT ... FOR UPDATE  (bloqueio pessimista)
       - coluna de versão       (otimista)
       - CHECK estoque >= 0     (o banco decide)

     Justifique. -->

### Por que `delta` e não estoque absoluto?

<!-- TODO: você já sabe a resposta. Escreva-a. -->

---

## Ambiente de desenvolvimento

```bash
# subir
uvicorn "atlas.api.aplicacao:criar_app" --factory --reload

# subir aceitando conexões da rede local (para testar do celular)
uvicorn "atlas.api.aplicacao:criar_app" --factory --host 0.0.0.0 --port 8000
```

> ⚠️ `--reload` é **só para desenvolvimento**. Ele vigia o sistema de
> arquivos e reinicia o processo — em produção isso é desperdício e
> risco. O modo de produção é assunto do M09.

---

## Consumindo de outras linguagens

O `/openapi.json` permite **gerar** clientes automaticamente:

```bash
# TypeScript
npx openapi-typescript http://127.0.0.1:8000/openapi.json -o api.d.ts

# Python
pip install openapi-python-client
openapi-python-client generate --url http://127.0.0.1:8000/openapi.json
```

> 💡 Este é o retorno concreto de ter caprichado nos tipos: o time do
> app não escreve nem lê a sua documentação — ele **gera** o cliente e
> ganha autocomplete com os seus campos.
