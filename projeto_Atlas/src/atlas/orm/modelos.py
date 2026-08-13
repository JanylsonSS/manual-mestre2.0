"""Modelos ORM do Atlas — SQLAlchemy 2.0.

**A pergunta que este arquivo responde:** quanto do desenho do Módulo 04
sobreviveu à troca de banco?

Se você separou domínio de persistência lá, a resposta é: **quase tudo**.
As dataclasses de `modelos.py` viram classes mapeadas aqui, as properties
calculadas continuam properties, e `servicos.py` não muda uma linha.

⚠️ ESTE ARQUIVO PRECISA SER UM MÓDULO, NÃO UM NOTEBOOK.

   O SQLAlchemy 2.0 resolve as anotações (`Mapped[int]`) inspecionando o
   namespace do módulo onde a classe foi definida. Em notebook isso falha
   com `MappedAnnotationError`.

📌 Relação com `atlas/modelos.py` (M04):

   | M04 (domínio)              | M05 (persistência)          |
   |----------------------------|-----------------------------|
   | `@dataclass(frozen=True)`  | `class X(Base)`             |
   | `Decimal`                  | `Numeric(12, 2)`            |
   | `Enum`                     | `String` + `CHECK`          |
   | `list[ItemVenda]`          | `relationship()`            |
   | properties calculadas      | properties (iguais!)        |

   💭 Decisão de arquitetura a tomar: você mantém as DUAS camadas
      (domínio puro + ORM, com conversores) ou usa o ORM direto como
      domínio? A primeira é mais limpa e mais trabalhosa. Escolha e
      documente em `docs/ARQUITETURA_DADOS.md`.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (CheckConstraint, DateTime, ForeignKey, Index, Numeric,
                        String, UniqueConstraint, func)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base de todos os modelos.

    💡 O `metadata` desta classe é o que o Alembic inspeciona no
       `--autogenerate`. Se um modelo não herdar daqui, ele fica
       invisível para as migrações — e o autogenerate vai gerar
       um `drop_table` para ele.
    """

    # TODO (opcional): convenção de nomes para constraints.
    #   Sem isso, o SQLite e o Postgres geram nomes diferentes para
    #   a MESMA constraint, e o autogenerate detecta diferença onde
    #   não há. Pesquise `naming_convention`.
    #
    # metadata = MetaData(naming_convention={
    #     "ix": "ix_%(column_0_label)s",
    #     "uq": "uq_%(table_name)s_%(column_0_name)s",
    #     "ck": "ck_%(table_name)s_%(constraint_name)s",
    #     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    #     "pk": "pk_%(table_name)s",
    # })


# ═══════════════════════════════════════════════════════════════
#  Cliente
# ═══════════════════════════════════════════════════════════════

class Cliente(Base):
    __tablename__ = "clientes"

    # A PK já vem pronta: sem pelo menos uma coluna de chave primária,
    # o SQLAlchemy recusa a classe e o módulo nem importa.
    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: declarar os demais campos.
    #   nome          String(120)
    #   email         String(160)  unique, index
    #   cidade        String(80)
    #   uf            String(2)
    #   segmento      String(20)   default "varejo"
    #   data_cadastro Mapped[date]
    #   telefone      Mapped[str | None]
    #
    # 💡 `Mapped[str | None]` gera nullable=True automaticamente.
    #    A anotação de tipo É a definição do schema.

    # TODO: relacionamento 1-N com Pedido
    #   pedidos: Mapped[list[Pedido]] = relationship(back_populates="cliente")
    #
    # ⚠️ NÃO use cascade="all, delete-orphan" aqui: apagar um cliente
    #    não deveria apagar o histórico de pedidos dele. É a mesma
    #    decisão RESTRICT × CASCADE que você tomou no M03.

    __table_args__ = (
        # TODO: CheckConstraint para uf (2 letras maiúsculas)
        # TODO: CheckConstraint para segmento IN ('varejo','corporativo')
    )

    @property
    def praca(self) -> str:
        """'Campinas/SP'."""
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...


# ═══════════════════════════════════════════════════════════════
#  Pedido
# ═══════════════════════════════════════════════════════════════

