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


"""Database models for `lino_cosi.lib.vatless`.



"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

from django.db import models

from lino.api import dd, _

from lino.utils import SumCollector

from lino_cosi.lib.ledger.mixins import (
    ProjectRelated,  # PartnerRelated,
    AccountVoucherItem, Matching)
from lino_cosi.lib.sepa.mixins import Payable
from lino_cosi.lib.ledger.models import Voucher
from lino_cosi.lib.ledger.choicelists import TradeTypes

TradeTypes.purchases.update(
    partner_account_field_name='suppliers_account',
    partner_account_field_label=_("Suppliers account"))


class AccountInvoice(Payable, Voucher, Matching, ProjectRelated):

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    def compute_totals(self):
        if self.pk is None:
            return
        base = Decimal()
        for i in self.items.all():
            if i.amount is not None:
                base += i.amount
        self.amount = base

    def get_payable_sums_dict(self):
        tt = self.get_trade_type()
        sums = SumCollector()
        for i in self.items.order_by('seqno'):
            if i.amount:
                b = i.get_base_account(tt)
                if b is None:
                    raise Exception(
                        "No base account for %s (amount is %r)" % (
                            i, i.amount))
                sums.collect((b, i.project or self.project), i.amount)
        return sums

    def full_clean(self, *args, **kw):
        self.compute_totals()
        super(AccountInvoice, self).full_clean(*args, **kw)

    def before_state_change(self, ar, old, new):
        if new.name == 'registered':
            self.compute_totals()
        elif new.name == 'draft':
            pass
        super(AccountInvoice, self).before_state_change(ar, old, new)


class InvoiceItem(AccountVoucherItem, ProjectRelated):
    """An item of an :class:`AccountInvoice`."""
    voucher = dd.ForeignKey('vatless.AccountInvoice', related_name='items')
    title = models.CharField(_("Description"), max_length=200, blank=True)
    amount = dd.PriceField(_("Amount"), blank=True, null=True)


from .ui import *
