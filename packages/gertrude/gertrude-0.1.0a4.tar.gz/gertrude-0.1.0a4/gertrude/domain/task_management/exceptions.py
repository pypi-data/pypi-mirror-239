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


from .enums import TaskStates


class TaskNotFound(Exception):
    pass


class TransitionNotAllowed(Exception):
    def __init__(self, current: TaskStates, next: TaskStates) -> None:
        super().__init__(
            f'It\'s not allowed to transition from state "{current.name}" to '
            f'state "{next.name}".'
        )
        self.current = current
        self.next = next
