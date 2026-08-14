# 0003 · Quarentenar linha inválida em vez de abortar o lote

- **Estado:** _(preencha)_
- **Data:** _(preencha — Módulo 10)_
- **Decidido por:** _(preencha)_

---

## Contexto

> 🔧 Módulo 10. Talvez a decisão mais consequente do pipeline inteiro.

O pipeline lê milhões de linhas por noite, de três origens que o Atlas
não controla. Alguma proporção delas vem malformada — sempre.

A pergunta: **o que fazer com a linha ruim?**

Na API a resposta era fácil: devolve 400 e o cliente reenvia. No
pipeline não há ninguém para reenviar. _(preencha: por que essa
diferença muda tudo)_

---

## Decisão

_(preencha)_

---

## Alternativas consideradas

| Alternativa | Por que não |
|-------------|-------------|
| Abortar o lote inteiro | _(preencha — pense em 1 linha ruim em 2 milhões, e no que acontece com a equipe depois da terceira madrugada seguida sem relatório)_ |
| Descartar a linha em silêncio | _(preencha — 🔴 esta é a pior das três e a mais tentadora, porque nada dá errado visivelmente. Explique o dano.)_ |
| Corrigir automaticamente (imputar valor) | _(preencha — quando isso é legítimo e quando vira invenção de dado?)_ |

---

## Consequências

**Positivas**

- _(preencha)_

**Negativas / custos aceitos**

- _(preencha — alguém precisa OLHAR a quarentena. Quem? Com que
  frequência? Uma quarentena que ninguém abre é dado perdido com
  passos extras.)_
- _(preencha — ⚠️ LGPD: a quarentena guarda a linha original, e a
  linha original tem dado pessoal. O que o Atlas mascara?)_

**O que passa a ser proibido**

- _(preencha)_

---

## Quando revisitar

_(preencha — sugestão de formato: um limiar na taxa de rejeição)_
