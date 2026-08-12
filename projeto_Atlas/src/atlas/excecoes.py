"""Exceções de domínio do Atlas.

**Por que criar exceções próprias em vez de usar ValueError?**

1. **Comunicam intenção.** `LinhaInvalidaError` diz muito mais que `ValueError`.
2. **Permitem tratamento seletivo.** Lá na CLI você quer capturar erros de
   negócio e mostrar mensagem amigável, mas deixar bugs de programação
   (TypeError, AttributeError) estourarem — eles precisam aparecer.
3. **Uma base comum resolve tudo de uma vez.** Com `AtlasError` no topo da
   hierarquia, `except AtlasError:` captura qualquer erro previsto do sistema.

Hierarquia:

    AtlasError
    ├── ArquivoInvalidoError    (o arquivo em si está errado)
    ├── LinhaInvalidaError      (uma linha específica está errada)
    └── MetricaIndefinidaError  (não dá para calcular — ex.: divisão por zero)

⚠️ Este módulo não importa nada. É folha da árvore de dependências.
"""


class AtlasError(Exception):
    """Exceção base de todo o sistema Atlas.

    Capture esta na fronteira do programa (CLI) para tratar qualquer erro
    previsto de uma vez só.
    """

    # TODO: nada a implementar. Uma classe com só docstring é válida em Python.
    #       (Se precisar de um corpo explícito, use `pass`.)


class ArquivoInvalidoError(AtlasError):
    """O arquivo de entrada não pode ser processado.

    Casos: não existe, está vazio, não tem cabeçalho, falta coluna obrigatória.
    """

    # TODO


class LinhaInvalidaError(AtlasError):
    """Uma linha do CSV não passou na validação.

    Esta exceção NÃO deve derrubar o programa. Ela é capturada pelo laço de
    validação, que registra a rejeição e segue para a próxima linha.

    TODO (recomendado): guarde `numero_linha` e `campo` como atributos, além
    da mensagem. Isso permite montar o relatório de rejeições com precisão:

        raise LinhaInvalidaError(
            numero_linha=42,
            campo="quantidade",
            mensagem="valor não inteiro: 'dez'",
        )

    Para isso você precisa sobrescrever __init__, guardar os atributos e
    chamar super().__init__(mensagem_formatada).
    """

    # TODO: implementar __init__ com numero_linha, campo e mensagem.


class MetricaIndefinidaError(AtlasError):
    """Não é possível calcular uma métrica com os dados disponíveis.

    Exemplo: ticket médio quando não há nenhum pedido pago.

    💭 Reflita: é melhor levantar esta exceção ou devolver 0.0?
       Depende de quem consome. Um relatório provavelmente prefere 0.0 com
       uma nota; um sistema de cobrança prefere falhar alto. Decida e
       documente sua escolha.
    """

    # TODO
