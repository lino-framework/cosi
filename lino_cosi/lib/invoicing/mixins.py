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
Model mixins for `lino_cosi.lib.invoicing`.

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

from decimal import Decimal

ZERO = Decimal()

from lino.api import dd, rt
from lino.core.gfks import gfk2lookup


class Invoiceable(dd.Model):
    """Mixin for things that are "invoiceable", i.e. for which a customer
    is going to receive an invoice.

    .. attribute:: invoice

    """

    invoiceable_date_field = ''
    """The name of the field which holds the invoiceable date.  Must be
    set by subclasses.

    """

    class Meta:
        abstract = True

    # invoice = dd.ForeignKey('sales.VatProductInvoice', blank=True, null=True)

    def get_invoicings(self, **kwargs):
        InvoiceItem = rt.modules.sales.InvoiceItem
        kwargs.update(gfk2lookup(InvoiceItem.invoiceable, self))
        return InvoiceItem.objects.filter(**kwargs)

    def get_wanted_items(self, ar, invoice, item_model):
        i = item_model(voucher=invoice, invoiceable=self,
                       product=self.get_invoiceable_product(),
                       title=self.get_invoiceable_title(),
                       qty=self.get_invoiceable_qty())
        am = self.get_invoiceable_amount()
        if am is not None:
            i.set_amount(ar, am)
        self.setup_invoice_item(i)
        return [i]

    def get_invoiceable_product(self):
        """To be implemented by subclasses.  Return the product to put into
        the invoice item.

        """
        return None

    def get_invoiceable_qty(self):
        """To be implemented by subclasses.  Return the quantity to put into
        the invoice item.

        """
        return None

    def get_invoiceable_title(self):
        """Return the title to put into the invoice item.  May be overridden
        by subclasses.

        """
        return unicode(self)

    def get_invoiceable_amount(self):
        return None

    def get_invoiceable_partner(self):
        return None

    def get_invoiceable_date(self):
        return getattr(self, self.invoiceable_date_field)

    @classmethod
    def unused_get_partner_filter(cls, partner):
        """
        To be implemented by subclasses.
        Return the filter to apply to :class:`lino.modlib.contacts.models.Partner` in
        order to get the partner who must receive the invoice.

        """
        raise NotImplementedError()

    # @classmethod
    # def get_invoiceables_for_partner(cls, partner, max_date):
    #     """Yield a sequence of invoiceables (of this class) for the given
    #     partner.

    #     """
    #     raise NotImplementedError()

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):
        """Yield a sequence of invoiceables (of this class) for the given
        partner.

        """
        raise NotImplementedError()

    def setup_invoice_item(self, item):
        pass
