# Roteiro — Módulo 06 · A Atlas API

> **Objetivo:** transformar o Atlas de um programa que roda no seu terminal
> numa **API HTTP** que o time do app, o setor de compras e a diretoria
> consomem — cada um vendo só o que lhe cabe.

---

## A situação

O Atlas hoje funciona. Ele lê CSV, valida, grava em PostgreSQL, tem
camadas, tipos e testes. E tem exatamente **um** usuário: você, no terminal.

Na reunião de segunda, três pessoas pediram a mesma coisa de três jeitos:

| Quem | O que disse |
|------|-------------|
| **Time do app** | *"Preciso listar produtos com filtro. Hoje você me manda um CSV por e-mail e ele já nasce desatualizado."* |
| **Compras** | *"Quero registrar entrada de estoque sem pedir para você abrir o banco."* |
| **Diretoria** | *"Quero ver margem. Mas isso não pode aparecer para ninguém mais."* |

E você acrescentou uma quarta, silenciosa:

> *"Quero dormir sabendo que ninguém apaga a base sem querer."*

---

## Ordem de trabalho

Faça **nesta ordem**. Cada etapa depende da anterior.

```
1. Ambiente e configuração    ← sem isso, nada sobe
2. Esqueleto que responde     ← /saude no ar
3. Esquemas                   ← o contrato antes do código
4. Sessão e camadas           ← a API conversa com o M05
5. CRUD de produtos           ← o primeiro recurso completo
6. Segurança                  ← fechar a porta que você abriu
7. Pedidos                    ← 🔴 a parte que custa dinheiro
8. Relatórios e documentação  ← fechar o círculo
```

---

## Etapa 1 — Ambiente e configuração

### O que fazer

1. Instale as dependências novas:

   ```bash
   pip install "fastapi[standard]" pydantic-settings pyjwt bcrypt python-multipart
   ```

2. Acrescente todas ao `pyproject.toml`, em `dependencies`.

3. Copie `.env.example` para `.env` e **gere uma chave de verdade**:

   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```

4. Confirme que `.env` está no `.gitignore`:

   ```bash
   git check-ignore -v .env
   ```

   Se esse comando não imprimir nada, **pare e conserte**. É o erro mais
   caro deste módulo.

5. Implemente `src/atlas/api/config.py`.

### Pronto quando

- [ ] `python -m atlas.api.config` imprime a configuração **sem** mostrar a chave inteira
- [ ] Com `ATLAS_SECRET_KEY` vazia, a classe **levanta erro** em vez de aceitar
- [ ] `git status` não mostra o `.env`

> 🔴 A validação `Field(min_length=32)` não é decoração. Sem ela, uma
> chave vazia deixa o app subir e assinar tokens que qualquer um forja.
> **Falhar ao subir é melhor do que funcionar errado.**

---

## Etapa 2 — Esqueleto que responde

### O que fazer

1. Implemente `criar_app()` em `aplicacao.py` com apenas `GET /saude`.
2. Suba:

   ```bash
   uvicorn "atlas.api.aplicacao:criar_app" --factory --reload
   ```

3. Abra `http://127.0.0.1:8000/docs`.

### Pronto quando

- [ ] `curl http://127.0.0.1:8000/saude` devolve `200`
- [ ] O `/docs` abre e mostra a rota
- [ ] `--reload` recarrega quando você salva um arquivo

> 💡 Pare aqui e olhe o `/docs`. Ele foi gerado a partir dos seus tipos.
> Cada campo que você declarar daqui em diante aparece nele
> automaticamente — é a razão de o esforço em `esquemas.py` valer a pena.

---

## Etapa 3 — Esquemas

### O que fazer

Implemente `esquemas.py` **antes** de qualquer rota. O contrato primeiro.

Para produtos, você precisa dos quatro:

| Esquema | Papel |
|---------|-------|
| `ProdutoBase` | campos comuns |
| `ProdutoCriar` | entrada do `POST` |
| `ProdutoAtualizar` | entrada do `PATCH` — **tudo opcional** |
| `ProdutoResposta` | saída — **sem `custo`** |

### Pronto quando

- [ ] `ProdutoCriar` recusa `preco: -100` com mensagem em `loc: ["body","preco"]`
- [ ] `ProdutoCriar(sku="  nb-dell-15  ")` produz `"NB-DELL-15"`
- [ ] `ProdutoResposta` **não tem** `custo`
- [ ] Um corpo com quatro erros devolve **os quatro de uma vez**

