# Gertrude --- GTD done right
# Copyright © 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from bles import RunFromBeginningProjector

from gertrude.domain.task_management.enums import TaskStates


class TaskProjection(ABC):
    @abstractmethod
    def capture_task(
        self, task_id: str, user_id: str, title: str, description: str
    ) -> None:
        ...

    @abstractmethod
    def update_state(self, task_id: str, state: TaskStates) -> None:
        ...

    @abstractmethod
    def delegate_to(self, task_id: str, person_id: str) -> None:
        ...

    @abstractmethod
    def assign_to(self, task_id: str, project_id: str) -> None:
        ...


class Tasks(RunFromBeginningProjector):
    def __init__(self, projection: TaskProjection) -> None:
        super().__init__("tasks")
        self.__projection = projection

    def when_task_captured(self, data: dict[str, str]) -> None:
        self.__projection.capture_task(
            data["task_id"], data["user_id"], data["title"], data["description"]
        )

    def when_task_eliminated(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.ELIMINATED)

    def when_task_filed(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.FILED)

    def when_task_incubated(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.INCUBATED)

    def when_task_done(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.DONE)

    def when_task_delegated_to(self, data: dict[str, str]) -> None:
        self.__projection.delegate_to(data["task_id"], data["person_id"])

    def when_task_assigned_to(self, data: dict[str, str]) -> None:
        self.__projection.assign_to(data["task_id"], data["project_id"])

    def when_task_scheduled(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.SCHEDULED)

    def when_task_actionable(self, data: dict[str, str]) -> None:
        self.__projection.update_state(data["task_id"], TaskStates.ACTIONABLE)
