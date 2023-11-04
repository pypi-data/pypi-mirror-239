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

from abc import ABC, abstractmethod
from http import HTTPStatus as HTTP


class HttpPresenter(ABC):
    @abstractmethod
    def status_code(self) -> int:
        ...

    @abstractmethod
    def headers(self) -> dict[str, str]:
        ...

    @abstractmethod
    def data(self) -> str:
        ...


class Redirection(HttpPresenter):
    def __init__(self, cible: str, code_statut: HTTP = HTTP.SEE_OTHER) -> None:
        self.__cible = cible
        self.__code_statut = code_statut

    def status_code(self) -> int:
        return self.__code_statut

    def headers(self) -> dict[str, str]:
        return {"Location": self.__cible}

    def data(self) -> str:
        return ""
