"""Fixtures dos testes de INTEGRAÇÃO.

Aqui pode haver banco, cliente HTTP e arquivo temporário. Não pode
haver **rede de verdade** — use `respx` (M07) para dublar o que sai.

🔴 Teste que depende da internet é teste que falha no avião, no CI sem
   saída, e no dia em que o parceiro estiver fora do ar. Ele não está
   testando o seu código: está testando a conexão.
"""

import pytest

# TODO: reaproveite as fixtures de tests/conftest.py (o pytest as
#       herda automaticamente — não reimplemente `sessao` aqui).

# TODO: fixture `cliente_autenticado`
#
#   Devolve um TestClient já com o cabeçalho Authorization. Sem ela,
#   metade dos testes vira três linhas de login copiadas.
#
#   💡 Faça uma versão POR PAPEL (`cliente_admin`, `cliente_leitura`).
#      É o que torna barato testar autorização — e autorização só se
#      prova com o papel ERRADO tentando e recebendo 403.

# TODO: fixture `lago_temporario`
#
#   tmp_path com bronze/prata/ouro/quarentena/estado, para os testes
#   do pipeline (M10).
#
#   💡 Use o `tmp_path` do próprio pytest, não uma pasta fixa: ele dá
#      um diretório novo por teste e limpa sozinho. Pasta fixa faz
#      um teste enxergar o lixo do anterior.