class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: cliente_id (FK), data, status, canal, frete,
    #       criado_em (server_default=func.now())
    #
    # 💰 `frete` e todo valor monetário: Numeric(12, 2), NUNCA Float.
    #    Você viu por quê na aula 01_01 e de novo no 05_01.
    #
    # ⏰ `criado_em`: no PostgreSQL use DateTime(timezone=True).
    #    Revise a aula 04_05 sobre naive vs aware.

    # TODO: relationships
    #   cliente: Mapped[Cliente] = relationship(back_populates="pedidos")
    #   itens: Mapped[list[ItemPedido]] = relationship(
    #       back_populates="pedido", cascade="all, delete-orphan")
    #
    # ✅ AQUI o cascade FAZ sentido: item de pedido não existe sem
    #    o pedido. É composição, como você decidiu no M03.

    __table_args__ = (
        # TODO: CHECK de status e canal
        # TODO: CHECK frete >= 0
        # TODO: Index composto ("status", "data") — o mais consultado
    )

    @property
    def subtotal(self) -> Decimal:
        """Soma dos itens, sem frete.

        ⚠️ ARMADILHA DE DESEMPENHO: esta property acessa `self.itens`.
           Se a relação não foi carregada com eager loading, cada
           acesso dispara uma consulta — e num laço isso é o N+1.

           Ao listar pedidos, SEMPRE use:
               select(Pedido).options(selectinload(Pedido.itens))
        """
        # TODO
        ...

    @property
    def total(self) -> Decimal:
        # TODO: subtotal + frete
        ...

    @property
    def margem(self) -> Decimal:
        # TODO
        ...

    @property
    def quantidade_itens(self) -> int:
        # TODO: soma das quantidades (não o número de linhas)
        ...

    @property
    def faturado(self) -> bool:
        # TODO
        ...

    @property
    def mes(self) -> str:
        """'2026-07'."""
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...


# ═══════════════════════════════════════════════════════════════
#  ItemPedido
# ═══════════════════════════════════════════════════════════════

class ItemPedido(Base):
    """Tabela de junção COM atributos.

    A mesma modelagem do M03: `pedidos` × `produtos` é N-N, e a tabela
    intermediária carrega `quantidade` e `preco_unitario`.
    """

    __tablename__ = "itens_pedido"

    id: Mapped[int] = mapped_column(primary_key=True)

    # TODO: pedido_id (FK), produto_sku, quantidade, preco_unitario
    #
    # 🎯 DECISÃO DE ARQUITETURA IMPORTANTE:
    #
    #    Os produtos agora vivem no MongoDB. Então este item NÃO tem
    #    FK para uma tabela `produtos` — ele guarda o `sku` como texto.
    #
    #    ⚠️ Isso significa que o banco NÃO garante que o produto existe.
    #       A integridade referencial entre os dois bancos é sua
    #       responsabilidade (Parte G do projeto: reconciliação).
    #
    #    💭 É um custo real da persistência poliglota. Documente-o.
    #
    # 📌 E continue guardando `preco_unitario`: o preço de catálogo
    #    muda no Mongo, o praticado na venda não pode mudar.
    #    Agora essa decisão vale AINDA MAIS — o catálogo é externo.

    __table_args__ = (
        # TODO: UniqueConstraint(pedido_id, produto_sku)
        # TODO: CHECK quantidade > 0
        # TODO: CHECK preco_unitario >= 0
    )

    @property
    def total(self) -> Decimal:
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...


# ═══════════════════════════════════════════════════════════════
#  (Opcional) Espelho do catálogo
# ═══════════════════════════════════════════════════════════════
# TODO (desafio): uma tabela `produtos_espelho` no Postgres com os
#   campos ESTÁVEIS do catálogo (sku, nome, categoria, custo).
#
#   💭 Por quê? Porque relatórios que precisam juntar pedidos e
#      produtos ficariam presos a fazer duas consultas em bancos
#      diferentes e juntar em Python — perdendo a capacidade de
#      agregar no banco.
#
#      Com um espelho sincronizado, o relatório volta a ser um JOIN.
#
#   ⚠️ O custo é a sincronização. Quem mantém o espelho atualizado?
#      Um job? Um Change Stream do Mongo? Escreva a decisão no
#      documento de arquitetura.
#
#   Este é um trade-off real de arquitetura de dados, e não existe
#   resposta certa universal. Existe a que você consegue defender.


if __name__ == "__main__":
    # TODO: criar o schema num SQLite temporário e imprimir o DDL gerado.
    #
    #   from sqlalchemy import create_engine
    #   from sqlalchemy.schema import CreateTable
    #   engine = create_engine("sqlite://")
    #   for tabela in Base.metadata.sorted_tables:
    #       print(CreateTable(tabela).compile(engine))
    pass
