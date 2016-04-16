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
    """Base for :class:`StartInvoicingForJournal`,
    :class:`StartInvoicingForPartner`.

    """
    icon_name = 'basket'
    sort_index = 52
    label = _("Create invoices")
    select_rows = False
    http_method = 'POST'

    def get_options(self, ar):
        return {}

    def run_from_ui(self, ar, **kw):
        options = self.get_options(ar)
        plan = rt.modules.invoicing.Plan.start_plan(ar.get_user(), **options)
        ar.goto_instance(plan)


class StartInvoicingForJournal(StartInvoicing):
    """Start an invoicing plan for this journal.

    This is installed onto the VouchersByJournal table of the
    VoucherType for the configured
    :attr:`voucher_model<lino_cosi.lib.invoicing.Plugin.voucher_model>`
    as `start_invoicing`.

    """

    def get_options(self, ar):
        jnl = ar.master_instance
        assert isinstance(jnl, rt.modules.ledger.Journal)
        return dict(journal=jnl)


class StartInvoicingForPartner(StartInvoicing):
    """Start an invoicing plan for this partner.

    This is installed onto the :class:`contacts.Partner
    <lino.modlib.contacts.models.Partner>` model as `start_invoicing`.

    """
    select_rows = True

    def get_options(self, ar):
        partner = ar.selected_rows[0]
        assert isinstance(partner, rt.modules.contacts.Partner)
        return dict(partner=partner)


class UpdatePlan(dd.Action):
    icon_name = 'lightning'
    help_text = _("Build a new list of suggestions. "
                  "This will remove all current suggestions")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        plan.items.all().delete()
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
    """Invert selection status for all suggestions."""
    label = _("Toggle selections")
    help_text = _("Invert selection status for all suggestions.")

    def run_from_ui(self, ar, **kw):
        plan = ar.selected_rows[0]
        for item in plan.items.all():
            item.selected = not item.selected
            item.save()
        ar.success(refresh=True)

