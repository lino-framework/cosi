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

"""
Actions for `lino_cosi.lib.invoicing`.

"""


from __future__ import unicode_literals

from lino.api import dd, rt, _


class StartInvoicing(dd.Action):
    icon_name = 'basket'
    sort_index = 52
    label = _("Create invoices")

    def run_from_ui(self, ar, **kw):
        jnl = ar.master_instance
        assert isinstance(jnl, rt.modules.ledger.Journal)
        Plan = rt.modules.invoicing.Plan
        # Item = rt.modules.invoicing.Item
        plan, created = Plan.objects.get_or_create(
            user=ar.get_user(), journal=jnl)
        if created:
            plan.save()
        # else:
        #     plan.items.delete()
        ar.goto_instance(plan)


class UpdatePlan(dd.Action):
    icon_name = 'lightning'
    help_text = _("Build a new list of suggestions. "
                  "This will remove all current suggestions")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        plan.fill_plan(ar)
        ar.success(refresh=True)


class ExecutePlan(dd.Action):
    icon_name = 'money'

    help_text = _("Execute this invoicing plan. "
                  "Create an invoice for each selected suggestion.")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.filter(selected=True, invoice__isnull=True):
            item.create_invoice(ar)
        ar.success(refresh=True)


class ToggleSelection(dd.Action):
    label = _("Toggle selections")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.all():
            item.selected = not item.selected
            item.save()
        ar.success(refresh=True)