> ⚠️ **A armadilha número um do Pydantic.** As restrições do `Field()`
> (`pattern`, `min_length`, `gt`) rodam **entre** o `mode="before"` e o
> `mode="after"`:
>
> ```
> bruto → [before] → tipo + Field() → [after] → pronto
> ```
>
> Se o validador **conserta** o dado, ele tem que rodar `before` — senão
> a restrição rejeita o dado sujo e o conserto nunca acontece.

---

## Etapa 4 — Sessão e camadas

### O que fazer

1. Implemente `obter_sessao()` em `dependencias.py`, com `yield` e
   `try/finally`.
2. Verifique que `atlas/servicos.py` **não importa `fastapi`**:

   ```bash
   grep -rn "fastapi" src/atlas/servicos.py src/atlas/repositorio.py
   ```

   Não deve retornar nada.

### Pronto quando

- [ ] `obter_sessao` tem `finally: sessao.close()`
- [ ] Nenhum arquivo fora de `atlas/api/` importa `fastapi`
- [ ] O repositório **nunca** chama `commit`

### 🔴 Prove que você entendeu

Escreva uma versão **sem** o `close()`, configure o engine com
`pool_size=2, max_overflow=0` e faça 20 requisições. Você deve ver:

```
QueuePool limit of size 2 overflow 0 reached, connection timed out
```

Guarde essa mensagem na memória. Em produção ela aparece **de
madrugada**, sob carga, longe da causa.

---

## Etapa 5 — CRUD de produtos

### O que fazer

Implemente as cinco rotas em `rotas/produtos.py`.

### Pronto quando

- [ ] `POST` devolve `201`
- [ ] `POST` com SKU repetido devolve `409`
- [ ] `GET /produtos` pagina e filtra
- [ ] `PATCH {"preco": 100}` altera **só** o preço
- [ ] `DELETE` devolve `204` com corpo vazio
- [ ] SKU inexistente devolve `404` em todas

### 🔴 O teste que importa

```bash
# crie um produto, depois:
curl -X PATCH .../produtos/NB-DELL-15 -d '{"preco": 2399}' | jq .nome
```

Se o nome voltou `null`, você esqueceu o `exclude_unset=True`.

---

## Etapa 6 — Segurança

### O que fazer

1. `seguranca.py`: hash com bcrypt, emissão e leitura de JWT.
2. `dependencias.py`: `usuario_atual` e `exigir_papel`.
3. `rotas/autenticacao.py`: `POST /auth/token` e `GET /auth/eu`.
4. Aplique os papéis nas rotas de produto.

### Pronto quando

- [ ] Senha gravada é hash — a mesma senha gera hashes **diferentes**
- [ ] Sem token: `401`. Token inválido: `401`. Token expirado: `401`
- [ ] Leitor tentando `DELETE`: `403`
- [ ] O `401` traz `WWW-Authenticate: Bearer`
- [ ] O botão **Authorize** funciona no `/docs`

### 🔴 As duas provas de segurança

**Prova 1 — mensagens idênticas.**

```python
a = cliente.post("/auth/token", data={"username": "ninguem@x.com", "password": "a"})
b = cliente.post("/auth/token", data={"username": "ana@aurora.com.br", "password": "errada"})
assert a.status_code == b.status_code and a.json() == b.json()
```

Se diferirem, você entregou ao atacante a lista de quem tem conta.

**Prova 2 — o JWT não esconde nada.**

Pegue um token, divida por `.` e decodifique a carga em base64 **sem
chave nenhuma**. Você vai ler tudo. Confirme então que não há nada
sensível ali — só `sub`, `papel` e datas.

---

## Etapa 7 — 🔴 Pedidos

Esta é a etapa que separa um exercício de um sistema.

### O que fazer

Implemente `POST /pedidos` em `servicos.py`, com atomicidade real.

### O teste de aceitação

```python
antes = get("/produtos/AR-KING-1TB").json()["estoque"]   # 47

post("/pedidos", json={
    "cliente_email": "teste@aurora.com.br", "canal": "site",
    "itens": [{"sku": "AR-KING-1TB", "quantidade": 1},     # cabe
              {"sku": "MO-SAM-27C",  "quantidade": 999}]})  # não cabe
# → 409

depois = get("/produtos/AR-KING-1TB").json()["estoque"]
assert depois == antes        # 🔴 47, não 46
```

### Pronto quando

- [ ] O teste acima passa
- [ ] Um pedido com dois problemas devolve **os dois** de uma vez
- [ ] `GET /pedidos` usa `selectinload` (meça com `echo=True`)

