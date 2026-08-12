# Roteiro de implementação — Módulo 04 (Python Avançado)

> **Pré-requisito:** M03 funcionando. Você vai comparar a saída do Atlas
> refatorado com a do Atlas atual — se a versão atual não estiver correta,
> não há referência para comparar.

---

## A dor

> *"O script virou um monstro de 800 linhas. Toda vez que preciso adicionar
> uma métrica nova, copio um bloco de 40 linhas e mudo três palavras. Já tem
> cinco cópias quase iguais. Ontem corrigi um bug em uma delas e esqueci das
> outras quatro. E quando roda de madrugada e falha, eu não faço ideia do
> que aconteceu."*

## A entrega

Atlas com modelos tipados, serviços orientados a objetos, apresentação por
composição, motor de regras extensível e logging estruturado.

---

## 🎯 A regra que governa este módulo

> **A saída dos relatórios deve ser IDÊNTICA à do Módulo 03.**

Refatoração que muda o comportamento não é refatoração — é reescrita com bug
novo. Por isso a Etapa 0 é criar a rede de segurança.

---

## Etapa 0 — Congelar o comportamento atual (30 min)

**Antes de tocar em uma linha de código**, capture a saída atual:

```bash
git switch -c feature/m04-refatoracao-oop

mkdir -p tests/referencia
python main.py relatorio --todos --formato json > tests/referencia/m03_relatorios.json
python main.py relatorio faturamento_por_cidade > tests/referencia/m03_cidade.txt
python main.py status > tests/referencia/m03_status.txt

git add tests/referencia/
git commit -m "test: congela a saída do M03 como referência de regressão"
```

**Pronto quando:** os arquivos de referência estão versionados. Eles são o
seu contrato: no fim do módulo, a nova versão precisa reproduzi-los.

---

## Etapa 1 — Modelos (90 min)

Complete `src/atlas/modelos.py`.

Ordem sugerida:

1. Os `Enum` (`Status`, `Canal`, `Segmento`) — 10 minutos, e todo o resto depende
2. `Produto` — `frozen=True`, `slots=True`, `__post_init__`, properties de margem
3. `Cliente`
4. `ItemVenda` — repare que `margem` usa `preco_unitario`, não `produto.preco`
5. `Pedido` — o mais rico; cuidado com `field(default_factory=list)`
6. `Metricas` — `frozen`, com `somar()` devolvendo nova instância
7. `Rejeicao`

**Teste enquanto escreve:**

```bash
python src/atlas/modelos.py
```

**Pronto quando:**

- `Produto` é hasheável (`{produto: 0}` funciona)
- `produto.preco = 99` levanta erro
- `Pedido(...).subtotal` bate com a conta feita na calculadora
- Duas instâncias de `Pedido` não compartilham a lista `itens`

⚠️ **A armadilha que você vai encontrar:** com `frozen=True`, normalizar
dentro do `__post_init__` exige `object.__setattr__(self, "campo", valor)`.
É feio de propósito.

---

## Etapa 2 — Serviços (90 min)

Complete `src/atlas/servicos.py`.

O coração é `Agregador.por(dimensao)`. Escreva-o primeiro e teste com
`"cidade"`, `"uf"`, `"canal"`, `"mes"` e `"status"` — **cinco relatórios
diferentes com o mesmo código**.

**O teste do desenho:** adicione uma property `trimestre` em `Pedido`.
`agregador.por("trimestre")` deve funcionar **sem tocar em `servicos.py`**.
Se você precisou alterar algo aqui, o desenho está errado.

⚠️ Valide a dimensão logo na entrada. `getattr(pedido, "cidde")` (com typo)
levanta `AttributeError` no meio do laço, com mensagem inútil. Falhe cedo,
listando as dimensões disponíveis.

**Pronto quando:** `totais()` bate com os números do M03.

---

## Etapa 3 — Apresentação (60 min)

Complete `src/atlas/apresentacao.py`.

Ordem: `DestinoMemoria` primeiro (é o mais simples e o que vai te ajudar a
testar os formatadores), depois os formatadores, depois os outros destinos.

**Pronto quando:** as 12 combinações (4 formatos × 3 destinos) funcionam:

```python
for F in [FormatadorTexto, FormatadorCSV, FormatadorJSON, FormatadorMarkdown]:
    for D in [DestinoConsole, DestinoArquivo, DestinoMemoria]:
        ServicoRelatorio(agregador, F(), D()).gerar()
```

