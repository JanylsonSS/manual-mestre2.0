# CSV vs SQL — o que mudou de verdade

> **Entregável do Módulo 03.**
>
> Meça. Não escreva impressões — escreva números que você obteve rodando as
> duas implementações.

---

## Por que este documento existe

É fácil aceitar "banco de dados é melhor que CSV" como dogma. Este documento
existe para você **provar** — e para descobrir onde o CSV ainda ganha.

Engenharia é sobre trade-offs. Um profissional sabe defender a escolha **e**
enunciar o custo dela.

---

## 1. Esforço de implementação

Conte as linhas de código de cada implementação do **mesmo** relatório
(faturamento por cidade, com share e ticket médio).

| | Módulo 01 (CSV + Python) | Módulo 03 (SQLite + SQL) |
|---|--------------------------|--------------------------|
| Linhas de código da agregação | | |
| Arquivos envolvidos | | |
| Onde mora a regra "só conta pago" | | |
| Onde mora a regra de agrupamento | | |

**Comando para contar:** `wc -l arquivo` ou o contador do VS Code.

---

## 2. Desempenho

Meça com `time.perf_counter()`. Rode **cada** medição 5 vezes e reporte a
mediana — a primeira execução sempre é mais lenta (cache frio).

| Cenário | CSV (ms) | SQL (ms) | Vencedor |
|---------|----------|----------|----------|
| 30 pedidos | | | |
| 180 pedidos | | | |
| 5.000 pedidos (gere sinteticamente) | | | |
| 100.000 pedidos | | | |

**Onde a curva vira?**

<!-- TODO -->

**Surpresa esperada:** em volume pequeno o CSV pode ser **mais rápido**. Abrir
conexão, planejar a consulta e materializar o resultado tem custo fixo. Se foi
o que você mediu, **reporte com honestidade** — e explique por que ainda assim
o SQL é a escolha certa.

<!-- TODO -->

---

## 3. Memória

| | CSV | SQL |
|---|-----|-----|
| Pico de RAM com 100.000 pedidos | | |
| O que acontece com 10 milhões de linhas | | |

**Dica:** `import tracemalloc` ou meça o `sys.getsizeof` das estruturas
intermediárias.

**A diferença conceitual:** onde o processamento acontece em cada caso?

<!-- TODO -->

---

## 4. Robustez

| Situação | CSV (M01) | SQL (M03) |
|----------|-----------|-----------|
| Quantidade = `"dez"` | | |
| Preço negativo | | |
| Cliente duplicado com e-mail em maiúsculas | | |
| Pedido referenciando produto inexistente | | |
| Duas execuções simultâneas do relatório | | |
| Duas execuções simultâneas da **carga** | | |
| Processo morto no meio da gravação | | |

**Qual a diferença fundamental?** Em um caso a validação é *código que você
escreveu*; no outro é *garantia do sistema*. O que isso muda na prática?

<!-- TODO -->

---

## 5. Evolução

Estime o esforço para cada mudança nas duas arquiteturas:

| Mudança pedida | CSV | SQL |
|----------------|-----|-----|
| "Quero ver por canal também" | | |
| "Quero filtrar por período" | | |
| "Quero saber quem comprou notebook e nunca comprou mouse" | | |
| "Quero o histórico de preço de cada produto" | | |
| "Adicionem o campo `vendedor`" | | |
| "Preciso do top 10 por margem, não por receita" | | |

<!-- TODO -->

---

## 6. Onde o CSV ainda ganha

Seja honesto. Liste pelo menos três situações em que o arquivo é a escolha certa.

<!-- TODO
Pense em:
  - troca de dados entre sistemas
  - inspeção manual rápida
  - versionamento em Git
  - portabilidade
  - a curva de aprendizado da equipe
-->

---

## 7. Onde o SQLite vai doer

Você vai migrar para PostgreSQL no Módulo 05. Antecipe: quais limites do
SQLite você já sentiu ou vai sentir?

| Limitação | Impacto no Atlas | Como o Postgres resolve |
|-----------|------------------|-------------------------|
| Um escritor por vez | | |
| `ALTER TABLE` limitado | | |
| Afinidade de tipo permissiva | | |
| `GROUP BY` permissivo | | |
| Sem tipos nativos de data/decimal | | |
| Banco é um arquivo local | | |

---

## 8. A mudança de mentalidade

Escreva 2 ou 3 parágrafos, com suas palavras, sobre a diferença entre
programação **imperativa** (dizer COMO percorrer) e **declarativa** (dizer O QUE
você quer).

Use um exemplo concreto do seu código: o mesmo agrupamento por cidade, dos dois
jeitos.

<!-- TODO -->

---

## 9. Veredito

Se um colega perguntasse *"vale a pena migrar de CSV para banco?"*, o que você
responderia — e **a partir de que ponto**?

<!-- TODO: seja específico. "Depende" não é resposta; "acima de N registros,
     ou quando mais de uma pessoa precisar escrever, ou quando a integridade
     referencial importar" é. -->
