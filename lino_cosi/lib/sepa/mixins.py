# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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
Model mixins for `lino_cosi.lib.sepa`.

"""

from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError

from lino.api import dd, rt, _

from lino.utils import SumCollector
from lino_cosi.lib.ledger.mixins import PartnerRelated


class Payable(PartnerRelated):
    """Model mixin for database objects that are considered *payable
    transactions*. To be combined with some mixin which defines a
    field `partner`.

    A **payable transaction** is a transaction that is expected to
    cause a payment.

    .. attribute:: your_ref
    .. attribute:: due_date
    .. attribute:: title

       A char field with a description for this transaction.

    """
    class Meta:
        abstract = True

    your_ref = models.CharField(
        _("Your reference"), max_length=200, blank=True)
    due_date = models.DateField(_("Due date"), blank=True, null=True)
    # title = models.CharField(_("Description"), max_length=200, blank=True)
    bank_account = dd.ForeignKey('sepa.Account', blank=True, null=True)

    def full_clean(self):
        if self.bank_account:
            if self.bank_account.partner != self.get_partner():
                raise ValidationError(_("Partners mismatch"))
        else:
            self.partner_changed(None)

        if not self.due_date:
            if self.payment_term is not None:
                self.due_date = self.payment_term.get_due_date(
                    self.voucher_date)

        super(Payable, self).full_clean()

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Payable, cls).get_registrable_fields(site):
            yield f
        yield 'your_ref'
        yield 'bank_account'

    def partner_changed(self, ar):
        qs = rt.modules.sepa.Account.objects.filter(
            partner=self.get_partner(), primary=True)
        if qs.count() == 1:
            self.bank_account = qs[0]
        else:
            self.bank_account = None
        
    def get_due_date(self):
        return self.due_date or self.voucher_date

    def get_bank_account(self):
        return self.bank_account

    @dd.chooser()
    def bank_account_choices(cls, partner):
        return rt.modules.sepa.Account.objects.filter(
            partner=partner).order_by('iban')

    def get_payable_sums_dict(self):
        raise NotImplemented()

    def get_wanted_movements(self):
        item_sums = self.get_payable_sums_dict()
        # logger.info("20120901 get_wanted_movements %s", sums_dict)
        counter_sums = SumCollector()
        for k, amount in item_sums.items():
            acc, prj = k
            yield self.create_movement(acc, None, not self.journal.dc, amount)
            counter_sums.collect(prj, amount)

        acc = self.get_trade_type().get_partner_account()
        if acc is None:
            if len(counter_sums.items()):
                raise Exception("Could not find partner account")
        else:
            for prj, amount in counter_sums.items():
                yield self.create_movement(
                    acc, prj, self.journal.dc, amount,
                    partner=self.get_partner(),
                    match=self.match or self.get_default_match())

