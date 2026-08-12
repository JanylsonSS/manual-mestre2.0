# Roteiro de implementação — Módulo 01

Ordem sugerida. Cada etapa deve **rodar** antes de você passar para a próxima. Nada de escrever tudo e testar no final.

---

## Etapa 0 — Ambiente (30 min)

1. Python 3.10+ instalado e no PATH
2. VS Code + extensões Python, Pylance, Jupyter
3. `python -m venv .venv` e ativado
4. Interpretador selecionado no VS Code
5. `python main.py` roda (mesmo que só imprima "não implementado")

**Pronto quando:** `python -c "import sys; print(sys.version)"` mostra 3.10+ com `(.venv)` no prompt.

---

## Etapa 1 — `config.py` (20 min)

Só constantes. É o arquivo mais fácil e o que dá o vocabulário do projeto.

- Caminhos base usando `pathlib.Path`
- Conjuntos de valores válidos (`STATUS_VALIDOS`, `CANAIS_VALIDOS`)
- Constantes de negócio (`STATUS_FATURAVEL`, cortes da curva ABC)
- Nomes das colunas esperadas

**Pronto quando:** `python -c "from src.atlas import config; print(config.DIR_DADOS_BRUTOS)"` funciona.

---

## Etapa 2 — `excecoes.py` (10 min)

Quatro classes vazias com docstring. Leva 5 minutos e paga dividendos no resto.

**Pronto quando:** você consegue `raise LinhaInvalidaError("teste")` e capturar com `except AtlasError`.

---

## Etapa 3 — `formatacao.py` (30 min)

Funções puras, sem dependência de nada. São as mais fáceis de testar mentalmente.

- `formatar_brl(1234.5)` → `"R$ 1.234,50"`
- `formatar_pct(0.1234)` → `"12,3%"`
- `formatar_int(1234567)` → `"1.234.567"`
- `truncar("texto longo", 8)` → `"texto l…"`
- `barra_ascii(0.6, 20)` → `"████████████░░░░░░░░"`

**Pronto quando:** você roda `python src/atlas/formatacao.py` e o bloco `__main__` imprime os casos de teste corretos.

⚠️ Atenção no `formatar_brl`: o padrão brasileiro é **ponto no milhar e vírgula no decimal** — o inverso do que a f-string faz por padrão. Dica: formate com `:,.2f` e depois troque os separadores usando um caractere temporário.

---

## Etapa 4 — `leitura.py` (30 min)

Só ler o arquivo e devolver linhas cruas. **Nada de validar aqui** — separação de responsabilidades.

- Verificar existência do arquivo antes de abrir
- `csv.DictReader` com `encoding="utf-8"` e `newline=""`
- Numerar as linhas a partir de 2 (linha 1 é o cabeçalho)
- Levantar `ArquivoInvalidoError` se faltar coluna obrigatória

**Pronto quando:** `ler_csv(Path("dados/brutos/vendas_jul2026.csv"))` devolve 20 tuplas `(numero, dict)`.

---

## Etapa 5 — `validacao.py` (60 min)

O coração da robustez. É a etapa mais longa — não tenha pressa.

Implemente na ordem:

1. `para_int`, `para_float` (conversores seguros que devolvem `None` em falha)
2. `normalizar_texto`
3. `validar_data`
4. `validar_linha` (usa todas as anteriores)
5. `validar_todas` (percorre e separa válidos de rejeitados)

**Pronto quando:** rodando contra `vendas_sujas.csv` você obtém alguns válidos e alguns rejeitados, cada rejeição com número da linha e motivo legível.

⚠️ `validar_linha` deve levantar `LinhaInvalidaError` com **mensagem específica** — "quantidade inválida: 'dez'" e não "erro".

---

## Etapa 6 — `metricas.py` (60 min)

Agora que os dados são confiáveis, calcule.

1. `valor_pedido` (a mais simples — comece por ela)
2. `filtrar_faturados`
3. `agrupar_por` (a função genérica; use `defaultdict`)
4. `calcular_totais`
5. `top_n`
6. `calcular_curva_abc`
7. `calcular_metricas` (junta tudo em um dict)

**Pronto quando:** com `vendas_jul2026.csv`, `calcular_totais` devolve faturamento total, nº de pedidos, ticket médio e taxa de cancelamento — e você conferiu ao menos um número na mão.

⚠️ Toda divisão precisa proteger o denominador zero. Se não houver pedidos pagos, o programa não pode quebrar.

---

## Etapa 7 — `relatorios.py` (60 min)

Renderização. Recebe o dict de métricas e devolve texto/estrutura.

1. `render_json` (mais fácil — só reorganizar o dict)
2. `render_csv_resumo`
3. `gravar_rejeitados`
4. `render_txt` (a mais trabalhosa: alinhamento de colunas)

**Pronto quando:** os três arquivos aparecem em `saida/` e o `.txt` está com as colunas alinhadas.

💡 Para alinhar, use a mini-linguagem de formatação: `f"{texto:<20}{valor:>15,.2f}"`.

---

## Etapa 8 — `cli.py` e `main.py` (30 min)

Orquestração. Este arquivo deve ser **legível como um resumo do programa**: ler → validar → calcular → renderizar → gravar.

- Ler o caminho de `sys.argv`
- Capturar `AtlasError` e mostrar mensagem amigável (sem traceback)
- Imprimir o resumo executivo no terminal

**Pronto quando:** os três comandos da seção "Como executar" do README funcionam.

---

## Etapa 9 — Polimento (30 min)

- Passe em todos os arquivos conferindo docstrings e type hints
- Nenhuma função com mais de ~25 linhas — quebre as que passarem
- Rode contra o CSV sujo e leia as mensagens de rejeição: elas estão úteis?
- Teste os casos de erro: arquivo inexistente, CSV vazio, CSV só com cabeçalho

---

## Desafios extras (opcionais)

| Desafio | Onde mexer |
|---------|-----------|
| ⭐ Flag `--formato txt\|json\|ambos` | `cli.py` |
| ⭐ Gráfico de barras ASCII no relatório | `formatacao.py` + `relatorios.py` |
| ⭐ Comparação com período anterior | novo módulo `comparacao.py` |
| ⭐ Detecção de anomalias (preço fora do padrão, cidade com UF divergente) | novo módulo `qualidade.py` |
| ⭐⭐ Consolidar múltiplos CSVs de uma pasta | `leitura.py` + `cli.py` |

---

## Tempo total estimado

**6 a 8 horas** de trabalho concentrado. Se levar mais, tudo bem — é o seu primeiro projeto. Se levar muito menos, provavelmente você pulou a robustez; teste com o CSV sujo.
