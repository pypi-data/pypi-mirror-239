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

from typing import Optional

from bl3d import DomainEvent

from .events import TaskCaptured
from .value_objects import TaskId, UserId


def capture_task(
    identifier: TaskId, user: UserId, title: str, description: Optional[str] = ""
) -> list[DomainEvent]:
    return [TaskCaptured(0, str(identifier), str(user), title, description)]
