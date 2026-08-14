# 0002 · Autenticar por token JWT, não por sessão

- **Estado:** _(preencha)_
- **Data:** _(preencha — a data em que você fez o M06)_
- **Decidido por:** _(preencha)_

---

## Contexto

> 🔧 Módulo 06.

Quem consome a API: o app do time interno, e depois o front do
cliente. _(preencha: quantos consumidores, e a partir de onde)_

_(preencha: por que o assunto "autenticação" surgiu agora e não no M04)_

---

## Decisão

_(preencha)_

---

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| Sessão em cookie, estado no servidor | _(preencha — 🔑 note que esta é a opção **mais simples e mais segura** para muitos casos. O que a descartou aqui? Se a resposta for "JWT é mais moderno", volte e pense de novo.)_ |
| Chave de API fixa por cliente | _(preencha)_ |
| OAuth2 com provedor externo | _(preencha — considere o tamanho do time)_ |

---

## Consequências

**Positivas**

- _(preencha)_

**Negativas / custos aceitos**

- 🔴 _(preencha a mais importante: um JWT emitido **não se revoga**.
  Demitiu alguém às 14h e o token dele vale até as 15h. O que o Atlas
  faz? Lista de revogação? Validade curta? Aceita o risco? Escreva
  qual, e o número que você escolheu para `ATLAS_TOKEN_EXPIRA_MINUTOS`
  é consequência direta desta linha.)_
- _(preencha)_

**O que passa a ser proibido**

- _(preencha — pense no que não pode entrar no payload de um token que
  o cliente consegue ler com base64)_

---

## Quando revisitar

_(preencha)_
