"""
Camada de dados do Atlas — o pipeline analítico.
═══════════════════════════════════════════════════════════════════════

Este pacote NÃO é a API. É o outro lado do sistema.

    API (src/atlas/api/)          Pipeline (src/atlas/dados/)
    ─────────────────────         ───────────────────────────
    responde em milissegundos     roda uma vez por noite
    uma linha por vez             milhões de linhas por vez
    OLTP — transacional           OLAP — analítico
    o cliente espera              ninguém está esperando

A regra que justifica a separação inteira:

    🔴 O pipeline NUNCA consulta o banco que atende o cliente
       em horário de pico, e NUNCA escreve nele.

    Ele lê uma réplica (ou lê no horário morto), escreve no lago,
    e a API lê o lago quando precisa de um agregado.

═══════════════════════════════════════════════════════════════════════
O fluxo, do começo ao fim
═══════════════════════════════════════════════════════════════════════

    origens            bronze          prata           ouro
    ───────            ──────          ─────           ────
    banco  ─┐
    CSV    ─┼─ extracao ─→ cru,   ─→ limpo,   ─→ agregado,
    API    ─┘   (marca      como       tipado,     pronto para
                d'água)     chegou     validado    a pergunta
                              │
                              └─→ quarentena (o que não passou)

Módulos:

    extracao.py       de onde o dado vem, e como saber onde parou
    contratos.py      o que é um dado válido — em Pydantic
    transformacao.py  bronze → prata → ouro
    qualidade.py      as seis verificações, antes de publicar
    orquestracao.py   quem roda o quê, em que ordem, e o que fazer
                      quando uma etapa falha

═══════════════════════════════════════════════════════════════════════

📖 Leia `ROTEIRO_M10.md` na raiz do projeto antes de escrever a
   primeira linha. A ordem das etapas importa mais aqui do que em
   qualquer outro módulo — construir o ouro antes do portão de
   qualidade é como publicar antes de conferir.

⚠️  Todos os arquivos deste pacote são ESQUELETOS. As assinaturas e os
    `# TODO:` estão prontos; os corpos são seus.
"""

# TODO: quando terminar `orquestracao.py`, exporte aqui o que o resto
#       do projeto precisa importar. Sugestão de superfície pública
#       mínima (o `scripts/rodar_pipeline.py` só deveria precisar
#       destes dois nomes):
#
#           from atlas.dados.orquestracao import construir_dag, executar_dag
#
#           __all__ = ["construir_dag", "executar_dag"]
#
#       Repare no que essa lista NÃO tem: nada de `pandas`, nada de
#       caminho de arquivo, nada de `extrair_vendas`. Quem chama o
#       pipeline não precisa saber que ele usa pandas — e no dia em
#       que você trocar por Polars, quem chama não muda.

__all__: list[str] = []
