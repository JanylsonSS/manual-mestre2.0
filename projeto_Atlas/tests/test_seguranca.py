"""🔒 Os testes mais baratos e mais valiosos da suíte.

Cada um destes previne um incidente que já aconteceu em alguma empresa.
Nenhum passa de 10 linhas.

💭 Testes de segurança têm uma propriedade rara: eles quase nunca
   quebram por refatoração, porque verificam PROPRIEDADES, não
   implementação. "custo não sai numa resposta" continua verdadeiro
   depois de qualquer reescrita — ou deveria.
"""

import pytest

# TODO: importar o que precisar

# 🔒 Campos que NUNCA podem sair numa resposta pública.
CAMPOS_PROIBIDOS = {"custo", "senha", "senha_hash", "password",
                    "fornecedor", "observacao_interna", "margem"}


@pytest.mark.seguranca
def test_nenhuma_resposta_expoe_campo_interno(cliente, catalogo):
    """Varre as rotas de leitura de uma vez só.

    🔴 O incidente que isto previne: o marketplace concorrente consulta
       a API pública e descobre a margem de cada produto.

    💡 Faça este teste PERCORRER as rotas em vez de listá-las uma a uma.
       Assim, quando alguém adicionar uma rota nova sem `response_model`,
       o teste pega.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_openapi_nao_documenta_campo_interno(cliente):
    """🎯 A versão estática do teste acima — e mais forte.

    Em vez de conferir as respostas que você lembrou de testar, leia o
    `/openapi.json` e verifique TODOS os esquemas usados em resposta.

    Isso pega rotas que você esqueceu de testar.

    ⚠️ Colete só os esquemas referenciados em `responses`. Um esquema de
       ENTRADA com `password` é normal — é o formulário de login.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.mark.seguranca
@pytest.mark.parametrize("papel,esperado", [
    (None,       401),      # anônimo   → não sei quem é você
    ("leitor",   403),      # leitor    → sei, e você não pode
    ("operador", 403),      # operador  → idem (DELETE é de admin)
    ("admin",    204),
])
def test_apagar_produto_exige_admin(cliente, catalogo, usuarios, papel, esperado):
    """🎯 A tabela inteira de autorização, num teste.

    O `401` vs `403` importa: o primeiro pede que você se identifique,
    o segundo diz que identificar-se não vai adiantar.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.mark.seguranca
@pytest.mark.parametrize("campo", ["custo", "inexistente", "id",
                                   "preco; DROP TABLE produtos--"])
def test_ordenacao_so_aceita_lista_branca(cliente, campo):
    """🔴 DOIS ataques diferentes, uma defesa.

    · `preco; DROP TABLE` → injeção de SQL. `ORDER BY` não aceita
      placeholder: o `?` protege VALORES, não IDENTIFICADORES.

    · `custo` → vazamento por canal lateral. É um campo REAL: ordenar
      por ele revela a ordem de margem do catálogo inteiro sem nunca
      exibir o valor. O `response_model` não protege contra isso.

    O segundo é o que quase todo mundo esquece.

    TODO: implementar — todos devem devolver 422.
    """
    raise NotImplementedError


@pytest.mark.seguranca
@pytest.mark.parametrize("por_pagina", [0, -1, 101, 10_000_000])
def test_paginacao_tem_teto(cliente, por_pagina):
    """🔴 `?por_pagina=10000000` é um ataque de negação de serviço de uma
    linha: o banco monta a consulta, a API serializa tudo em JSON, e a
    memória acaba.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_erro_de_login_e_identico(cliente, usuarios):
    """🔴 Byte a byte idêntico para "e-mail não existe" e "senha errada".

    Diferenciar entrega ao atacante a lista de quem tem conta na
    empresa — que é meio caminho para um ataque direcionado.

        assert r1.status_code == r2.status_code
        assert r1.json() == r2.json()

    💭 Rigorosamente, ainda dá para inferir pelo TEMPO: quando o e-mail
       não existe você pula o bcrypt e responde em 1 ms. A defesa é
       rodar um hash descartável nesse caso. Vale um teste à parte.

    TODO: implementar.
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_resposta_de_erro_nao_vaza_traceback(cliente):
    """🔴 Traceback numa resposta revela caminhos de arquivo, versões de
    biblioteca, estrutura do projeto e às vezes credenciais.

    Verifique que a resposta de 500 não contém "Traceback", nem
    "site-packages", nem o caminho do projeto.

    TODO: implementar (provoque um erro numa rota de teste).
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_webhook_recusa_assinatura_invalida(cliente):
    """As três recusas: sem assinatura, assinatura forjada, timestamp velho.

    TODO: implementar — todos devem devolver 401.
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_upload_recusa_executavel(cliente):
    """🔴 Magic bytes, não extensão.

    Envie `b"\\x7fELF..."` com o nome `planilha.csv` e o `Content-Type`
    `text/csv`. Ambos são escolhidos pelo cliente; só os primeiros bytes
    dizem o que o arquivo realmente é.

    TODO: implementar — deve devolver 415.
    """
    raise NotImplementedError


@pytest.mark.seguranca
def test_upload_nao_escreve_fora_da_pasta(cliente, tmp_path):
    """🔴 Path traversal: nome `../../../etc/passwd`.

    Verifique que o arquivo gravado está DENTRO da pasta de uploads.
    O upload pode até ser aceito — o que não pode é escapar da pasta.

    TODO: implementar.
    """
    raise NotImplementedError
