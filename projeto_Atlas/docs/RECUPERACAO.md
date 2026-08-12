# Manual de recuperação — Atlas

> **Este documento é um entregável do Módulo 02.**
>
> Não copie respostas prontas. Execute cada cenário de verdade no seu repositório,
> cole os comandos que você usou e a saída que observou. O objetivo é que daqui a
> seis meses, sob pressão, você consulte este arquivo e resolva em 30 segundos.

---

## Como usar sob pressão

**Antes de qualquer comando, responda:** *onde está a coisa que quero desfazer?*

| Onde está | Ferramenta |
|-----------|-----------|
| Edição no arquivo, não commitada | `git restore` |
| Arquivo no stage | `git restore --staged` |
| Último commit, **não** enviado | `git commit --amend` ou `git reset` |
| Commit **já enviado** | `git revert` |
| Trabalho pela metade, preciso trocar de contexto | `git stash` |
| "Sumiu tudo" | `git reflog` |

**Protocolo de emergência:**

1. Respire. Não rode mais comandos no impulso.
2. `git status` — onde estou?
3. `git reflog` — onde eu estava?
4. Só então aja.

---

## Cenário 1 — Descartar uma edição não commitada

**Situação:** editei `src/atlas/metricas.py`, não gostou, quero voltar ao último commit.

**Comandos executados:**

```bash
# TODO: cole aqui os comandos que você usou
```

**Saída observada:**

```
# TODO: cole a saída
```

**O que aprendi:**

<!-- TODO: uma ou duas frases. Ex.: por que git restore é irreversível? -->

---

## Cenário 2 — Tirar um arquivo do stage

**Situação:** dei `git add .` e um arquivo entrou sem querer.

**Comandos executados:**

```bash
# TODO
```

**Diferença entre `git restore --staged arq` e `git restore --staged --worktree arq`:**

<!-- TODO: explique com suas palavras -->

---

## Cenário 3 — Corrigir a mensagem do último commit

**Situação:** commitei com a mensagem `"asdf"`. Ainda não dei push.

**Comandos executados:**

```bash
# TODO
```

**Hash antes:** `_______`
**Hash depois:** `_______`

**Por que o hash mudou?**

<!-- TODO -->

**Em que situação eu NÃO poderia ter usado `--amend`?**

<!-- TODO -->

---

## Cenário 4 — Juntar vários commits antes do Pull Request

**Situação:** meu branch tem 6 commits com mensagens `wip`, `wip2`, `agora vai`.

**Comandos executados:**

```bash
# TODO
```

**Como confirmei que nenhuma linha de código se perdeu:**

<!-- TODO: que comando você usou para comparar? -->

---

## Cenário 5 — Desfazer um commit já enviado

**Situação:** o commit `abc1234` quebrou o cálculo de faturamento em produção. Já foi para o GitHub e o time já puxou.

**Comandos executados:**

```bash
# TODO
```

**Quantos commits o histórico tinha antes e depois? Por quê?**

<!-- TODO -->

**Por que `git reset` seria a escolha errada aqui?**

<!-- TODO -->

---

## Cenário 6 — Hotfix urgente no meio de uma feature

**Situação:** estou no meio da refatoração de `validacao.py`, com código que nem compila, e chega um bug crítico.

**Comandos executados:**

```bash
# TODO: stash → switch → corrigir → merge → voltar → pop
```

**O que acontece se eu tiver dois stashes e quiser aplicar o primeiro?**

<!-- TODO -->

**Por que `git stash` não substitui um commit num branch de rascunho?**

<!-- TODO -->

---

## Cenário 7 — Recuperar commits apagados por `reset --hard`

**Situação:** rodei `git reset --hard HEAD~3` e perdi o trabalho da tarde.

**Comandos executados:**

```bash
# TODO
```

**Saída do `git reflog` (as linhas relevantes):**

```
# TODO
```

**O que o reflog NÃO recupera:**

<!-- TODO: liste pelo menos 3 coisas -->

**Conclusão prática que tiro disso:**

<!-- TODO: dica — tem a ver com a frequência dos seus commits -->

---

## Cenário 8 — Segredo commitado

**Situação:** commitei o `.env` com a senha do banco.

### Caso A — o commit ainda NÃO foi enviado

**Comandos executados:**

```bash
# TODO
```

### Caso B — o commit JÁ foi enviado ao GitHub

**Qual é o PRIMEIRO passo, antes de qualquer comando Git?**

<!-- TODO: esta é a pergunta mais importante do documento -->

**Por que remover o arquivo em um commit novo não resolve?**

<!-- TODO -->

**Que ferramentas existem para reescrever o histórico?**

<!-- TODO: cite pelo menos duas -->

---

## Cenário 9 — Trabalhei no branch errado

**Situação:** fiz 3 commits direto em `main`; deveriam estar em `feature/relatorio`.

**Comandos executados:**

```bash
# TODO
```

**Estado final de cada branch (`git log --oneline --graph --all`):**

```
# TODO
```

---

## Cenário 10 — Merge deu errado no meio

**Situação:** comecei um merge, apareceram conflitos em 5 arquivos e percebi que era o branch errado.

**Comando de escape:**

```bash
# TODO
```

**Quais outras operações têm um `--abort` equivalente?**

<!-- TODO: liste pelo menos 3 -->

---

## Tabela de decisão pessoal

Preencha com as suas palavras. É esta tabela que você vai consultar de verdade.

| Situação | Comando | Por quê |
|----------|---------|---------|
| Editei e me arrependi | | |
| Dei `add` sem querer | | |
| Errei a mensagem do commit (local) | | |
| Commit já enviado quebrou algo | | |
| Preciso trocar de branch com trabalho pela metade | | |
| Apaguei commits sem querer | | |
| Commitei arquivo que não devia | | |
| Merge conflitou e quero cancelar | | |

---

## Aliases que configurei

```bash
# TODO: liste os aliases que você criou e para que serve cada um
```

---

## O que ainda me dá insegurança

<!--
TODO: seja honesto. Anotar o que você ainda não domina é mais útil
que fingir que domina tudo. Volte aqui depois do Módulo 12.
-->
