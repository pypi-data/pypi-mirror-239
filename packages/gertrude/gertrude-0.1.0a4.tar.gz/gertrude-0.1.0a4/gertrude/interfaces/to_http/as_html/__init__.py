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

import logging
import uuid
from abc import ABC
from http import HTTPStatus as HTTP
from importlib.metadata import version
from pathlib import Path
from typing import Any, Callable, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from jinja2_fragments import render_block

from gertrude import __name__ as PACKAGE_NAME
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
    list_projects,
    postpone_task,
    schedule_task,
)
from gertrude.domain.project_management.entities import Project
from gertrude.domain.task_management.dto import Task
from gertrude.domain.task_management.enums import TaskStates
from gertrude.interfaces import l10n
from gertrude.interfaces.to_http import HttpPresenter

ENVIRONMENT = Environment(
    loader=FileSystemLoader([Path(__file__).parent / "templates"]),
    autoescape=select_autoescape(),
    extensions=["pypugjs.ext.jinja.PyPugJSExtension"],
)
ENVIRONMENT.globals.update({"version": version(PACKAGE_NAME)})


def register_jinja_global(key: str, value: Any) -> None:
    ENVIRONMENT.globals[key] = value


def url_for(*args: Any, **kwargs: Any) -> str:
    if function := ENVIRONMENT.globals.get("url_for"):
        return function(*args, **kwargs)  # type: ignore
    raise RuntimeError("`url_for` is not declared on the environment!")


class JinjaPresenter(HttpPresenter):
    def __init__(self, template: str, fragment: str = "", **context: Any) -> None:
        self.__status_code = HTTP.OK
        self.__headers = {
            "Content-Type": "text/html; charset=UTF-8",
        }
        self.__template = template
        self.__context = context
        self.__fragment = fragment
        self._ = l10n.translator_for("en-GB")

    def status_code(self) -> int:
        return self.__status_code

    def headers(self) -> dict[str, str]:
        return self.__headers

    def data(self) -> str:
        return self.render(**self.__context)

    def render(self, **context: Any) -> str:
        if not self.__template:
            return ""

        ctx = {**self.__context, **context, "_": self._}
        if self.__fragment:
            return render_block(ENVIRONMENT, self.__template, self.__fragment, **ctx)
        return ENVIRONMENT.get_template(self.__template).render(**ctx)

    def render_error(self, message: str) -> str:
        return ENVIRONMENT.get_template("error.pug").render(error=message, _=self._)

    def set_status_code(self, status_code: HTTP) -> None:
        self.__status_code = status_code

    def add_header(self, key: str, value: str) -> None:
        self.__headers[key] = value

    def trigger(self, event: str) -> None:
        if event.startswith("Task"):
            self.add_header("HX-Trigger", f"{event}, TasksChanged")
        else:
            self.add_header("HX-Trigger", event)

    def disabled_rendering(self) -> None:
        self.__template = ""

    def redirect(self, url: str, status_code: HTTP = HTTP.SEE_OTHER) -> None:
        if self.__fragment:
            self.add_header("HX-Location", url)
        else:
            self.add_header("Location", url)
        self.set_status_code(status_code)


class PugPresenter(JinjaPresenter):
    def __init__(self, template: str, **context: Any) -> None:
        super().__init__(template + ".pug" if template else "", **context)


class ListTasks(PugPresenter, ABC):
    def __init__(
        self, template: str, tasks: list[Task], /, *, fragment: str = ""
    ) -> None:
        super().__init__(template, fragment=fragment)
        self.__context: dict[str, Any] = {"tasks": tasks}

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)


class ListTasksInbox(ListTasks):
    def __init__(self, tasks: list[Task], /, *, fragment: str = "") -> None:
        super().__init__("tasks/inbox", tasks, fragment=fragment)


class ListTasksOrganize(ListTasks):
    def __init__(self, tasks: list[Task]) -> None:
        super().__init__("tasks/organize", tasks)


