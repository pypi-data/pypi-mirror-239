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

from sqlalchemy import Column, Integer, MetaData, String, Table
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.repositories import Projects as ProjectsABC

METADATA = MetaData()
PROJECTS = Table(
    "projects",
    METADATA,
    Column("_pk", Integer, primary_key=True),
    Column("id", String(50), unique=True),
    Column("name", String(50)),
)


class Projects(ProjectsABC):
    def __init__(self, session: Session) -> None:
        self.__session = session

    def save(self, project: Project) -> None:
        if project._pk:
            self.__update(project)
        else:
            self.__insert(project)

    def __update(self, project: Project) -> None:
        self.__session.execute(
            PROJECTS.update()
            .where(PROJECTS.c._pk == project._pk)
            .values(id=project.id, name=project.name)
        )

    def __insert(self, project: Project) -> None:
        self.__session.execute(
            PROJECTS.insert().values(id=project.id, name=project.name)
        )

    def load(self, id: str) -> Optional[Project]:
        stmt = select([PROJECTS]).where(PROJECTS.c.id == id)
        if result := self.__session.execute(stmt).fetchone():
            return Project(
                id=result[PROJECTS.c.id],
                name=result[PROJECTS.c.name],
            )
        return None

    def list(self) -> list[Project]:
        stmt = select([PROJECTS])
        result = self.__session.execute(stmt)
        return [
            Project(id=row[PROJECTS.c.id], name=row[PROJECTS.c.name])
            for row in result.fetchall()
        ]
