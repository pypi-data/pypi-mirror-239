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

import datetime
from typing import Any, Optional

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    create_project,
    delegate_task,
    display_project,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    list_tasks,
    postpone_task,
    schedule_task,
)


class ListTasks:
    def __init__(self, user_id: str, params: dict[str, str]) -> None:
        self.__request = list_tasks.Request(user_id)

    def call(self, interactor: list_tasks.Interactor) -> None:
        interactor.execute(self.__request)


class CaptureTask:
    def __init__(self, user_id: str, params: dict[str, str]) -> None:
        self.__request = capture_task.Request(
            user_id,
            params.get("id", ""),
            params.get("title", ""),
            description=params.get("description", ""),
            project_id=params.get("project_id", ""),
        )

    def call(self, interactor: capture_task.Interactor) -> None:
        interactor.execute(self.__request)


class EliminateTask:
    def __init__(self, a_user_id: str, a_task_id: str) -> None:
        self.__request = eliminate_task.Request(a_user_id, a_task_id)

    def call(self, interactor: eliminate_task.Interactor) -> None:
        interactor.execute(self.__request)


class IncubateTask:
    def __init__(self, a_user_id: str, a_task_id: str) -> None:
        self.__request = incubate_task.Request(a_user_id, a_task_id)

    def call(self, interactor: incubate_task.Interactor) -> None:
        interactor.execute(self.__request)


class FileTask:
    def __init__(self, a_user_id: str, a_task_id: str) -> None:
        self.__request = file_task.Request(a_user_id, a_task_id)

    def call(self, interactor: file_task.Interactor) -> None:
        interactor.execute(self.__request)


class DoTask:
    def __init__(self, a_user_id: str, a_task_id: str) -> None:
        self.__request = do_task.Request(a_user_id, a_task_id)

    def call(self, interactor: do_task.Interactor) -> None:
        interactor.execute(self.__request)


class PostponeTask:
    def __init__(self, a_user_id: str, a_task_id: str) -> None:
        self.__request = postpone_task.Request(a_user_id, a_task_id)

    def call(self, interactor: postpone_task.Interactor) -> None:
        interactor.execute(self.__request)


class ScheduleTask:
    def __init__(self, a_user_id: str, a_task_id: str, params: dict[str, str]) -> None:
        # FIXME format depends on the browser?!
        date_format = "%Y-%m-%d"
        date: Optional[datetime.date] = None
        try:
            date = datetime.datetime.strptime(
                params.get("scheduled_on", ""), date_format
            ).date()
        except ValueError:
            pass

        self.__request = schedule_task.Request(a_user_id, a_task_id, date=date)

    def call(self, interactor: schedule_task.Interactor) -> None:
        interactor.execute(self.__request)


class AssignTask:
    def __init__(self, a_user_id: str, a_task_id: str, params: dict[str, str]) -> None:
        self.__request = assign_task.Request(
            a_user_id, a_task_id, params.get("assigned_to", "")
        )

    def call(self, interactor: assign_task.Interactor) -> None:
        interactor.execute(self.__request)


class DelegateTask:
    def __init__(self, a_user_id: str, a_task_id: str, params: dict[str, str]) -> None:
        self.__request = delegate_task.Request(
            a_user_id, a_task_id, params.get("delegated_to", "")
        )

    def call(self, interactor: delegate_task.Interactor) -> None:
        interactor.execute(self.__request)


class CreateProject:
    def __init__(self, data: dict[str, Any]) -> None:
        self.__request = create_project.Request(
            data.get("id", ""), name=data.get("name", "")
        )

    def call(self, interactor: create_project.Interactor) -> None:
        interactor.execute(self.__request)


class DisplayProject:
    def __init__(self, a_project_id: str) -> None:
        self.__request = display_project.Request(id=a_project_id)

    def call(self, interactor: display_project.Interactor) -> None:
        interactor.execute(self.__request)