class ListTasksNext(ListTasks):
    def __init__(self, tasks: list[Task], /, *, fragment: str = "") -> None:
        super().__init__("tasks/next", tasks, fragment=fragment)


class ListTasksScheduled(ListTasks):
    def __init__(self, tasks: list[Task]) -> None:
        super().__init__("tasks/scheduled", tasks)


class ListTasksSomeday(ListTasks):
    def __init__(self, tasks: list[Task]) -> None:
        super().__init__("tasks/someday", tasks)


class ListTasksWaiting(ListTasks):
    def __init__(self, tasks: list[Task]) -> None:
        super().__init__("tasks/waiting", tasks)


class CaptureTaskForm(PugPresenter):
    def __init__(self, projects: list[Project], /, *, fragment: str = "") -> None:
        super().__init__("tasks/capture", fragment=fragment)
        self.__context: dict[str, Any] = {
            "task": {"id": str(uuid.uuid4())},
            "projects": projects,
            "message": "",
            "errors": {},
        }

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)


class CaptureTask(PugPresenter, capture_task.Presenter):
    def __init__(
        self, data: dict[str, Any], projects: list[Project], /, *, fragment: str = ""
    ) -> None:
        super().__init__("tasks/capture", fragment=fragment)
        self.__context: dict[str, Any] = {
            "task": data,
            "projects": projects,
            "message": "",
            "errors": {},
        }
        self.__fragment = fragment

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)

    def error(self, attribute: str, message: str) -> None:
        self.__context["errors"][attribute] = message

    def missing_task_id(self) -> None:
        self.error("other", "Missing task ID!?")

    def incorrect_task_id(self) -> None:
        self.error("other", "Incorrect task ID!?")

    def task_id_already_used(self) -> None:
        self.error("other", "Task ID already exists!?")

    def incorrect_user_id(self) -> None:
        self.error("other", "Incorrect user ID!?")

    def incorrect_project_id(self, project_id: str) -> None:
        self.error("project_id", "Incorrect project ID!?")

    def missing_title(self) -> None:
        self.error("title", "You must provide a title.")

    def task_captured(self) -> None:
        if self.__fragment:
            self.trigger("TaskCaptured")
            self.disabled_rendering()
        else:
            self.redirect(url_for("tasks.inbox"))


class TaskPresenter(PugPresenter):
    def __init__(
        self,
        notifier: Callable[[str, str], None],
        template: str = "tasks/inbox",
        task: Optional[dict[str, Any]] = None,
        fragment: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(template, fragment=fragment)
        self.notify = notifier
        self.__context: dict[str, Any] = {**{"task": task or {}, "errors": {}}, **kwargs}

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)

    def error(self, attribute: str, message: str) -> None:
        self.__context["errors"][attribute] = message

    def missing_task_id(self) -> None:
        self.notify("Missing task ID!", "error")
        self.redirect(url_for("tasks.index"))

    def incorrect_task_id(self) -> None:
        self.notify("Incorrect task ID!", "error")
        self.redirect(url_for("tasks.index"))

    def task_not_found(self) -> None:
        self.notify("Task not found!", "error")
        self.redirect(url_for("tasks.index"))

    def transition_not_allowed(self, current: TaskStates, next: TaskStates) -> None:
        logging.debug(
            f"Transition not allowed! [current={current.name}, next={next.name}]"
        )
        self.notify("Transition not allowed!", "error")
        self.redirect(url_for("tasks.index"))


