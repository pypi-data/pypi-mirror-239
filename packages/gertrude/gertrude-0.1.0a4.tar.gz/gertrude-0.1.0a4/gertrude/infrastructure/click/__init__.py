# Gertrude --- GTD done right
# Copyright © 2020-2022 Tanguy Le Carrour <tanguy@bioneland.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
from time import sleep

import click
from bles import Projectionist, ProjectorRegistry
from blessql import EVENT_REGISTRY, LEDGER_REGISTRY, EventStore, Ledger
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session, sessionmaker

from gertrude.application import projectors
from gertrude.infrastructure.sqlalchemy import projections, repositories

level = logging.DEBUG
str_fmt = "[%(asctime)s] [%(levelname)s] %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S %z"
logging.basicConfig(format=str_fmt, level=level, datefmt=date_fmt)


def build(dsn: str) -> click.Group:
    return cli(obj={"dsn": dsn})  # type: ignore[no-any-return]


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    pass


@cli.group()
@click.pass_context
def db(ctx: click.Context) -> None:
    pass


@db.command()
@click.pass_context
def initialise(ctx: click.Context) -> None:
    """Initialise DB."""

    click.echo("Initialising DB schemas…")
    create_tables("events", ctx.obj["dsn"], EVENT_REGISTRY.metadata)
    create_tables("ledger", ctx.obj["dsn"], LEDGER_REGISTRY.metadata)
    create_tables("projections", ctx.obj["dsn"], projections.METADATA)
    create_tables("data", ctx.obj["dsn"], repositories.METADATA)

    click.echo("Booting projectors…")
    with sessionmaker(bind=create_engine(ctx.obj["dsn"]))() as session:
        projectionist = build_projectionist(session)
        projectionist.boot()
        session.commit()


def create_tables(schema: str, dsn: str, metadata: MetaData) -> None:
    click.echo(f"Initialising schema `{schema}`.")
    engine = create_engine(dsn)
    metadata.create_all(engine)


def build_projectionist(session: Session) -> Projectionist:
    store = EventStore(session)
    ledger = Ledger(session)
    registry = ProjectorRegistry([projectors.Tasks(projections.Tasks(session))])

    return Projectionist(store, ledger, registry)


@cli.group()
@click.pass_context
def projectionnist(ctx: click.Context) -> None:
    pass


@projectionnist.command()
@click.pass_context
def start(ctx: click.Context) -> None:
    """Start the projection manager."""

    with sessionmaker(bind=create_engine(ctx.obj["dsn"]))() as session:
        while True:
            projectionist = build_projectionist(session)
            projectionist.play()
            session.commit()
            sleep(1)
