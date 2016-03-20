# Copyright 2008-2016 Luc Saffre
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
Model mixins for :mod:`lino_cosi.lib.finan`.
"""


from django.db import models
from django.core.exceptions import ValidationError

from lino_cosi.lib.accounts.utils import DEBIT, CREDIT, ZERO
from lino_cosi.lib.accounts.fields import DebitOrCreditField
from lino_cosi.lib.ledger.mixins import VoucherItem, SequencedVoucherItem
from lino_cosi.lib.ledger.mixins import ProjectRelated, Matching, FKMATCH
from lino.utils.xmlgen.html import E

from lino.api import dd, rt, _

from lino_cosi.lib.ledger.choicelists import VoucherStates

ledger = dd.resolve_app('ledger')


class FinancialVoucher(ledger.Voucher):
    """Base class for all financial vouchers:
    :class:`Grouper`,
    :class:`JournalEntry`,
    :class:`PaymentOrder` and
    :class:`BankStatement`.

    .. attribute:: item_account

        The default value to use when
        :attr:`FinancialVoucherItem.account` of an item is empty.

    .. attribute:: item_remark

        The default value to use when
        :attr:`FinancialVoucherItem.remark` of an item is empty.

    """

    class Meta:
        abstract = True

    item_account = dd.ForeignKey('accounts.Account', blank=True, null=True)
    item_remark = models.CharField(
        _("External reference"), max_length=200, blank=True)

    # def after_state_change(self, ar, old, new):
    #     super(FinancialVoucher, self).after_state_change(ar, old, new)
    #     if self.journal.auto_check_clearings:
    #         self.check_clearings()

    def add_item_from_due(self, obj, **kwargs):
        # if not obj.balance:
        #     raise Exception("20151117")
        if obj.project:
            kwargs.update(project=obj.project)
        if obj.partner:
            kwargs.update(partner=obj.partner)
        i = self.add_voucher_item(
            obj.account, dc=not obj.dc,
            amount=obj.balance, match=obj.match, **kwargs)
        if i.amount < 0:
            i.amount = - i.amount
            i.dc = not i.dc
        return i

    def get_wanted_movements(self):
        raise NotImplemented()

    def get_finan_movements(self):
        # dd.logger.info("20151211 get_finan_movements()")
        amount = ZERO
        mvts = []
        for i in self.items.all():
            if i.dc == self.journal.dc:
                amount += i.amount
            else:
                amount -= i.amount
            # kw = dict(seqno=i.seqno, partner=i.partner)
            kw = dict(partner=i.get_partner())
            kw.update(match=i.match or i.get_default_match())
            b = self.create_movement(
                i.account or self.item_account,
                i.project, i.dc, i.amount, **kw)
            mvts.append(b)

        return amount, mvts


class FinancialVoucherItem(VoucherItem, SequencedVoucherItem,
                           ProjectRelated, Matching):
    """The base class for the items of all types of financial vouchers
    (:class:`FinancialVoucher`).

    .. attribute:: account

        The general account to be used in the primary booking.
        If this is empty, use :attr:`item_account` of the voucher.

    .. attribute:: project

        The client related to this transaction.

    .. attribute:: partner

        The partner account to be used in the primary booking.
    
        In Lino Welfare this field is optional and used only for
        transactions whose *recipient* is different from the *client*.
        When empty, Lino will book to the **client**
        (i.e. :attr:`project`).

    .. attribute:: amount

        The amount to be booked. If this is empty, then the voucher
        cannot be registered.

    .. attribute:: dc

        The direction of the primary booking to create.

    .. attribute:: remark

        External reference. The description of this transation
        as seen by the external partner.

    .. attribute:: seqno

    .. attribute:: match

        (if FKMATCH) The voucher that caused this voucher item.  For
        example the :attr:`match` of the payment of an invoice points
        to that invoice.

        An arbitrary string used to group several movements.

    """
    class Meta:
        abstract = True
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    amount = dd.PriceField(_("Amount"), default=ZERO)
    dc = DebitOrCreditField()
    remark = models.CharField(
        _("External reference"), max_length=200, blank=True)
    account = dd.ForeignKey('accounts.Account', blank=True, null=True)
    partner = dd.ForeignKey('contacts.Partner', blank=True, null=True)

    @dd.chooser(simple_values=not FKMATCH)
    def match_choices(cls, voucher, partner):
        return cls.get_match_choices(voucher.journal, partner)

    def get_default_match(self):
        return "%s#%s:%s" % (
            self.voucher.journal.ref, self.voucher.id, self.seqno)
        # return str(self.date)

    def get_siblings(self):
        return self.voucher.items.all()

    def match_changed(self, ar):
        if self.match:
            dc = not self.voucher.journal.dc
            m = ledger.DueMovement(dc, self)
            self.dc = dc
            self.amount = m.balance
            # if not m.balance:
            #     raise Exception("20151117")

    def partner_changed(self, ar):
        """The :meth:`trigger method <lino.core.model.Model.FOO_changed>` for
        :attr:`partner`.

        """
        if self.partner:
            flt = dict(partner=self.partner, satisfied=False)
            if self.match:
                flt.update(match=self.match)
            suggestions = list(ledger.get_due_movements(
                self.voucher.journal.dc, **flt))

            if len(suggestions) == 0:
                pass
            elif len(suggestions) == 1:
                self.fill_suggestion(suggestions[0])
            else:
                def ok(ar2):
                    # self.fill_suggestion(suggestions[0])
                    # self.set_grouper(suggestions)
                    ar2.error(_("Oops, not implemented."))
                    return

                html = E.div(
                    E.p("Cool", E.b(str(len(suggestions)), "suggestions")))
                if ar:
                    ar.confirm(ok, E.tostring(html))
                return
            if self.account_id is None:
                if self.voucher.item_account_id is None:
                    raise ValidationError(
                        _("Could not determine the general account"))
        # print self.partner_id
        # if self.partner_id is None:
        #     raise ValidationError(
        #         _("Could not determine the partner account"))

    def get_partner(self):
        return self.partner or self.project

    def fill_suggestion(self, match):
        """Fill the fields of this item from the given suggestion (a
        `DueMovement` instance).

        """
        # if not match.balance:
        #     raise Exception("20151117")
        if match.trade_type:
            self.account = match.trade_type.get_partner_account()
        if self.account_id is None:
            self.account = match.account
        self.dc = match.dc
        self.amount = - match.balance
        self.match = match.match
        self.project = match.project

    def full_clean(self, *args, **kwargs):
        if self.dc is None:
            self.dc = self.voucher.journal.dc
        if self.amount < 0:
            self.amount = - self.amount
            self.dc = not self.dc
        # dd.logger.info("20151117 FinancialVoucherItem.full_clean a %s", self.amount)
        super(FinancialVoucherItem, self).full_clean(*args, **kwargs)
        # dd.logger.info("20151117 FinancialVoucherItem.full_clean b %s", self.amount)

