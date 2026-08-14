# Changelog

Todas as mudanças relevantes do Atlas.

Formato: [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
Versionamento: [SemVer](https://semver.org/lang/pt-BR/)

---

## Para que serve, na prática

Um changelog não é `git log`. O `git log` diz **o que mudou no
código**; o changelog diz **o que mudou para quem usa**.

Por isso ele é escrito para humanos, agrupado por tipo, e omite as
duzentas linhas de refatoração que ninguém de fora percebe.

> 🔑 O teste: alguém que usa a API do Atlas consegue decidir, lendo só
> esta página, se precisa mexer em algo antes de atualizar? Se não
> consegue, o changelog não está fazendo o trabalho dele.

### SemVer em uma tabela

| Mudança | Versão | Exemplo no Atlas |
|---------|--------|------------------|
| Quebra compatibilidade | **MAIOR** (2.0.0) | remover um campo da resposta de `/produtos` |
| Funcionalidade compatível | **MENOR** (1.1.0) | novo endpoint `/relatorios/margem` |
| Correção compatível | **CORREÇÃO** (1.0.1) | consertar arredondamento do frete |

> ⚠️ **A parte que quase todo mundo erra:** acrescentar um campo
> **obrigatório** num corpo de requisição é mudança MAIOR, não menor.
> Todo cliente que não manda o campo passa a receber 422.
>
> Campo **opcional** com padrão é menor. A diferença é exatamente
> "código de terceiros que funcionava para de funcionar" — e é essa a
> definição de quebra, não o tamanho do diff.

### Categorias

`Adicionado` · `Alterado` · `Descontinuado` · `Removido` · `Corrigido` · `Segurança`

---

## [Não publicado]

_(o que está na `main` e ainda não saiu numa versão)_

### Adicionado
- _(preencha)_

### Corrigido
- _(preencha)_

---

## [1.0.0] — AAAA-MM-DD

_(preencha a data em que você fechar o M13)_

> 🏁 **Atlas 1.0.** A primeira versão que a Aurora pode operar sem
> você por perto.

### O que 1.0 significa aqui

Não é "está pronto" — software não fica pronto. É um compromisso
específico:

- A API v1 é **estável**: o que está documentado em `docs/API.md` não
  muda sem incremento de versão MAIOR.
- Existe caminho de volta: rollback em um comando (M09).
- Existe caminho de diagnóstico: `docs/RUNBOOK.md` e
  `docs/PIPELINE.md`.
- As decisões estão registradas: `docs/adr/`.

### Adicionado

_(preencha — a lista abaixo é o histórico dos módulos, use como base
e escreva do ponto de vista de quem USA o sistema)_

- CLI de relatórios sobre CSV, com arquivo de rejeições (M01)
- Persistência relacional com schema modelado e migração idempotente (M03)
- Persistência poliglota: PostgreSQL + MongoDB (M05) — veja ADR 0001
- API HTTP autenticada, com autorização por papel (M06) — veja ADR 0002
- Integrações resilientes com transportadora e gateway (M07)
- Recebimento de webhooks com validação de assinatura (M07)
- Empacotamento em containers (M08)
- Pipeline de dados diário com lago em camadas (M10) — veja ADR 0004
- _(preencha o resto)_

### Segurança

- _(preencha — autenticação, autorização por papel, validação na
  fronteira, segredos fora do versionamento, upload com verificação
  de assinatura de arquivo)_

---

## Histórico de desenvolvimento

As versões abaixo são os marcos dos módulos do manual. Elas não foram
publicadas para ninguém — servem para você ver a evolução, e para
praticar o hábito de registrar antes que ele valha dinheiro.

| Versão | Módulo | Entrega |
|--------|--------|---------|
| 0.1.0 | M01 | CLI de relatórios sobre CSV |
| 0.2.0 | M02 | Versionamento e automações |
| 0.3.0 | M03 | Banco relacional |
| 0.4.0 | M04 | Orientação a objetos e logging |
| 0.5.0 | M05 | PostgreSQL + MongoDB |
| 0.6.0 | M06 | API v1 |
| 0.7.0 | M07 | Integrações e testes |
| 0.8.0 | M08 | Containers |
| 0.9.0 | M09 | Deploy e CI/CD |
| 0.10.0 | M10 | Pipeline de dados |
| 0.11.0 | M11 | Arquitetura e ADRs |
| 0.12.0 | M12 | Suíte de testes |
| **1.0.0** | **M13** | **Atlas 1.0** |

> 💭 Repare que `0.10.0` vem **depois** de `0.9.0`. Em SemVer os
> números não são decimais: `0.10.0 > 0.9.0`. Ordenar versão como
> texto é um clássico — e faz o seu script de deploy escolher a
> versão errada.

---

## Como manter isto vivo

O changelog morre do mesmo jeito que os ADRs: por ser escrito
"depois".

```bash
# ✅ na mesma mudança
git add CHANGELOG.md src/atlas/...
git commit -m "feat(relatorios): adiciona margem por canal"
```

> 💡 Se escrever a entrada do changelog é difícil, geralmente é sinal
> de que a mudança faz duas coisas ao mesmo tempo. Considere separar —
> o changelog está te dando uma informação sobre o commit, não só
> pedindo burocracia.

---

*Atlas · Aurora Comércio*
