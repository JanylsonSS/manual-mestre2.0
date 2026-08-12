"""Migração: dos CSVs do Módulo 01 para o banco relacional.

Este é um **ETL** em miniatura — o mesmo desenho que você vai
reencontrar em escala no Módulo 10:

    Extrair (CSV)  ->  Transformar (normalizar/validar)  ->  Carregar (SQL)

🎯 **O requisito mais importante: IDEMPOTÊNCIA.**

   Rodar a migração 1, 2 ou 10 vezes com o mesmo arquivo deve deixar
   o banco exatamente no mesmo estado. Nada de duplicatas.

   Por que isso importa tanto? Porque cargas falham no meio. A rede
   cai, o disco enche, alguém aperta Ctrl+C. Se o processo não pode
   ser reexecutado com segurança, cada falha vira uma operação manual
   de limpeza às duas da manhã.

   O mecanismo: `INSERT ... ON CONFLICT ... DO UPDATE` (UPSERT).
"""

from __future__ import annotations

import csv
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from atlas import config, repositorio, validacao
from atlas.excecoes import AtlasError


@dataclass
class ResultadoMigracao:
    """Relatório do que aconteceu na carga.

    💡 Devolver um objeto estruturado em vez de imprimir direto
       permite que a CLI decida como apresentar, e que os testes
       do M12 verifiquem os números.
    """
    arquivo: str = ""
    linhas_lidas: int = 0
    linhas_validas: int = 0
    clientes_novos: int = 0
    produtos_novos: int = 0
    pedidos_inseridos: int = 0
    itens_inseridos: int = 0
    rejeitados: list[dict] = field(default_factory=list)

    @property
    def linhas_rejeitadas(self) -> int:
        return len(self.rejeitados)

    def resumo(self) -> str:
        """Uma linha para o terminal."""
        # TODO: implementar
        raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Normalização
# ═══════════════════════════════════════════════════════════════
# A dor do M03 é: "a do comercial tem 'Campinas', a do financeiro
# tem 'campinas/SP', a do estoque tem 'CPS'". É AQUI que isso morre.


def normalizar_email(bruto: str) -> str:
    """`.strip().lower()`.

    ⚠️ Isto é o que impede o mesmo cliente de virar 4 clientes.
       E-mail é case-insensitive no mundo real; se você gravar
       'Maria@X.com' e 'maria@x.com', o UNIQUE não vai reclamar
       e você terá duplicatas silenciosas.
    """
    # TODO: implementar
    raise NotImplementedError


def normalizar_cidade(bruto: str) -> str:
    """Remove espaços extras e aplica Title Case.

    💡 " são   paulo " -> "São Paulo"
       Colapse espaços internos com " ".join(texto.split()).

    💭 Desafio: e "Ribeirão Preto/SP"? E "S. Paulo"? Um normalizador
       de verdade precisaria de uma tabela de-para. Documente a
       limitação em vez de fingir que resolveu.
    """
    # TODO: implementar
    raise NotImplementedError


def normalizar_uf(bruto: str) -> str:
    """`.strip().upper()`, validando que tem 2 letras.

    Raises:
        LinhaInvalidaError: se não for uma UF plausível.

    💡 Considere validar contra a lista das 27 UFs brasileiras,
       não só o comprimento. 'XX' tem 2 letras e não existe.
    """
    # TODO: implementar
    raise NotImplementedError


def normalizar_status(bruto: str) -> str:
    """`.strip().lower()`, validando contra config.STATUS_VALIDOS."""
    # TODO: implementar
    raise NotImplementedError


def derivar_sku(nome_produto: str) -> str:
    """Gera um SKU determinístico a partir do nome do produto.

    O CSV do M01 não tem SKU, mas o schema exige. Você precisa
    derivar um — e ele precisa ser **estável**: o mesmo nome deve
    sempre gerar o mesmo SKU, senão a idempotência quebra.

    Exemplo: "Notebook Dell Inspiron 15" -> "NOTEBOOK-DELL-INSP"

    ⚠️ NÃO use hash aleatório, uuid4() nem timestamp. Precisa ser
       uma função pura do nome.

    💡 Sugestão: remova acentos, maiúsculas, troque espaços por
       hífen, trunque em ~20 caracteres. Trate colisões.
    """
    # TODO: implementar
    raise NotImplementedError