class DoTask(TaskPresenter, do_task.Presenter):
    def __init__(
        self,
        notifier: Callable[[str, str], None],
        task: Optional[Task] = None,
        /,
        *,
        fragment: str = "",
    ) -> None:
        super().__init__(notifier, "tasks/inbox")
        self.__task = task
        self.__fragment = fragment

    def task_done(self) -> None:
        if self.__fragment:
            self.trigger("TaskDone")
            self.disabled_rendering()
            if self.__task and self.__task.assigned_to:
                self.add_header(
                    "HX-Redirect",
                    url_for("projects.display", id=str(self.__task.assigned_to)),
                )
        else:
            self.notify("Task done!", "success")
            if self.__task and self.__task.assigned_to:
                self.redirect(
                    url_for("projects.display", id=str(self.__task.assigned_to))
                )
            else:
                self.redirect(url_for("tasks.inbox"))


class DelegateTask(TaskPresenter, delegate_task.Presenter):
    def __init__(
        self,
        data: dict[str, Any],
        notifier: Callable[[str, str], None],
        /,
        *,
        fragment: str = "",
    ) -> None:
        super().__init__(notifier, "tasks/delegate", data, fragment=fragment)
        self.__fragment = fragment

    def missing_person_id(self) -> None:
        self.error("delegated_to", "Missing person ID!")

    def incorrect_person_id(self) -> None:
        self.error("delegated_to", "Incorrect person ID!")

    def task_delegated(self) -> None:
        if self.__fragment:
            self.trigger("TaskDelegated")
            self.disabled_rendering()
        else:
            self.notify("Task delegated!", "success")
            self.redirect(url_for("tasks.inbox"))


class AssignTask(TaskPresenter, assign_task.Presenter):
    def __init__(
        self,
        data: dict[str, Any],
        projects: list[Project],
        notifier: Callable[[str, str], None],
        fragment: str = "",
    ) -> None:
        super().__init__(
            notifier, "tasks/assign", data, projects=projects, fragment=fragment
        )
        self.__fragment = fragment

    def missing_project_id(self) -> None:
        self.error("assigned_to", "Missing project ID!")

    def incorrect_project_id(self) -> None:
        self.error("assigned_to", "Incorrect project ID!")

    def task_assigned(self) -> None:
        if self.__fragment:
            self.trigger("TaskAssigned")
            self.disabled_rendering()
        else:
            self.notify("Task assigned!", "success")
            self.redirect(url_for("tasks.inbox"))


class ScheduleTask(TaskPresenter, schedule_task.Presenter):
    def __init__(
        self,
        data: dict[str, Any],
        notifier: Callable[[str, str], None],
        fragment: str = "",
    ) -> None:
        super().__init__(notifier, "tasks/schedule", data, fragment=fragment)
        self.__fragment = fragment

    def missing_date(self) -> None:
        self.error("scheduled_on", "Missing date!")

    def incorrect_person_id(self) -> None:
        self.error("scheduled_on", "Incorrect person ID!")

    def task_scheduled(self) -> None:
        if self.__fragment:
            self.trigger("TaskScheduled")
            self.disabled_rendering()
        else:
            self.notify("Task scheduled!", "success")
            self.redirect(url_for("tasks.inbox"))


class IncubateTask(TaskPresenter, incubate_task.Presenter):
    def __init__(
        self, notifier: Callable[[str, str], None], /, *, fragment: str = ""
    ) -> None:
        super().__init__(notifier, "tasks/inbox", fragment=fragment)
        self.__fragment = fragment

    def task_incubated(self) -> None:
        if self.__fragment:
            self.trigger("TaskIncubated")
            self.disabled_rendering()
        else:
            self.notify("Task incubate!", "success")
            self.redirect(url_for("tasks.inbox"))


class FileTask(TaskPresenter, file_task.Presenter):
    def __init__(
        self, notifier: Callable[[str, str], None], /, *, fragment: str = ""
    ) -> None:
        super().__init__(notifier, "tasks/inbox", fragment=fragment)
        self.__fragment = fragment

    def task_filed(self) -> None:
        if self.__fragment:
            self.trigger("TaskFiled")
            self.disabled_rendering()
        else:
            self.notify("Task filed!", "success")
            self.redirect(url_for("tasks.inbox"))


