#!/usr/bin/env python3
"""
Ponto de entrada do pipeline de dados do Atlas.
═══════════════════════════════════════════════════════════════════════

    python scripts/rodar_pipeline.py                  # ontem
    python scripts/rodar_pipeline.py 2026-03-12       # um dia específico
    python scripts/rodar_pipeline.py 2026-03-01 2026-03-31   # intervalo
    python scripts/rodar_pipeline.py --forcar         # ignora a trava

───────────────────────────────────────────────────────────────────────
🔴 Por que o padrão é ONTEM e não HOJE
───────────────────────────────────────────────────────────────────────

Porque hoje ainda não acabou. Rodar o pipeline de "hoje" às 3h da
manhã processa 3 horas de pedidos e chama isso de "o dia". O número
sai baixo, e não há erro nenhum para investigar.

Todo pipeline diário processa o dia FECHADO. No Airflow isso é o `ds`:
a DAG agendada para 03:00 de 14/08 tem `ds = 2026-08-13`. Não é
detalhe de implementação — é a definição do que o dado significa.

───────────────────────────────────────────────────────────────────────
🔴 Por que a data é PARÂMETRO e não `date.today()`
───────────────────────────────────────────────────────────────────────

Porque em novembro a Aurora vai mudar a regra da margem e pedir para
recalcular março. Se a data estiver embutida no código, "recalcular
março" significa mexer no código, e o dado de março passa a depender
de qual versão do script você rodou.

Data como parâmetro é o que transforma reprocessamento de operação de
risco em `python scripts/rodar_pipeline.py 2026-03-12`.

⚠️  ESQUELETO. Assinaturas e TODOs prontos; os corpos são seus.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

# Deixa `src/` importável sem precisar de `pip install -e .`
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# TODO: from atlas.dados.orquestracao import rodar, resumo


def analisar_argumentos(argv: list[str] | None = None) -> argparse.Namespace:
    """Monta o parser da linha de comando."""
    # TODO: implemente com argparse:
    #
    #   dias        0, 1 ou 2 datas posicionais (nargs="*")
    #   --forcar    ignora a trava (NUNCA o portão de qualidade)
    #   --so        limita as fontes: --so banco csv
    #   --seco      mostra o que faria, sem escrever nada
    #
    # 💭 O `--seco` (dry-run) parece supérfluo até a primeira vez em
    #    que você for reprocessar 90 dias e quiser conferir a lista de
    #    partições ANTES de sobrescrever alguma coisa.
    raise NotImplementedError


def dias_do_intervalo(inicio: date, fim: date) -> list[date]:
    """Todos os dias entre inicio e fim, inclusive."""
    # TODO: implemente.
    raise NotImplementedError


def main(argv: list[str] | None = None) -> int:
    """Devolve o código de saída do processo."""
    # TODO:
    #   1. args = analisar_argumentos(argv)
    #   2. determine a lista de dias (padrão: [ontem])
    #   3. para cada dia: execucoes = rodar(dia, forcar=args.forcar)
    #   4. imprima o resumo
    #   5. devolva o código de saída
    #
    # ───────────────────────────────────────────────────────────────
    # 🔴 O CÓDIGO DE SAÍDA IMPORTA MAIS DO QUE PARECE
    # ───────────────────────────────────────────────────────────────
    #
    # Este script vai ser chamado por cron, systemd timer ou Airflow.
    # Nenhum dos três lê a sua saída bonita. Os três olham UM número:
    #
    #     0    deu certo
    #     1    falhou — alguma tarefa crítica não passou
    #     2    trava ocupada (outro processo rodando)
    #     3    portão de qualidade reprovou
    #
    # Um script que imprime "❌ ERRO" e devolve 0 é um pipeline que
    # falha em silêncio para sempre. O monitoramento do M09 nunca vai
    # tocar, porque para o sistema operacional deu tudo certo.
    #
    # 🔑 Distinguir 2 de 1 é o que evita alerta falso: "já estava
    #    rodando" não é falha, é concorrência normal.
    #
    # ───────────────────────────────────────────────────────────────
    # 🔴 REPROCESSAMENTO DE INTERVALO — SEQUENCIAL, NÃO PARALELO
    # ───────────────────────────────────────────────────────────────
    #
    # Tentador: 90 dias, 8 processos ao mesmo tempo. Três motivos para
    # não fazer:
    #
    #   1. a trava é uma só (e se você criar uma por dia, oito
    #      processos batem no banco de origem ao mesmo tempo);
    #   2. a verificação de volume compara com o histórico — que os
    #      outros processos estão escrevendo AGORA;
    #   3. quando falhar no dia 47, você não vai saber quais dos 90
    #      terminaram.
    #
    # Sequencial, com log por dia. Demora mais e você dorme melhor.
    raise NotImplementedError


if __name__ == "__main__":
    sys.exit(main())
