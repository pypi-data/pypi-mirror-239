# Gertrude --- GTD done right
# Copyright © 2020-2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from typing import Optional

from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from gertrude.application import projectors
from gertrude.domain.task_management import dto, enums, projections

METADATA = MetaData()
TASKS = Table(
    "tasks",
    METADATA,
    Column("id", String),
    Column("title", String),
    Column("description", String),
    Column("state", String),
    Column("belongs_to", String),
    Column("delegated_to", String, default=""),
    Column("assigned_to", String, default=""),
)


class Tasks(projectors.TaskProjection, projections.Tasks):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def capture_task(
        self, id: str, belongs_to: str, title: str, description: str
    ) -> None:
        self.__session.execute(
            TASKS.insert().values(
                id=id,
                title=title,
                description=description,
                state=enums.TaskStates.CAPTURED.value,
                belongs_to=belongs_to,
            )
        )

    def update_state(self, id: str, state: enums.TaskStates) -> None:
        self.__session.execute(
            TASKS.update().where(TASKS.c.id == id).values(state=state.value)
        )

    def delegate_to(self, id: str, delegated_to: str) -> None:
        self.__session.execute(
            TASKS.update()
            .where(TASKS.c.id == id)
            .values(state=enums.TaskStates.DELEGATED.value, delegated_to=delegated_to)
        )

    def assign_to(self, id: str, assigned_to: str) -> None:
        self.__session.execute(
            TASKS.update().where(TASKS.c.id == id).values(assigned_to=assigned_to)
        )

    def load(self, id: str) -> Optional[dto.Task]:
        stmt = select([TASKS]).where(TASKS.c.id == id)
        result = self.__session.execute(stmt).fetchone()
        if result:
            return dto.Task(
                id=result[TASKS.c.id],
                title=result[TASKS.c.title],
                description=result[TASKS.c.description],
                state=result[TASKS.c.state],
                delegated_to=result[TASKS.c.delegated_to],
                assigned_to=result[TASKS.c.assigned_to],
            )
        return None

    def list(
        self, /, *, state: Optional[enums.TaskStates] = None, assigned_to: str = ""
    ) -> list[dto.Task]:
        # FIXME delay added to wait for the projections to be updated.
        import time

        time.sleep(1)

        stmt = select([TASKS])
        if state:
            stmt = stmt.where(TASKS.c.state == state.value)
        if assigned_to:
            stmt = stmt.where(TASKS.c.assigned_to == assigned_to)

        result = self.__session.execute(stmt)
        return [
            dto.Task(
                id=row[TASKS.c.id],
                title=row[TASKS.c.title],
                description=row[TASKS.c.description],
                state=row[TASKS.c.state],
                delegated_to=row[TASKS.c.delegated_to],
                assigned_to=row[TASKS.c.assigned_to],
            )
            for row in result.fetchall()
        ]
