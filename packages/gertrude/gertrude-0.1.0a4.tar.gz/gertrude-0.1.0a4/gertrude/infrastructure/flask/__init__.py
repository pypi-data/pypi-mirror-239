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
import sys

from flask import Flask, g, get_flashed_messages, request, url_for
from flask_cors import CORS

from gertrude.infrastructure.flask import services
from gertrude.infrastructure.flask.aliases import blueprint as aliases
from gertrude.infrastructure.flask.auth import blueprint as auth
from gertrude.infrastructure.flask.projects import blueprint as projects
from gertrude.infrastructure.flask.tasks import blueprint as tasks
from gertrude.infrastructure.settings import WsgiSettings
from gertrude.interfaces import l10n
from gertrude.interfaces.to_http.as_html import register_jinja_global


def build_app(settings: WsgiSettings) -> Flask:
    services.define_settings(settings)

    configure_logging()

    app = Flask(
        __name__,
        static_folder="./static/",
        static_url_path="/resources",
        template_folder="./templates/",
    )

    CORS(app)
    app.config.update(
        SECRET_KEY=settings.SECRET_KEY,
        DSN=settings.DSN,
        DEBUG_SQL=settings.DEBUG_SQL,
        # SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    app.register_blueprint(aliases, url_prefix="/")
    app.register_blueprint(tasks, url_prefix="/tasks")
    app.register_blueprint(projects, url_prefix="/projects")

    app.auth_links = []  # type: ignore[attr-defined]
    app.register_blueprint(auth, url_prefix="/auth")

    if settings.AUTHORIZED_IP:
        from gertrude.infrastructure.flask.ip import blueprint as ip

        app.register_blueprint(ip, url_prefix="/auth/ip")
        app.auth_links.append(  # type: ignore[attr-defined]
            {"route": "ip.login", "label": "IP"}
        )

    app.teardown_appcontext(services.close_sessions)

    @app.before_request
    def guess_locale() -> None:
        g.locale = (
            request.accept_languages.best_match(l10n.LOCALES) or l10n.DEFAULT_LOCALE
        )

    register_jinja_global("url_for", url_for)
    register_jinja_global("locales", l10n.LOCALES)
    register_jinja_global("get_flashed_messages", get_flashed_messages)

    @app.before_request
    def set_current_url() -> None:
        register_jinja_global("current_url", request.path)

    return app


def configure_logging() -> None:
    default = logging.getLogger("default")
    default.setLevel(logging.CRITICAL)
    default.addHandler(logging.StreamHandler(sys.stderr))

    werkzeug = logging.getLogger("werkzeug")
    werkzeug.setLevel(logging.INFO)
    werkzeug.addHandler(logging.StreamHandler(sys.stdout))
