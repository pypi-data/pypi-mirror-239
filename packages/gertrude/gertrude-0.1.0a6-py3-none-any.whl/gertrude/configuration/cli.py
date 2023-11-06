# Gertrude --- GTD done right
# Copyright © 2020-2022 Tanguy Le Carrour <tanguy@bioneland.org>
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

import os
import sys

import click


def cli() -> click.Group:
    from gertrude.infrastructure.click import build

    return build(read_dsn_from_env())


def read_dsn_from_env() -> str:
    var = "GERTRUDE_DSN"
    if var not in os.environ:
        print("Please set the ENV variable '{}'".format(var))
        sys.exit(1)
    return os.environ[var]
