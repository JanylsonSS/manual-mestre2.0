# Refatoração para orientação a objetos — Módulo 04

> **Entregável do Módulo 04.**
>
> Preencha com medições reais. "Ficou melhor" não é dado; "de 5 funções
> quase iguais para 1 método parametrizado" é.

---

## 1. A dor que originou este trabalho

> *"O script virou um monstro de 800 linhas. Copio um bloco de 40 linhas e
> mudo três palavras. Ontem corrigi um bug em uma cópia e esqueci das outras
> quatro."*

### O código duplicado que existia

Cole aqui **duas** das funções quase idênticas do M01/M03, lado a lado.

```python
# TODO
```

**O que variava entre elas:**

<!-- TODO -->

---

## 2. Antes e depois — números

| Métrica | M03 | M04 |
|---------|-----|-----|
| Arquivos em `src/atlas/` | | |
| Linhas totais | | |
| Maior função (linhas) | | |
| Maior arquivo (linhas) | | |
| Funções de agregação | | |
| `print` fora da apresentação | | |
| Funções com type hints | | |

**Comandos úteis:**

```bash
wc -l src/atlas/*.py
grep -c "^def \|^    def " src/atlas/*.py
grep -rn "print(" src/atlas/ | grep -v apresentacao.py | wc -l
```

⚠️ **Provavelmente o total de linhas AUMENTOU.** Isso é esperado e não é
fracasso: você trocou repetição por estrutura. O que importa é o tamanho da
**mudança necessária** para adicionar algo novo — meça isso na seção 4.

---

## 3. Decisões de desenho

### 3.1 Por que `dataclass` no domínio e Pydantic só na fronteira?

<!-- TODO: pense em custo de validação repetida, e em onde o dado
     não confiável realmente entra -->

### 3.2 Por que `frozen=True` em `Produto` e não em `Pedido`?

<!-- TODO -->

### 3.3 Por que composição em vez de herança na apresentação?

Conte as classes das duas abordagens:

| | Herança | Composição |
|---|---------|------------|
| Classes para 4 formatos × 3 destinos | | |
| Classes para adicionar 1 formato | | |
| Classes para adicionar 1 destino | | |

<!-- TODO -->

### 3.4 Por que `Protocol` em vez de `ABC` nos formatadores?

<!-- TODO -->

### 3.5 Por que o motor de regras usa decorador de registro?

<!-- TODO: o decorador não altera a função — ele a cataloga.
     Que problema isso resolve? -->

### 3.6 A regra de frete grátis

Ela não é percentual, e o motor devolve percentuais. Como você resolveu?

<!-- TODO: descreva a alternativa que você NÃO escolheu e por quê -->

---

## 4. 🎯 O teste real do desenho

Meça o **tamanho da mudança** para cada cenário. Faça de verdade e use
`git diff --stat`.

| Cenário | Arquivos tocados | Linhas alteradas |
|---------|:----------------:|:----------------:|
| Adicionar a dimensão "trimestre" | | |
| Adicionar o formato HTML | | |
| Adicionar o destino "e-mail" | | |
| Adicionar uma regra de preço | | |
| Mudar a definição de "faturado" | | |
| Trocar o separador do CSV | | |

**Compare com o M03:** quantos arquivos você teria tocado lá para cada um?

<!-- TODO -->

---

## 5. Equivalência de comportamento

Saída de `scripts/comparar_m03_m04.py`:

```
TODO: cole aqui
```

### Divergências encontradas

| Relatório | Diferença | Causa | Aceitável? |
|-----------|-----------|-------|------------|
| | | | |

<!-- TODO. "Não sei por quê" não é uma causa. -->

---

## 6. Medições

### 6.1 Desempenho

| Operação | M03 | M04 | Δ |
|----------|-----|-----|---|
| Carga de 100k linhas | | | |
| Agregação por cidade | | | |
| Geração dos 8 relatórios | | | |
| Memória de pico | | | |

⚠️ Rode 5 vezes e use a **mediana** — a primeira execução sempre é mais lenta.

<!-- Se ficou mais lento, investigue: property recalculada em laço?
     Metricas frozen criando objeto demais? Documente. -->

### 6.2 Concorrência

**Ponto escolhido:**

<!-- TODO -->

**Por que este e não os outros:**

<!-- TODO -->

| | Sequencial | Concorrente | Ganho |
|---|-----------|-------------|-------|
| Tempo | | | |

**Decisão final:**

<!-- TODO: implementei / NÃO implementei porque o ganho foi de X.
     A segunda resposta é perfeitamente válida. -->

---

## 7. O que ficou pior

Seja honesto. Toda refatoração tem custo.

<!--
TODO. Pense em:
  • mais arquivos para navegar
  • indireção: entender o fluxo exige abrir 3 arquivos
  • curva de aprendizado de quem chegar depois
  • overhead de criar objetos
  • Protocol e ABC exigem conhecimento que uma função não exige
-->

---

## 8. Onde eu resisti à tentação

Liste lugares onde você **quase** aplicou uma técnica do módulo e decidiu
não aplicar.

<!--
TODO. Exemplos:
  • "quase criei uma classe Validador, mas era uma função"
  • "quase usei herança para os formatadores, mas a composição venceu"
  • "quase paralelizei a leitura, mas medi e não compensou"
  • "quase usei metaclasse, mas o decorador resolveu"

💭 Esta seção é a mais importante do documento. Aplicar a técnica é fácil;
   saber não aplicar é o que separa engenharia de exibicionismo.
-->

---

## 9. Preparando o Módulo 05

No M05 este código migra para PostgreSQL com SQLAlchemy. Anote sua aposta:

| Camada | Vai mudar muito? | Por quê |
|--------|:----------------:|---------|
| `modelos.py` | | |
| `servicos.py` | | |
| `apresentacao.py` | | |
| `repositorio.py` | | |
| `regras.py` | | |

<!-- 💭 Se a resposta for "só o repositório", o desenho está certo:
     você separou domínio de persistência.
     Se `servicos.py` também mudar muito, houve vazamento de
     responsabilidade — e é bom descobrir isso agora. -->

---

## 10. O que eu faria diferente

<!-- TODO: escreva DEPOIS de terminar, não antes. -->
