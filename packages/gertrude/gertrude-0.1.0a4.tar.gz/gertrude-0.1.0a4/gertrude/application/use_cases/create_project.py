# Gertrude --- GTD done right
# Copyright © 2020, 2021, 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from abc import ABC, abstractmethod
from dataclasses import dataclass

from gertrude.domain.project_management.entities import Project
from gertrude.domain.project_management.repositories import Projects


@dataclass(frozen=True)
class Request:
    id: str
    name: str


class Presenter(ABC):
    @abstractmethod
    def missing_id(self) -> None:
        ...

    @abstractmethod
    def missing_name(self) -> None:
        ...

    @abstractmethod
    def project_already_exists(self) -> None:
        ...

    @abstractmethod
    def project_created(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    projects: Projects

    def execute(self, request: Request) -> None:
        if not request.id:
            return self.presenter.missing_id()

        if not request.name:
            return self.presenter.missing_name()

        try:
            self.projects.load(request.id)
        except KeyError:
            self.projects.save(Project(id=request.id, name=request.name))
            return self.presenter.project_created()

        return self.presenter.project_already_exists()
