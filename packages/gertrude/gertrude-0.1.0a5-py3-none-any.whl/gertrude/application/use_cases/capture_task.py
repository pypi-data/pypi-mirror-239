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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from gertrude.domain.task_management.entities import Task
from gertrude.domain.task_management.exceptions import TaskNotFound
from gertrude.domain.task_management.repositories import DomainHistory, Tasks, Users
from gertrude.domain.task_management.services import capture_task
from gertrude.domain.task_management.value_objects import ProjectId, TaskId, UserId


@dataclass(frozen=True)
class Request:
    user_id: str
    task_id: str
    title: str
    description: str = ""
    project_id: str = ""


class Presenter(ABC):
    @abstractmethod
    def missing_task_id(self) -> None:
        ...

    @abstractmethod
    def incorrect_task_id(self) -> None:
        ...

    @abstractmethod
    def incorrect_user_id(self) -> None:
        ...

    @abstractmethod
    def incorrect_project_id(self, project_id: str) -> None:
        ...

    @abstractmethod
    def task_id_already_used(self) -> None:
        ...

    @abstractmethod
    def missing_title(self) -> None:
        ...

    @abstractmethod
    def task_captured(self) -> None:
        ...


@dataclass(frozen=True)
class Interactor:
    presenter: Presenter
    history: DomainHistory
    tasks: Tasks
    users: Users

    def execute(self, request: Request) -> None:
        if not request.task_id:
            return self.presenter.missing_task_id()

        try:
            task_id = TaskId.instanciate(request.task_id)
        except Exception:
            return self.presenter.incorrect_task_id()

        try:
            user_id = UserId.instanciate(request.user_id)
        except Exception:
            return self.presenter.incorrect_user_id()

        project_id: Optional[ProjectId] = None
        if request.project_id:
            try:
                project_id = ProjectId.instanciate(request.project_id)
            except Exception:
                return self.presenter.incorrect_project_id(request.project_id)

        try:
            self.tasks.load(task_id)
        except TaskNotFound:
            pass
        else:
            return self.presenter.task_id_already_used()

        if not request.title:
            return self.presenter.missing_title()

        events = capture_task(task_id, user_id, request.title, request.description)

        if project_id:
            task = Task.instanciate(events)  # type: ignore
            events += task.assign_to(project_id)

        self.history << events
        self.presenter.task_captured()
