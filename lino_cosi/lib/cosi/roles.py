# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
# License: BSD (see file COPYING for details)

# Note that some roles are not needed *here*, but may be needed by
# code which imports * from here.

from lino.core.roles import Anonymous, SiteAdmin

from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino.modlib.accounts.roles import AccountingReader


class SiteUser(OfficeUser, AccountingReader):
    pass


class SiteAdmin(SiteAdmin, OfficeStaff, AccountingReader):
    pass

