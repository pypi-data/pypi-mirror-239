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
from dataclasses import dataclass
from typing import Any, Optional

from bl3d import DomainEvent, Entity, EntityState
from typing_extensions import Self  # Required before Python 3.11

from .enums import TaskStates
from .events import (
    TaskActionable,
    TaskAssignedTo,
    TaskCaptured,
    TaskDelegatedTo,
    TaskDone,
    TaskEliminated,
    TaskEvent,
    TaskFiled,
    TaskIncubated,
    TaskScheduled,
)
from .exceptions import TransitionNotAllowed
from .value_objects import PersonId, ProjectId, TaskId, UserId

POSSIBLE_NEXT_STATES_OF_TASK = {
    TaskStates.CAPTURED: (
        TaskStates.ELIMINATED,
        TaskStates.FILED,
        TaskStates.INCUBATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.INCUBATED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.ACTIONABLE: (
        TaskStates.ELIMINATED,
        TaskStates.INCUBATED,
        TaskStates.DONE,
        TaskStates.DELEGATED,
        TaskStates.SCHEDULED,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.DELEGATED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.ACTIONABLE,
    ),
    TaskStates.SCHEDULED: (
        TaskStates.ELIMINATED,
        TaskStates.DONE,
        TaskStates.SCHEDULED,
    ),
}


@dataclass(frozen=True)
class TaskState(EntityState):
    id: TaskId
    state: TaskStates
    title: str
    description: str
    assigned_to: Optional[ProjectId] = None
    delegated_to: Optional[PersonId] = None

    def apply(self, event: DomainEvent) -> Self:
        # To make MyPy stop complaining about all `apply` calls.
        return super().apply(event)  # type: ignore

    def apply_task_captured(self, event: TaskCaptured) -> Self:
        return self.__create_new_state_with(
            task_id=TaskId(event.task_id),
            title=event.title,
            description=event.description or "",
            state=TaskStates.CAPTURED,
        )

    def apply_task_eliminated(self, event: TaskEliminated) -> Self:
        return self.__create_new_state_with(state=TaskStates.ELIMINATED)

    def apply_task_filed(self, event: TaskFiled) -> Self:
        return self.__create_new_state_with(state=TaskStates.FILED)

    def apply_task_incubated(self, event: TaskIncubated) -> Self:
        return self.__create_new_state_with(state=TaskStates.INCUBATED)

    def apply_task_done(self, event: TaskDone) -> Self:
        return self.__create_new_state_with(state=TaskStates.DONE)

    def apply_task_delegated_to(self, event: TaskDelegatedTo) -> Self:
        return self.__create_new_state_with(
            state=TaskStates.DELEGATED, delegated_to=PersonId(event.person_id)
        )

    def apply_task_scheduled(self, event: TaskScheduled) -> Self:
        return self.__create_new_state_with(state=TaskStates.SCHEDULED)

    def apply_task_actionable(self, event: TaskActionable) -> Self:
        return self.__create_new_state_with(state=TaskStates.ACTIONABLE)

    def apply_task_assigned_to(self, event: TaskAssignedTo) -> Self:
        # FIXME this is not a transition!
        if self.state == TaskStates.ELIMINATED:
            raise TransitionNotAllowed(self.state, self.state)
        return self.__create_new_state_with(assigned_to=ProjectId(event.project_id))

    def __create_new_state_with(self, **kwargs: Any) -> Self:
        if "state" in kwargs:
            self.__check_transition(kwargs["state"])

        return TaskState(  # type: ignore[return-value]
            self.version + 1,
            kwargs.get("task_id", self.id),
            kwargs.get("state", self.state),
            kwargs.get("title", self.title),
            kwargs.get("description", self.description),
            kwargs.get("assigned_to", self.assigned_to),
            kwargs.get("delegated_to", self.delegated_to),
        )

    def __check_transition(self, state: TaskStates) -> None:
        if self.state not in POSSIBLE_NEXT_STATES_OF_TASK:
            raise TransitionNotAllowed(self.state, state)
        if state not in POSSIBLE_NEXT_STATES_OF_TASK[self.state]:
            raise TransitionNotAllowed(self.state, state)


class Task(Entity):
    __state: TaskState

    @classmethod
    def instanciate(cls, events: list[TaskEvent]) -> Self:
        assert events
        captured = events[0]
        assert captured.version == 0
        assert isinstance(captured, TaskCaptured)

        state = TaskState(
            1,
            TaskId(captured.task_id),
            TaskStates.CAPTURED,
            captured.title,
            captured.description or "",
        )
        for e in events[1:]:
            state = state.apply(e)

        return cls(state)

    def __init__(self, state: TaskState) -> None:
        self.__state = state

    def eliminate(self) -> list[DomainEvent]:
        event = TaskEliminated(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def file(self) -> list[DomainEvent]:
        event = TaskFiled(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def incubate(self) -> list[DomainEvent]:
        event = TaskIncubated(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def do(self) -> list[DomainEvent]:
        event = TaskDone(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def delegate_to(self, delegated_to: PersonId) -> list[DomainEvent]:
        event = TaskDelegatedTo(
            self.__state.version, str(self.__state.id), str(delegated_to)
        )
        self.__state = self.__state.apply(event)
        return [event]

    def schedule_for(self, a_date: datetime.date) -> list[DomainEvent]:
        event = TaskScheduled(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def mark_as_actionable(self) -> list[DomainEvent]:
        event = TaskActionable(self.__state.version, str(self.__state.id))
        self.__state = self.__state.apply(event)
        return [event]

    def assign_to(self, assigned_to: ProjectId) -> list[DomainEvent]:
        events: list[DomainEvent] = []

        event: DomainEvent = TaskAssignedTo(
            self.__state.version, str(self.__state.id), str(assigned_to)
        )
        self.__state = self.__state.apply(event)
        events.append(event)

        # If it's assigned to a project, it means the project already
        # exists and contains tasks, so chances are this newly captured task
        # is not the very next thing to be done.
        if self.__state.state == TaskStates.CAPTURED:
            event = TaskIncubated(self.__state.version, str(self.__state.id))
            self.__state = self.__state.apply(event)
            events.append(event)

        return events


class User:
    def __init__(self, identifier: UserId) -> None:
        self.__identifier = identifier
