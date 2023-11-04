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

import datetime
from typing import Any, Optional

from blessql import EventStore
from flask import g
from flask import session as flask_session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from gertrude.domain.task_management.repositories import DomainHistory, Tasks, Users
from gertrude.infrastructure.settings import WsgiSettings
from gertrude.infrastructure.sqlalchemy.projections import Tasks as TaskProjection
from gertrude.infrastructure.sqlalchemy.repositories import Projects

__SETTINGS: Optional[WsgiSettings] = None


def define_settings(settings: WsgiSettings) -> None:
    global __SETTINGS
    __SETTINGS = settings


def get_settings() -> WsgiSettings:
    if not __SETTINGS:
        raise RuntimeError("You must define the settings!")
    return __SETTINGS


def session() -> Session:
    # To share a session between repositories (Unit of Work pattern)
    # session should be attach to `g` and passed to repositories.
    s = get_settings()

    if "session" not in g:
        options: dict[str, Any] = {}
        if s.DEBUG_SQL:
            options["echo"] = True
            options["echo_pool"] = "debug"

        engine = create_engine(s.DSN, **options)
        g.setdefault("session", sessionmaker(bind=engine)())

    return g.session


def close_sessions(exception: Optional[BaseException]) -> None:
    if session := g.pop("session", None):
        if exception:
            session.rollback()
        else:
            session.commit()
        session.close()


def users() -> Users:
    if "users" not in g:
        g.users = Users()
    return g.users  # type: ignore[no-any-return]


def history() -> DomainHistory:
    if "history" not in g:
        g.history = DomainHistory(EventStore(session()), lambda: datetime.datetime.now())
    return g.history  # type: ignore[no-any-return]


def tasks() -> Tasks:
    if "tasks" not in g:
        g.tasks = Tasks(history())
    return g.tasks  # type: ignore[no-any-return]


def task_projection() -> TaskProjection:
    if "task_projection" not in g:
        g.task_projection = TaskProjection(session())
    return g.task_projection  # type: ignore[no-any-return]


def projects() -> Projects:
    if "projects" not in g:
        g.projects = Projects(session())
    return g.projects  # type: ignore[no-any-return]


def user_id() -> str:
    return str(flask_session.get("user_id", ""))