⚠️ **Emoji em célula de tabela quebra o alinhamento.** `len("🔴")` é 1, o
terminal desenha 2 colunas. Use marcadores ASCII.

---

## Etapa 4 — Motor de regras (60 min)

Complete `src/atlas/regras.py`.

1. `DefinicaoRegra`, `AjusteAplicado`, `ResultadoPrecificacao`
2. O decorador `regra(...)`
3. `aplicar_regras(...)` com teto
4. As 7 regras de negócio

**Pronto quando:** você adiciona uma oitava regra e **nenhuma linha
existente muda**. Faça isso de verdade e confirme com `git diff`.

⚠️ **Convenção de sinal:** negativo é desconto, positivo é acréscimo.
Escreva isso em letras garrafais no topo do arquivo. Inverter o sinal por
engano é o bug mais caro que este arquivo pode produzir.

💭 A regra `frete_gratis` é um desafio de modelagem: ela não é percentual.
Escolha entre converter para percentual equivalente ou mudar o contrato da
regra — e **documente o porquê**.

---

## Etapa 5 — Observabilidade (60 min)

Complete `src/atlas/observabilidade.py`.

1. `FormatadorConsole` e `FormatadorJSON`
2. `configurar_logging()`
3. `ResultadoEtapa`, `Execucao`
4. `Monitor` com o context manager `etapa()`
5. `gravar_historico()` e `analisar_historico()`

**Depois, a limpeza:**

```bash
grep -rn "print(" src/atlas/ | grep -v apresentacao.py
```

Cada resultado é um `print` que deveria ser `log`. Zero resultados = pronto.

**Pronto quando:** você roda o Atlas, mata o processo no meio (`Ctrl+C`), e
consegue dizer pelo `saida/atlas.jsonl` exatamente onde ele parou.

---

## Etapa 6 — Integração (60 min)

Reescreva `src/atlas/cli.py` usando as peças novas:

```python
def main(argv=None) -> int:
    args = parsear(argv)
    logger = configurar_logging(nivel_console=DEBUG if args.verbose else INFO)
    monitor = Monitor(logger, comando=args.comando)

    try:
        with monitor.etapa("Carga"):
            pedidos = carregar(args.arquivo)

        with monitor.etapa("Agregação") as m:
            agregador = Agregador(pedidos)
            m["pedidos"] = len(pedidos)

        with monitor.etapa("Relatórios"):
            servico = ServicoRelatorio(
                agregador,
                criar_formatador(args.formato),
                DestinoMultiplo(DestinoConsole(), DestinoArquivo()),
            )
            servico.gerar()

        return 0
    except AtlasError as erro:
        logger.error("Falha: %s", erro)
        return 1
    finally:
        monitor.gravar_historico()
```

💭 **Repare:** `main` virou legível. Cada linha diz **o quê**, não **como**.
Se ela ficar difícil de ler de novo, algo vazou para o lugar errado.

---

## Etapa 7 — Empacotamento (30 min)

Complete `pyproject.toml`:

```bash
pip install -e ".[dev]"
atlas --help          # se você configurou [project.scripts]
mypy src/
ruff check src/
```

Depois **remova o `sys.path.insert`** do `main.py` — com o pacote instalado,
ele virou desnecessário.

---

## Etapa 8 — Concorrência, se compensar (45 min)

Escolha **um** ponto e **meça antes e depois**:

| Candidato | Tipo | Ferramenta |
|-----------|------|-----------|
| Ler N CSVs de uma pasta | I/O | `ThreadPoolExecutor` |
| Gerar N relatórios em formatos diferentes | I/O | `ThreadPoolExecutor` |
| Enriquecer clientes via API de CEP | I/O | `asyncio` |
| Agregar 1M+ registros em lotes | CPU | `ProcessPoolExecutor` |

> 🔴 **Se a medição não mostrar ganho, NÃO paralelize.**
>
> Escreva em `docs/REFATORACAO.md`: *"medi X e Y, o ganho foi de 1.05×, não
> compensa a complexidade"*. **Essa é uma entrega melhor** que adicionar
> concorrência inútil. Saber quando não usar a ferramenta é parte do
> aprendizado do módulo.

---

## Etapa 9 — Verificação de equivalência (45 min)

Escreva `scripts/comparar_m03_m04.py`:

