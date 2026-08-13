"""Fixtures compartilhadas por toda a suíte.

🔑 O pytest encontra este arquivo sozinho — nenhum import é necessário.

🎯 O objetivo de tudo aqui é UM: **cada teste começa do mesmo estado**,
   independentemente do que os outros fizeram e da ordem em que rodaram.

   Um teste que depende da ordem é pior do que nenhum teste: ele falha
   em situações sem relação com o bug, e você aprende a ignorá-lo.
"""

import pytest

# TODO: importar create_engine, sessionmaker, StaticPool
# TODO: importar TestClient
# TODO: importar Base, criar_app, obter_sessao do seu projeto


# ═══════════════════════════════════════════════════════════════════════
#  Banco isolado
# ═══════════════════════════════════════════════════════════════════════
@pytest.fixture
def sessao():
    """Um banco NOVO, em memória, por teste.

    Isolamento pela via mais simples: o banco não é limpo, é RECRIADO.
    Não há estado para vazar.

    🔴 `poolclass=StaticPool` é OBRIGATÓRIO com `sqlite:///:memory:`.

       Um banco em memória pertence à CONEXÃO. O TestClient roda as
       rotas numa thread do pool, que abriria uma conexão nova — e
       encontraria um banco vazio. O erro é

           sqlite3.OperationalError: no such table: produtos

       que parece problema de modelo e não é. Guarde esse sintoma.

    💭 "Criar um engine por teste não é caro?" Para SQLite em memória,
       custa cerca de 1 ms. Para PostgreSQL seria caro — e lá se usa o
       padrão de transação + rollback (ver ROTEIRO_M07.md).

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.fixture
def cliente(sessao):
    """TestClient com o banco de teste no lugar do real.

    🎯 Isto só funciona porque as rotas DECLARAM que precisam de uma
       sessão (`Depends`) em vez de criá-la. É o retorno concreto do
       trabalho de arquitetura do M06 — e a razão prática de usar
       `Depends` para tudo.

        app.dependency_overrides[obter_sessao] = lambda: sessao

    ⚠️ Limpe os overrides no fim, senão eles vazam para outros testes.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.fixture
def cache_teste():
    """`fakeredis` — a mesma API do Redis, sem servidor.

    ⚠️ Como o mongomock no M05: simulacro cobre o caminho comum e falha
       nas bordas. Ele não reproduz cluster, eviction sob pressão de
       memória, nem latência de rede.

    🔑 Comece limpo: `cache.flushall()`.

    TODO: implementar.
    """
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Dados
# ═══════════════════════════════════════════════════════════════════════
@pytest.fixture
def catalogo(sessao):
    """Alguns produtos no banco.

    ⚠️ Inclua ao menos um com estoque ZERO. As bordas são onde os bugs
       moram, e "não tem estoque" é a borda mais importante do Atlas.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.fixture
def usuarios(sessao):
    """Um usuário de cada papel: leitor, operador, admin.

    💡 Devolva também os cabeçalhos de autenticação prontos — assim os
       testes de autorização ficam de duas linhas.

    TODO: implementar.
    """
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════════════
#  Fixtures do próprio pytest que valem conhecer
# ═══════════════════════════════════════════════════════════════════════
#   tmp_path      pasta temporária nova por teste
#   monkeypatch   altera env/atributo e desfaz sozinho
#   capsys        captura stdout/stderr
#   caplog        captura o logging (útil para o M04)
#
# 🧭 REGRA DOS ESCOPOS
#
#   function (padrão)  a cada teste          ✅ quase tudo
#   module             por arquivo           🔶 caro E imutável
#   session            uma vez               🔶 engine, container
#
#   🔴 Escopo amplo com objeto MUTÁVEL é armadilha: um teste altera e o
#      próximo recebe o estado sujo. Se precisar de escopo amplo,
#      garanta que o objeto não muda.