class PostponeTask(TaskPresenter, postpone_task.Presenter):
    def __init__(
        self, notifier: Callable[[str, str], None], /, *, fragment: str = ""
    ) -> None:
        super().__init__(notifier, "tasks/inbox", fragment=fragment)
        self.__fragment = fragment

    def task_postponed(self) -> None:
        if self.__fragment:
            self.trigger("TaskPostponed")
            self.disabled_rendering()
        else:
            self.notify("Task postponed!", "success")
            self.redirect(url_for("tasks.inbox"))


class EliminateTask(TaskPresenter, eliminate_task.Presenter):
    def __init__(
        self, notifier: Callable[[str, str], None], /, *, fragment: str = ""
    ) -> None:
        super().__init__(notifier, "tasks/inbox", fragment=fragment)
        self.__fragment = fragment

    def task_eliminated(self) -> None:
        if self.__fragment:
            self.trigger("TaskEliminated")
            self.disabled_rendering()
        else:
            self.notify("Task eliminated!", "success")
            self.redirect(url_for("tasks.inbox"))


class ListProjects(PugPresenter, list_projects.Presenter):
    def __init__(self) -> None:
        super().__init__("projects/list")
        self.__projects: list[dict[str, Any]] = []

    def projects(self, projects: list[Project]) -> None:
        self.set_status_code(HTTP.OK)
        for p in projects:
            self.__projects.append({"id": p.id, "name": p.name})

    def render(self, **context: Any) -> str:
        return super().render(projects=self.__projects, **context)


class CreateProjectForm(PugPresenter):
    def __init__(self) -> None:
        super().__init__("projects/create")
        self.__context: dict[str, Any] = {
            "project": {"id": str(uuid.uuid4())},
            "errors": {},
        }

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)


class CreateProject(PugPresenter, create_project.Presenter):
    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__("projects/create")
        self.__context: dict[str, Any] = {"project": data, "errors": {}}
        self.__redirect_url = url_for("projects.list")

    def render(self, **context: Any) -> str:
        return super().render(**self.__context, **context)

    def __error(self, status_code: HTTP, message: str) -> None:
        self.set_status_code(status_code)
        self.__context["errors"]["name"] = message

    def missing_id(self) -> None:
        self.__error(HTTP.BAD_REQUEST, "You must provide an ID!")

    def missing_name(self) -> None:
        self.__error(HTTP.BAD_REQUEST, "You must provide a name!")

    def project_already_exists(self) -> None:
        self.__error(HTTP.BAD_REQUEST, "This ID is already used by another project!")

    def project_created(self) -> None:
        self.redirect(self.__redirect_url)


class DisplayProject(PugPresenter, display_project.Presenter):
    def __init__(self, /, *, fragment: str = "") -> None:
        super().__init__("projects/display", fragment=fragment)
        self.__project: Optional[Project] = None
        self.__error = ""
        self.__tasks: list[Task] = []

    def render(self, **context: Any) -> str:
        if self.__error:
            return self.render_error(self.__error)

        actionable_tasks = [
            t for t in self.__tasks if t.state == TaskStates.ACTIONABLE.value
        ]
        incubated_tasks = [
            t for t in self.__tasks if t.state == TaskStates.INCUBATED.value
        ]
        done_tasks = [t for t in self.__tasks if t.state == TaskStates.DONE.value]
        tasks = actionable_tasks + incubated_tasks

        return super().render(
            project=self.__project,
            tasks=tasks,
            actionable_tasks=actionable_tasks,
            incubated_tasks=incubated_tasks,
            done_tasks=done_tasks,
            **context,
        )

    def project_not_found(self, an_id: str) -> None:
        self.set_status_code(HTTP.NOT_FOUND)
        self.__error = "The project your are looking for does not exist!"

    def project(self, a_project: Project) -> None:
        self.set_status_code(HTTP.OK)
        self.__project = a_project

    def task(self, task: Task) -> None:
        self.__tasks.append(task)