```bash
python scripts/comparar_m03_m04.py
# ✅ faturamento_por_cidade  : idêntico
# ✅ faturamento_por_canal   : idêntico
# ✅ top_produtos            : idêntico
# ❌ curva_abc               : divergência em Sorocaba (80.1% vs 80.0%)
```

**Se houver divergência, os suspeitos habituais:**

| Sintoma | Causa provável |
|---------|----------------|
| Diferença de centavos | Ordem do arredondamento mudou |
| Uma cidade a mais/menos | Normalização diferente |
| Totais inflados | Property somando frete duas vezes |
| Ordem diferente | Faltou desempate no `sorted` |

⚠️ **Diferença de arredondamento é aceitável, mas precisa ser explicada.**
"Deu diferente e não sei por quê" não é resposta.

---

## Etapa 10 — Documentação (45 min)

Escreva `docs/REFATORACAO.md`:

| Seção | Conteúdo |
|-------|----------|
| Antes/depois | Linhas por arquivo, funções por módulo |
| Decisões de desenho | Por que dataclass e não Pydantic no domínio? Por que composição? |
| O que ficou melhor | Com exemplo concreto: "adicionar dimensão = 1 property" |
| O que ficou pior | Seja honesto — mais arquivos, mais indireção |
| Medições | Tempo, memória, e o resultado do teste de concorrência |
| O que eu faria diferente | Escreva **depois** de terminar |

---

## Checklist de entrega

**Comportamento**

- [ ] `scripts/comparar_m03_m04.py` reporta tudo idêntico
- [ ] Divergências (se houver) explicadas em `docs/REFATORACAO.md`

**Modelos**

- [ ] Todos com type hints completos
- [ ] `frozen=True` onde faz sentido, e sei justificar
- [ ] `field(default_factory=...)` em todas as coleções
- [ ] Validação em `__post_init__`
- [ ] Zero valor derivado guardado como atributo (tudo é property)

**Desenho**

- [ ] Nenhuma hierarquia de herança com mais de 2 níveis
- [ ] `ServicoRelatorio` recebe as dependências, não as constrói
- [ ] Adicionar uma dimensão de análise = 1 property, 0 alterações em serviços
- [ ] Adicionar uma regra de preço = 1 função, 0 alterações no motor

**Observabilidade**

- [ ] `grep -rn "print(" src/atlas/ | grep -v apresentacao` → vazio
- [ ] `logging.getLogger(__name__)` em todo módulo
- [ ] `saida/atlas.jsonl` responde "o que aconteceu às 3h?"
- [ ] `Execucao.resumo()` sai ao final de cada run

**Ferramentas**

- [ ] `pip install -e ".[dev]"` funciona
- [ ] `mypy src/` passa (nível 1 no mínimo)
- [ ] `ruff check src/` passa
- [ ] `sys.path.insert` removido do `main.py`

**Concorrência**

- [ ] Medi antes e depois
- [ ] Implementei **ou** documentei por que não compensou

---

## Desafios extras

| Desafio | Onde |
|---------|------|
| ⭐ `@lru_cache` nas agregações caras, com invalidação | `servicos.py` |
| ⭐ `__enter__`/`__exit__` no `Agregador` | `servicos.py` |
| ⭐ Pydantic Settings lendo do `.env` | novo `configuracao.py` |
| ⭐ `FormatadorHTML` com CSS embutido | `apresentacao.py` |
| ⭐⭐ Plugins: formatadores descobertos de uma pasta | `apresentacao.py` |
| ⭐⭐ `mypy --strict` passando em todo o pacote | `pyproject.toml` |
| ⭐⭐ Relatórios gerados concorrentemente | `cli.py` |

---

## Tempo total estimado

**10 a 12 horas.** É o módulo mais longo até aqui, porque refatorar exige
manter dois sistemas na cabeça ao mesmo tempo.

💡 **Faça em commits pequenos.** Um commit por etapa, rodando a comparação
de equivalência a cada um. Se algo quebrar, você sabe exatamente onde.

---

## ➡️ O que vem depois

No **Módulo 05**, o SQLite dá lugar ao PostgreSQL com SQLAlchemy e Alembic,
e o catálogo de produtos vai para o MongoDB.

Seus modelos do M04 vão virar modelos de ORM quase sem mudança — porque
você separou domínio de persistência. Se tivesse misturado, seria reescrita.