> 🔴 **Por que este é o erro mais perigoso do módulo.** Se o estoque
> baixar e você não desfizer, nada falha: não há exceção, não há log,
> não há alerta. O cliente vê um erro e vai embora. O estoque fica
> errado. A descoberta acontece no inventário do fim do mês — quando já
> não dá para saber qual pedido causou.

---

## Etapa 8 — Relatórios e documentação

### O que fazer

1. `GET /relatorios/faturamento`, exigindo `admin`.
2. Escreva `docs/API.md` com um `curl` por rota.
3. Rode a auditoria da lista de exercícios contra a sua API.

### 🎯 O fechamento do círculo

O faturamento por categoria você já calculou **três vezes**:

| Módulo | Onde |
|--------|------|
| M01 | `atlas/metricas.py` — Python puro sobre CSV |
| M03 | `dados/consultas/faturamento_por_categoria.sql` |
| M05 | `atlas/relatorios_sql.py` — SQLAlchemy |

Agora, a quarta: JSON via HTTP.

**Os quatro devem dar o mesmo número.** Compare-os. Se divergirem, um
tem bug — e achar qual é o exercício mais valioso deste módulo, porque
é exatamente o que acontece quando a diretoria compara o seu relatório
com a planilha do financeiro.

### Pronto quando

- [ ] Os quatro cálculos batem
- [ ] `docs/API.md` tem um exemplo executável por rota
- [ ] A auditoria do `openapi.json` passa

---

## ✅ Checklist final do módulo

### Contrato

- [ ] Toda rota tem `response_model`
- [ ] Nenhum esquema de resposta expõe `custo` (exceto `ProdutoInterno`, que exige admin)
- [ ] Erros de todas as rotas têm o mesmo formato
- [ ] `responses={}` documenta os erros previstos

### Arquitetura

- [ ] `atlas/servicos.py` **não importa `fastapi`**
- [ ] O repositório **não chama `commit`**
- [ ] Nenhuma função de rota passa de 5 linhas
- [ ] `obter_sessao` tem `try/finally`

### Segurança

- [ ] `.env` ignorado, `.env.exemplo` versionado
- [ ] Nenhuma senha em texto no banco
- [ ] Erro de login idêntico para usuário e senha errados
- [ ] `401` ≠ `403`, e cada um no lugar certo
- [ ] Lista branca em `ordenar_por` e `agrupar_por`
- [ ] Nenhum traceback numa resposta

### Correção

- [ ] 🔴 Pedido inviável não altera estoque nenhum
- [ ] `PATCH` parcial não apaga campos
- [ ] `GET /pedidos` não sofre N+1

---

## Erros que você provavelmente vai cometer

Não é pessimismo — é a lista dos que todo mundo comete.

| Sintoma | Causa |
|---------|-------|
| `GET /produtos/destaques` devolve 404 | Rota dinâmica declarada antes da estática |
| `PATCH` apaga campos | Faltou `exclude_unset=True` |
| `custo` aparece na resposta | Rota sem `response_model` |
| `no such table` só nos testes | SQLite em memória sem `poolclass=StaticPool` |
| `QueuePool limit reached` após horas | `get_sessao` sem `finally: close()` |
| Front vê "CORS policy" num erro 500 | CORS não é o middleware mais externo |
| Validador de `sku` "não roda" | Faltou `mode="before"` |
| Estoque some sem explicação | Falta `rollback` no caminho de erro |
| Listagem lenta com 50 pedidos | N+1 — faltou `selectinload` |

---

## Se você quiser ir além

Nada aqui é requisito do M06 — são as portas para o M07.

1. **Refresh token** — acesso de 15 min + refresh de 7 dias
2. **Idempotência** — `Idempotency-Key` no `POST /pedidos`, para que um
   duplo clique não gere dois pedidos
3. **Limitação de taxa** — 60 req/min por token, com `429` e `Retry-After`
4. **Versionamento** — `/v1/produtos`, para poder quebrar o contrato depois
5. **Paginação por cursor** — `offset` grande fica lento; cursor não
6. **Escopos** em vez de papéis — quando a hierarquia deixar de ser linear
7. **Exclusão lógica** — `ativo=False` em vez de `DELETE`

---

> 📖 **Antes de expor qualquer API à internet**, leia o
> [OWASP API Security Top 10](https://owasp.org/API-Security/). O item
> nº 1 — *Broken Object Level Authorization* — está comentado dentro de
> `rotas/pedidos.py`, e é o que você mais provavelmente deixou passar.
