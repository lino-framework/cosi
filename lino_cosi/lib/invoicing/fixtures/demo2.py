# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

"""Creates an invoicing plan and executes the first ten items
(i.e. generates ten invoices).

"""

from lino.api import dd, rt


def objects():
    vt = dd.plugins.invoicing.get_voucher_type()
    jnl_list = vt.get_journals()
    if len(jnl_list) == 0:
        return
    from lino_cosi.lib.ledger.roles import LedgerStaff
    accountants = LedgerStaff.get_user_profiles()
    users = rt.modules.users.User.objects.filter(
        language=dd.get_default_language(), profile__in=accountants)
    if users.count() == 0:
        return
    ses = rt.login(users[0].username)
    Plan = rt.modules.invoicing.Plan
    plan = Plan.start_plan(ses.get_user(), journal=jnl_list[0])
    yield plan
    plan.fill_plan(ses)
    for i in plan.items.all()[:9]:
        obj = i.create_invoice(ses)
        assert obj is not None
        yield obj
