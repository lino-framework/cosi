# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Defines a default set of user roles and fills
:class:`lino.modlib.users.choicelists.UserProfiles`.

"""

from lino.api import _
from lino.modlib.users.choicelists import UserProfiles
from lino.core.roles import UserRole, SiteAdmin
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.ledger.roles import LedgerUser, LedgerStaff


class SiteUser(OfficeUser, LedgerUser):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, LedgerStaff):
    pass

UserProfiles.clear()

add = UserProfiles.add_item

add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"),           SiteUser)
add('900', _("Administrator"),  SiteAdmin, name='admin')

