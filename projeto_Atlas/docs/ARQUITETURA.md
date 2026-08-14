# Arquitetura do Atlas

> O mapa do sistema, e — mais importante — **a regra que diz o que pode
> importar o quê**.

---

## Por que este documento existe

O Atlas já tem camadas. Ele nasceu com camadas no M04, ganhou
repositório no M05, API no M06 e pipeline no M10.

O problema é que essas camadas existem **só na sua cabeça**. Nada no
projeto impede que, numa sexta-feira apressada, alguém escreva um
`SELECT` dentro de uma rota. O código funciona. Os testes passam. E a
camada morreu sem ninguém perceber.

> 🔑 **Arquitetura que não é verificada não é arquitetura — é
> intenção.** Este módulo transforma a intenção em duas coisas
> concretas: um documento que diz a regra, e um script que reprova
> quem a quebrar.

---

## As camadas

Do mais externo (o mundo) para o mais interno (as regras do negócio):

```
    ┌─────────────────────────────────────────────────┐
    │  ENTRADA        cli.py · api/ · dados/          │  ← o mundo fala
    │                 scripts/                         │     com o Atlas
    ├─────────────────────────────────────────────────┤
    │  SERVIÇO        servicos.py · regras.py         │  ← o que o
    │                 metricas.py                      │     negócio faz
    ├─────────────────────────────────────────────────┤
    │  ACESSO         repositorio.py · orm/ · mongo/  │  ← onde o dado
    │                 leitura.py · relatorios_sql.py   │     mora
    ├─────────────────────────────────────────────────┤
    │  DOMÍNIO        modelos.py · excecoes.py        │  ← 🔑 não
    │                 validacao.py                     │     importa NADA
    ├─────────────────────────────────────────────────┤
    │  APOIO          config.py · formatacao.py       │  ← qualquer um
    │                 observabilidade.py               │     pode usar
    └─────────────────────────────────────────────────┘
```

### A regra

Ela tem **três** partes, e a terceira é a que quase todo mundo esquece:

> **1. Nenhuma camada importa uma camada de cima.**
>
> **2. DOMÍNIO e APOIO podem ser importados por qualquer um.**
> `modelos`, `excecoes`, `config` e `formatacao` não têm regra de
> negócio nem guardam estado. Uma rota usar `Pedido` é normal.
>
> **3. 🔑 ACESSO só pode ser importada por SERVIÇO** — ou pela
> própria ACESSO. Import dentro da mesma camada é sempre livre.

### Por que a terceira parte precisa existir

Porque as duas primeiras, sozinhas, **aprovam SQL dentro de uma rota**.

`api` é camada 0, `repositorio` é camada 2. Importar "para dentro" é
permitido — e assim `from atlas.repositorio import buscar_produto`
dentro de `rotas/produtos.py` passa por uma regra puramente linear
sem levantar suspeita.

Só que essa é exatamente a violação que dói:

> A rota chama o repositório direto e pula a regra de negócio. O
> código funciona. No dia em que a regra mudar, ela muda em
> `servicos.py` — e continua velha nas três rotas que aprenderam a se
> virar sozinhas.

> 💭 Vale reparar em como este furo apareceu: a regra linear parecia
> completa até alguém **plantar uma violação de propósito** e ver que
> o verificador aprovou. Nenhuma leitura do documento teria pego —
> foi o teste que pegou.
>
> É a mesma lição do portão de qualidade do M10, aplicada à
> arquitetura: **verifique que a verificação funciona.**

### Resumo executável

| De ↓ / Para → | ENTRADA | SERVIÇO | ACESSO | DOMÍNIO | APOIO |
|---|:---:|:---:|:---:|:---:|:---:|
| **ENTRADA** | ✅ | ✅ | 🔴 | ✅ | ✅ |
| **SERVIÇO** | 🔴 | ✅ | ✅ | ✅ | ✅ |
| **ACESSO** | 🔴 | 🔴 | ✅ | ✅ | ✅ |
| **DOMÍNIO** | 🔴 | 🔴 | 🔴 | ✅ | ✅ |
| **APOIO** | 🔴 | 🔴 | 🔴 | 🔴 | ✅ |

Repare na diagonal: **toda camada pode importar a si mesma.** Parece
óbvio e é a fonte do falso positivo mais comum — `relatorios_sql`
importando `repositorio` são dois módulos de ACESSO conversando, não
uma violação.

A linha de baixo é a mais restritiva de todas, e é de propósito:
**APOIO não importa nada do Atlas.** Se `config` começar a importar
`modelos`, ele deixou de ser apoio e virou domínio.

### O que cada seta proibida significa na prática

| Import proibido | Por que dói |
|---|---|
| `modelos.py` → `repositorio.py` | O domínio passa a depender do banco. Testar uma regra de negócio exige subir Postgres. |
| `repositorio.py` → `servicos.py` | Ciclo. Você não consegue mais entender nenhum dos dois sozinho. |
| `api/rotas/` → `repositorio.py` | 🔴 SQL na rota. O dia em que a regra mudar, ela vai mudar em **um** lugar e continuar velha em três. |
| `servicos.py` → `api/esquemas.py` | O negócio passa a depender do formato HTTP. A CLI e o pipeline herdam conceitos de rede que não usam. |

> 💭 Repare que nenhuma dessas quebra o programa. Todas **funcionam**.
> É exatamente por isso que precisam de um verificador: o
> interpretador não vai te avisar, o teste não vai falhar, e o
> problema só aparece seis meses depois, como "por que mexer aqui
> quebra lá?".

---

## Os dois lados do sistema

O Atlas tem duas entradas que quase não se falam, e isso é
proposital:

| | `api/` (M06–M07) | `dados/` (M10) |
|---|---|---|
| Ritmo | milissegundos | uma vez por noite |
| Volume | uma linha | milhões |
| Perfil | OLTP | OLAP |
| Otimiza | latência | vazão |

**As duas atravessam a camada de SERVIÇO.** Nenhuma das duas fala com
o repositório direto. É o que garante que "faturamento" signifique a
mesma coisa no painel e na API — e é a razão de a regra de camadas
valer também para o pipeline.

---

## Preencha: as fronteiras do seu projeto

_(preencha)_

Rode `python scripts/verificar_camadas.py --mapa` e cole aqui o mapa
de dependências que ele imprimir. Se ele acusar violação, você tem
duas opções honestas:

1. **Consertar o código** — mover a função para a camada certa.
2. **Mudar a regra** — se a violação for legítima, declare a exceção
   em `verificar_camadas.py`, **com um comentário dizendo por quê**.

> ⚠️ A opção 2 é legítima e perigosa. Uma exceção justificada é
> engenharia; um arquivo cheio de exceções sem justificativa é a
> arquitetura morrendo devagar, com aprovação do CI.

---

## Decisões

As decisões que produziram esta arquitetura estão em **`docs/adr/`** —
uma por arquivo, com data, alternativas consideradas e consequências.

Este documento diz **o que** o sistema é. Os ADRs dizem **por quê**.

---

*Atlas · Aurora Comércio · Módulo 11*
