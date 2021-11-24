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

from .base import Command, Hello, Login, Logout, Request
from .check import CheckContact, CheckDomain, CheckKeyset, CheckNsset
from .create import CreateContact, CreateDomain, CreateKeyset, CreateNsset
from .delete import DeleteContact, DeleteDomain, DeleteKeyset, DeleteNsset
from .extensions import (CreditInfoRequest, SendAuthInfoContact, SendAuthInfoDomain, SendAuthInfoKeyset,
                         SendAuthInfoNsset, TestNsset)
from .info import InfoContact, InfoDomain, InfoKeyset, InfoNsset
from .renew import RenewDomain
from .transfer import TransferContact, TransferDomain, TransferKeyset, TransferNsset
from .update import UpdateContact, UpdateDomain, UpdateKeyset

__all__ = [
    'CheckContact',
    'CheckDomain',
    'CheckKeyset',
    'CheckNsset',
    'Command',
    'CreateContact',
    'CreateDomain',
    'CreateKeyset',
    'CreateNsset',
    'CreditInfoRequest',
    'DeleteContact',
    'DeleteDomain',
    'DeleteKeyset',
    'DeleteNsset',
    'Hello',
    'InfoContact',
    'InfoDomain',
    'InfoKeyset',
    'InfoNsset',
    'Login',
    'Logout',
    'RenewDomain',
    'Request',
    'SendAuthInfoContact',
    'SendAuthInfoDomain',
    'SendAuthInfoKeyset',
    'SendAuthInfoNsset',
    'TestNsset',
    'TransferContact',
    'TransferDomain',
    'TransferKeyset',
    'TransferNsset',
    'UpdateContact',
    'UpdateDomain',
    'UpdateKeyset',
]
