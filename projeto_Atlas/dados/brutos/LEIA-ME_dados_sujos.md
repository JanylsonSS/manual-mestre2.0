# Problemas propositais em `vendas_sujas.csv`

Este arquivo existe para testar a robustez do seu validador. **Cada linha tem um defeito específico.**

Não olhe esta lista antes de tentar. Rode seu programa contra o arquivo, veja o que ele pega, e só depois confira aqui o que passou despercebido.

<details>
<summary>👉 Clique para revelar a lista de defeitos</summary>

| Linha | ID | Defeito | Como tratar |
|-------|-----|---------|-------------|
| 2 | 2001 | Espaços múltiplos no cliente, cidade minúscula, status `PAGO` em maiúsculas | **Aceitar** após normalizar (`.title()`, `.lower()`) |
| 3 | 2002 | `quantidade` = `"dez"` (texto, não número) | Rejeitar |
| 4 | 2003 | `preco_unitario` vazio | Rejeitar |
| 5 | 2004 | `cliente` vazio **e** `quantidade` negativa | Rejeitar (mensagem deve citar o primeiro problema encontrado) |
| 6 | 2005 | `status` = `"entregue"` (fora do domínio) | Rejeitar |
| 7 | 2006 | `canal` vazio | Rejeitar |
| 8 | 2007 | `uf` = `"PARANA"` (não são 2 letras) | Rejeitar |
| 9 | `abc` | `id` não numérico | Rejeitar |
| 10 | 2009 | `data` no formato `DD/MM/AAAA` | Rejeitar (ou converter, se você implementou tolerância — documente a escolha) |
| 11 | 2010 | `categoria` vazia | Rejeitar |
| 12 | 2011 | `canal` = `"telefone"` (fora do domínio) | Rejeitar |
| 13 | 2012 | `preco_unitario` negativo | Rejeitar |
| 14 | 2013 | Linha válida | Aceitar |
| 15 | 2013 | **ID duplicado** (repete a linha 14) | Rejeitar — exige guardar os IDs já vistos |
| 16 | 2015 | `data` = `2026-02-31` (dia não existe em fevereiro) | Rejeitar — `strptime` pega isso |
| 17 | 2016 | `preco_unitario` = `1849,00` **sem aspas** → gera uma coluna extra e desloca todos os campos seguintes | Rejeitar. Este é o caso mais traiçoeiro: o `DictReader` joga o excedente na chave `None`. Detecte comparando o número de campos. |
| 18 | 2017 | Linha válida | Aceitar |

**Resultado esperado:** 3 linhas válidas (2001, 2013 e 2017) e 14 rejeitadas.

</details>

---

## Por que isso é realista

Nenhum destes defeitos é inventado. Todos aparecem em dados reais:

- Planilhas preenchidas à mão geram espaços, capitalização inconsistente e datas em formato brasileiro.
- Exportações do Excel em PT-BR usam vírgula decimal, o que quebra CSVs separados por vírgula.
- Integrações mal feitas duplicam registros quando há retry.
- Campos novos (`canal`) entram em produção antes de todos os sistemas serem atualizados, deixando vazios.

O objetivo do M01 não é fazer o programa funcionar com dados bonitos. É fazer o programa **não mentir** quando os dados são feios.
