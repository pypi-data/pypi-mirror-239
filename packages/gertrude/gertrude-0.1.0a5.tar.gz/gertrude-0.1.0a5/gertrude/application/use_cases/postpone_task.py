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

from gertrude.domain.task_management.enums import TaskStates
from gertrude.domain.task_management.exceptions import (
    TaskNotFound,
    TransitionNotAllowed,
)
from gertrude.domain.task_management.repositories import DomainHistory, Tasks
from gertrude.domain.task_management.value_objects import TaskId


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str


class Presenter(ABC):
    @abstractmethod
    def missing_task_id(self) -> None:
        ...

    @abstractmethod
    def incorrect_task_id(self) -> None:
        ...

    @abstractmethod
    def task_not_found(self) -> None:
        ...

    @abstractmethod
    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        ...

    @abstractmethod
    def task_postponed(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks

    def execute(self, request: Request) -> None:
        if not request.task_id:
            return self.presenter.missing_task_id()

        try:
            task_id = TaskId.instanciate(request.task_id)
        except ValueError:
            return self.presenter.incorrect_task_id()

        try:
            task = self.tasks.load(task_id)
            self.history << task.mark_as_actionable()
        except TaskNotFound:
            return self.presenter.task_not_found()
        except TransitionNotAllowed as exc:
            return self.presenter.transition_not_allowed(exc.current, exc.next)

        self.presenter.task_postponed()
