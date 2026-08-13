"""Cache — porque a tela de estoque faz a mesma pergunta 900 vezes/minuto.

> *"Só existem duas coisas difíceis em computação: invalidação de cache
>  e dar nomes às coisas."* — Phil Karlton

A piada é famosa porque é verdade. **Cache é uma cópia**, e toda cópia
pode divergir do original. A pergunta certa nunca é *"como evito
divergir?"* — é **"por quanto tempo posso divergir sem causar dano?"**

| Dado | Pode divergir por | Por quê |
|------|-------------------|---------|
| Nome/descrição do produto | horas | muda raramente |
| Preço | minutos | promoção precisa entrar rápido |
| **Estoque** | 🔴 segundos, ou nada | vender o que não tem custa dinheiro |
| Saldo financeiro | 🔴 não cacheie | |
"""

from __future__ import annotations

from typing import Any, Callable

# ---------------------------------------------------------------------------
# Chaves
# ---------------------------------------------------------------------------
# 🔑 O desenho da chave é metade do trabalho.
#
#     atlas:estoque:v1:NB-DELL-15              ✅ namespace:recurso:versão:id
#     atlas:relatorio:v1:faturamento:2026-08   ✅ período explícito
#     atlas:produtos:v1:cat=Notebooks&ord=sku  ✅ filtros na chave
#
#     NB-DELL-15                               🔴 colide com outro sistema
#     estoque                                  🔴 uma chave para todos os SKUs
#     atlas:relatorio:hoje                     🔴 "hoje" muda de significado
#
# 💡 O `v1` é o truque mais subestimado. Mudou o FORMATO do que você
#    guarda? Incremente para v2. As chaves v1 expiram sozinhas e você
#    nunca lê um dado no formato antigo achando que é o novo — bug
#    particularmente confuso, porque o cache "funciona".
PREFIXO = "atlas"
VERSAO = "v1"


def chave(recurso: str, *partes: Any) -> str:
    """Monta `atlas:<recurso>:v1:<partes>`.

    TODO: implementar. Normalize as partes (minúsculas, sem espaço) para
          que `Notebooks` e `notebooks` não virem duas entradas.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TTLs — em um lugar só, para poder discutir os números
# ---------------------------------------------------------------------------
# TODO: definir e JUSTIFICAR cada um em comentário.
TTL_PRODUTO = 300        # 5 min  — nome e preço mudam pouco
TTL_ESTOQUE = 10         # 🔴 curto: divergir aqui é vender o que não tem
TTL_RELATORIO = 3_600    # 1 h    — dado histórico não muda
TTL_COTACAO_FRETE = 600  # 10 min — mesmo peso + mesmo CEP = mesmo valor


def obter_ou_calcular(cache, chave_: str, ttl: int,
                      calcular: Callable[[], Any]) -> tuple[Any, bool]:
    """Cache-aside: o padrão mais comum, e o mais fácil de acertar.

        1. olha no cache
        2. não achou → busca na fonte
        3. grava com TTL
        4. devolve (valor, veio_do_cache)

    🔴 O ESTOURO DE CACHE (cache stampede)

       Uma chave popular expira. Nesse instante, TODAS as requisições em
       voo erram o cache e vão juntas ao banco. Com tráfego alto isso é
       uma avalanche — e o banco cai justamente no pico.

       Três defesas, combináveis:

       1. **Trava distribuída** — só um recalcula, os outros esperam.
          Use `SET chave valor NX EX 10` do Redis, não `threading.Lock`:
          com várias instâncias da API, uma trava local não protege nada.

          ⚠️ E confira o cache DE NOVO depois de pegar a trava — outra
             instância pode tê-lo preenchido enquanto você esperava.
             Sem essa segunda checagem, a trava apenas enfileira as
             consultas em vez de evitá-las.

       2. **TTL com jitter** — `ttl + aleatorio(0, ttl // 5)` faz as
          chaves expirarem espalhadas em vez de todas juntas.

       3. **Recomputação antecipada** — renova antes de expirar, com o
          valor velho ainda servindo.

    TODO: implementar com ao menos as defesas 1 e 2.
    """
    raise NotImplementedError


def invalidar(cache, *chaves: str) -> int:
    """Apaga chaves. Devolve quantas existiam.

    🔑 Chame em TODO caminho de escrita — `POST`, `PATCH`, `DELETE`, a
       carga noturna, o webhook, o script de correção manual.

    ⚠️ O caminho esquecido é a regra, não a exceção. Por isso:

       🧭 **Use TTL *e* invalidação explícita.** A invalidação cuida do
          caso normal; o TTL é a rede de segurança para o caminho que
          você esqueceu. Quem usa só invalidação serve dado velho para
          sempre no dia em que errar.

    TODO: implementar.
    """
    raise NotImplementedError


def invalidar_por_padrao(cache, padrao: str) -> int:
    """Apaga tudo que casa com `atlas:produtos:v1:*`.

    ⚠️ Use `SCAN`, nunca `KEYS`. O `KEYS` percorre o banco inteiro e
       BLOQUEIA o Redis — que é de thread única. Num Redis de produção
       com milhões de chaves, um `KEYS *` congela a aplicação toda.

    💭 E pergunte-se se você precisa disto. Invalidação por padrão
       costuma ser sinal de que as chaves estão mal desenhadas.

    TODO: implementar com scan_iter.
    """
    raise NotImplementedError
