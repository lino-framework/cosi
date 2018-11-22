# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""Defines a default set of user types and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

"""

from lino.api import _
from lino.modlib.users.choicelists import UserTypes
from lino.core.roles import UserRole, SiteAdmin
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.products.roles import ProductsUser, ProductsStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from lino_xl.lib.courses.roles import CoursesUser


class SiteUser(CoursesUser, ContactsUser, OfficeUser, LedgerUser,
               SepaUser, ExcerptsUser, ProductsUser):
    pass


class SiteAdmin(SiteAdmin, ContactsStaff, OfficeStaff, CoursesUser,
                LedgerStaff, SepaStaff, ExcerptsStaff, ProductsStaff):
    pass

UserTypes.clear()

add = UserTypes.add_item

add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("User"),           SiteUser)
add('900', _("Administrator"),  SiteAdmin, name='admin')

