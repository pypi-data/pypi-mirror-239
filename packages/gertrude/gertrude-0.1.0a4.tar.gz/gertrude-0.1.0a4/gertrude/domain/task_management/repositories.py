# Gertrude --- GTD done right
# Copyright © 2022 Tanguy Le Carrour <tanguy@bioneland.org>
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

import uuid

from bles import History

from . import events
from .entities import Task, User
from .exceptions import TaskNotFound
from .value_objects import TaskId, UserId


class DomainHistory(History):
    EVENT_MODULE = events


class Tasks:
    def __init__(self, history: DomainHistory) -> None:
        self.__history = history

    def load(self, identifier: TaskId) -> Task:
        events = self.__history.read(str(identifier))
        if not events:
            raise TaskNotFound(str(identifier))
        return Task.instanciate(events)  # type: ignore[arg-type]

    def next_id(self) -> TaskId:
        return TaskId.instanciate(str(uuid.uuid4()))


class Users:
    def load(self, identifier: UserId) -> User:
        return User(identifier)

    def next_id(self) -> UserId:
        return UserId.instanciate(str(uuid.uuid4()))
