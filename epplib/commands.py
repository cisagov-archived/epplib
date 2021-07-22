#
# Copyright (C) 2021  CZ.NIC, z. s. p. o.
#
# This file is part of FRED.
#
# FRED is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FRED is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with FRED.  If not, see <https://www.gnu.org/licenses/>.

"""Module providing EPP commands."""
from abc import ABC, abstractmethod, abstractproperty
from typing import Type

from lxml.etree import Element, ElementTree, tostring  # nosec - TODO: Fix lxml security issues

from epplib.constants import NAMESPACE_EPP, NAMESPACE_XSI, XSI_SCHEMA_LOCATION
from epplib.responses import Response


class Request(ABC):
    """Base class for EPP requests."""

    def xml(self) -> bytes:
        """Return xml representation of the Request."""
        root = Element('epp')
        root.set('xmlns', NAMESPACE_EPP)
        root.set('{{{}}}schemaLocation'.format(NAMESPACE_XSI), XSI_SCHEMA_LOCATION)
        root.append(self._get_payload())

        document = ElementTree(root)
        return tostring(document, encoding='utf-8', xml_declaration=True)

    @abstractmethod
    def _get_payload(self) -> Element:
        """Get subelements of the epp tag specific for the given Request subclass."""

    @abstractproperty
    def response_class(self) -> Type[Response]:
        """Class of the corresponding response."""