def inferir_categoria(nome_produto: str) -> str:
    """Deduz a categoria a partir do nome do produto.

    O CSV do M01 tem uma coluna `categoria` — se ela existir, use-a.
    Se não, infira por palavras-chave:

        'notebook', 'macbook'        -> Notebooks
        'monitor'                    -> Monitores
        'mouse', 'teclado', 'webcam' -> Periféricos
        'ssd', 'hd', 'pendrive'      -> Armazenamento
        'roteador', 'repetidor'      -> Redes
        'headset', 'fone'            -> Áudio
        (nenhuma)                    -> Outros

    💡 Um dicionário {palavra: categoria} percorrido com `in`
       resolve. Não precisa de regex.
    """
    # TODO: implementar
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Carga
# ═══════════════════════════════════════════════════════════════


def migrar_csv(caminho_csv: Path, conexao: sqlite3.Connection) -> ResultadoMigracao:
    """Carrega um CSV de vendas para o banco.

    Args:
        caminho_csv: Arquivo de origem.
        conexao: Conexão já aberta e com schema aplicado.

    Returns:
        ResultadoMigracao com as contagens e as rejeições.

    Raises:
        ArquivoInvalidoError: se o arquivo não existir ou faltar coluna.

    Fluxo para cada linha:
        1. Validar e converter tipos (reaproveite `validacao.py` do M01!)
        2. Normalizar textos
        3. UPSERT da categoria       -> categoria_id
        4. UPSERT do produto         -> produto_id
        5. UPSERT do cliente         -> cliente_id
        6. UPSERT do pedido          -> pedido_id
        7. Inserir o item do pedido

    ⚠️ TUDO dentro de UMA transação. Se a linha 4.000 falhar de forma
       inesperada, o banco não pode ficar com metade da carga.

    ⚠️ Linha inválida NÃO derruba o processo: registre em
       `resultado.rejeitados` com número da linha e motivo, e siga.
       Essa distinção é importante:
         - erro de DADO (linha ruim)      -> registra e continua
         - erro de SISTEMA (disco cheio)  -> rollback e propaga

    💡 O CSV do M01 tem uma linha por ITEM, não por pedido. Vários
       itens do mesmo pedido compartilham o `id`. Sua carga precisa
       lidar com isso: o pedido é inserido uma vez (UPSERT) e cada
       linha vira um item.
    """
    # TODO: implementar
    raise NotImplementedError


def migrar_diretorio(pasta: Path, conexao: sqlite3.Connection) -> list[ResultadoMigracao]:
    """Migra todos os .csv de uma pasta, em ordem alfabética.

    Cada arquivo em sua própria transação: se o terceiro falhar,
    os dois primeiros permanecem carregados.
    """
    # TODO: implementar
    raise NotImplementedError


def gravar_rejeitados(resultado: ResultadoMigracao, caminho: Path) -> None:
    """Grava as linhas rejeitadas em CSV, para investigação.

    Colunas: arquivo, linha, campo, motivo, dado_original

    💡 Grave mesmo quando não houver rejeições (só o cabeçalho).
       Arquivo vazio comunica "verifiquei e estava tudo certo";
       arquivo ausente comunica "não sei se rodou".
    """
    # TODO: implementar
    raise NotImplementedError


# ═══════════════════════════════════════════════════════════════
#  Verificação pós-carga
# ═══════════════════════════════════════════════════════════════


def conferir_com_csv(caminho_csv: Path, conexao: sqlite3.Connection) -> dict:
    """Compara os totais do banco com os totais calculados do CSV.

    Esta é a verificação mais importante do módulo: prova que a
    migração **não alterou os números**.

    Deve comparar:
        - Faturamento total (pedidos pagos)
        - Número de pedidos distintos
        - Número de itens
        - Faturamento por cidade

    Returns:
        Dict com os valores dos dois lados e a diferença.

    ⚠️ Espere pequenas diferenças de arredondamento em REAL. Use uma
       tolerância (ex.: abs(a - b) < 0.01) em vez de igualdade exata.
       Revise a armadilha do ponto flutuante na aula 01_01.

    💭 Se os números NÃO baterem, quase sempre é um destes:
        - Linhas rejeitadas que o M01 aceitava (ou vice-versa)
        - JOIN multiplicando linhas no cálculo
        - Filtro de status esquecido em um dos lados
    """
    # TODO: implementar
    raise NotImplementedError


def testar_idempotencia(caminho_csv: Path, conexao: sqlite3.Connection) -> bool:
    """Roda a migração duas vezes e verifica que o estado não mudou.

    Returns:
        True se as contagens de todas as tabelas forem idênticas.

    💡 Compare `repositorio.estatisticas_banco()` antes e depois.

    🎯 Este é o critério de aceitação da Parte C do projeto.
    """
    # TODO: implementar
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: migrar o CSV padrão e imprimir o resumo.
    pass
