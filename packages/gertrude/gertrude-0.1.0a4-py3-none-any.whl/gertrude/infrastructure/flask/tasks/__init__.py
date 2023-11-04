# Gertrude --- GTD done right
# Copyright © 2022, 2023 Tanguy Le Carrour <tanguy@bioneland.org>
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

from typing import Any
from uuid import UUID

from flask import Blueprint, request

from gertrude.application.use_cases import (
    assign_task,
    capture_task,
    delegate_task,
    do_task,
    eliminate_task,
    file_task,
    incubate_task,
    postpone_task,
    schedule_task,
)
from gertrude.domain.task_management.enums import TaskStates
from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.utils import (
    auth_required,
    htmx,
    notify,
    presenter_to_response,
)
from gertrude.interfaces import from_base_types as controllers
from gertrude.interfaces.to_http import as_html as presenters

blueprint = Blueprint("tasks", __name__)


@blueprint.get("")
@presenter_to_response
def index() -> Any:
    return presenters.PugPresenter("tasks/index")


@blueprint.get("/__new__")
@presenter_to_response
@auth_required
def capture() -> Any:
    return presenters.CaptureTaskForm(services.projects().list(), fragment=htmx.target)


@blueprint.post("/__new__")
@presenter_to_response
@auth_required
def capture_POST() -> Any:
    presenter = presenters.CaptureTask(
        request.form, services.projects().list(), fragment=htmx.target
    )
    interactor = capture_task.Interactor(
        presenter, services.history(), services.tasks(), services.users()
    )
    controller = controllers.CaptureTask(services.user_id(), request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/inbox")
@presenter_to_response
@auth_required
def inbox() -> Any:
    return presenters.ListTasksInbox(
        services.task_projection().list(state=TaskStates.CAPTURED), fragment=htmx.target
    )


@blueprint.get("/organize")
@presenter_to_response
@auth_required
def organize() -> Any:
    return presenters.ListTasksOrganize(services.task_projection().list())


@blueprint.get("/next")
@presenter_to_response
@auth_required
def next() -> Any:
    return presenters.ListTasksNext(
        services.task_projection().list(state=TaskStates.ACTIONABLE),
        fragment=htmx.target,
    )


@blueprint.get("/waiting")
@presenter_to_response
@auth_required
def waiting() -> Any:
    return presenters.ListTasksWaiting(
        services.task_projection().list(state=TaskStates.DELEGATED)
    )


@blueprint.get("/scheduled")
@presenter_to_response
@auth_required
def scheduled() -> Any:
    return presenters.ListTasksScheduled(
        services.task_projection().list(state=TaskStates.SCHEDULED)
    )


@blueprint.get("/someday")
@presenter_to_response
@auth_required
def someday() -> Any:
    return presenters.ListTasksSomeday(
        services.task_projection().list(state=TaskStates.INCUBATED)
    )


@blueprint.get("/<uuid:id>")
@presenter_to_response
@auth_required
def display(id: UUID) -> Any:
    return presenters.PugPresenter(
        "tasks/display",
        task=services.task_projection().load(str(id)),
        projects_by_id={p.id: p for p in services.projects().list()},
        fragment=htmx.target,
    )


@blueprint.post("/<uuid:id>/__do__")
@presenter_to_response
@auth_required
def do(id: UUID) -> Any:
    presenter = presenters.DoTask(
        notify, services.task_projection().load(str(id)), fragment=htmx.target
    )
    interactor = do_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.DoTask(services.user_id(), str(id))
    controller.call(interactor)
    return presenter


@blueprint.post("/<uuid:id>/__incubate__")
@presenter_to_response
@auth_required
def incubate(id: UUID) -> Any:
    presenter = presenters.IncubateTask(notify, fragment=htmx.target)
    interactor = incubate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.IncubateTask(services.user_id(), str(id))
    controller.call(interactor)
    return presenter


@blueprint.post("/<uuid:id>/__file__")
@presenter_to_response
@auth_required
def file(id: UUID) -> Any:
    presenter = presenters.FileTask(notify, fragment=htmx.target)
    interactor = file_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.FileTask(services.user_id(), str(id))
    controller.call(interactor)
    return presenter


@blueprint.post("/<uuid:id>/__postpone__")
@presenter_to_response
@auth_required
def postpone(id: UUID) -> Any:
    presenter = presenters.PostponeTask(notify, fragment=htmx.target)
    interactor = postpone_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.PostponeTask(services.user_id(), str(id))
    controller.call(interactor)
    return presenter


@blueprint.post("/<uuid:id>/__eliminate__")
@presenter_to_response
@auth_required
def eliminate(id: UUID) -> Any:
    presenter = presenters.EliminateTask(notify, fragment=htmx.target)
    interactor = eliminate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.EliminateTask(services.user_id(), str(id))
    controller.call(interactor)
    return presenter


@blueprint.get("/<uuid:id>/__delegate__")
@presenter_to_response
@auth_required
def delegate_form(id: UUID) -> Any:
    return presenters.PugPresenter(
        "tasks/delegate",
        task=services.task_projection().load(str(id)),
        errors={},
        fragment=htmx.target,
    )


@blueprint.post("/<uuid:id>/__delegate__")
@presenter_to_response
@auth_required
def delegate(id: UUID) -> Any:
    presenter = presenters.DelegateTask(request.form, notify, fragment=htmx.target)
    interactor = delegate_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.DelegateTask(services.user_id(), str(id), request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/<uuid:id>/__assign__")
@presenter_to_response
@auth_required
def assign_form(id: UUID) -> Any:
    return presenters.PugPresenter(
        "tasks/assign",
        task=services.task_projection().load(str(id)),
        projects=services.projects().list(),
        errors={},
        fragment=htmx.target,
    )


@blueprint.post("/<uuid:id>/__assign__")
@presenter_to_response
@auth_required
def assign(id: UUID) -> Any:
    presenter = presenters.AssignTask(
        request.form, services.projects().list(), notify, fragment=htmx.target
    )
    interactor = assign_task.Interactor(presenter, services.history(), services.tasks())
    controller = controllers.AssignTask(services.user_id(), str(id), request.form)
    controller.call(interactor)
    return presenter


@blueprint.get("/<uuid:id>/__schedule__")
@presenter_to_response
@auth_required
def schedule_form(id: UUID) -> Any:
    return presenters.PugPresenter(
        "tasks/schedule",
        task=services.task_projection().load(str(id)),
        errors={},
        fragment=htmx.target,
    )


@blueprint.post("/<uuid:id>/__schedule__")
@presenter_to_response
@auth_required
def schedule(id: UUID) -> Any:
    presenter = presenters.ScheduleTask(request.form, notify, fragment=htmx.target)
    interactor = schedule_task.Interactor(
        presenter, services.history(), services.tasks()
    )
    controller = controllers.ScheduleTask(services.user_id(), str(id), request.form)
    controller.call(interactor)
    return presenter
