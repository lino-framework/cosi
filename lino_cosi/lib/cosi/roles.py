# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# This file is part of Lino Cosi.
#
# Lino Cosi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Cosi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Cosi.  If not, see
# <http://www.gnu.org/licenses/>.


"""Defines a default set of user roles and fills
:class:`lino.modlib.users.choicelists.UserProfiles`.

"""

from lino.api import _
from lino.modlib.users.choicelists import UserProfiles
from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_cosi.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_cosi.lib.sepa.roles import SepaUser, SepaStaff


class SiteUser(OfficeUser, LedgerUser, SepaUser):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, LedgerStaff, SepaStaff):
    pass

UserProfiles.clear()

add = UserProfiles.add_item

add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"),           SiteUser)
add('900', _("Administrator"),  SiteAdmin, name='admin')

