# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
# License: BSD (see file COPYING for details)


"""Database models for `lino_cosi.lib.delivery`.

"""

from __future__ import unicode_literals

from decimal import Decimal

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.core import actions
from lino import mixins

from lino_xl.lib.excerpts.mixins import Certifiable

from lino_xl.lib.vat.utils import add_vat, remove_vat, HUNDRED
from lino_xl.lib.vat.mixins import QtyVatItemBase, VatDocument
from lino_xl.lib.vat.mixins import get_default_vat_regime
from lino_xl.lib.sepa.mixins import Payable
from lino_xl.lib.ledger.mixins import Matching, SequencedVoucherItem
from lino_xl.lib.ledger.models import Voucher
from lino_xl.lib.ledger.choicelists import TradeTypes
from lino_xl.lib.ledger.choicelists import VoucherTypes
from lino_xl.lib.ledger.ui import PartnerVouchers, ByJournal

# ledger = dd.resolve_app('ledger', strict=True)


class ShippingMode(mixins.BabelNamed):
    """
    Represents a possible method of how the items described in a
    :class:`SalesDocument` are to be transferred from us to our customer.

    .. attribute:: price

    """
    class Meta:
        app_label = 'delivery'
        verbose_name = _("Shipping Mode")
        verbose_name_plural = _("Shipping Modes")

    price = dd.PriceField(blank=True, null=True)


class ShippingModes(dd.Table):

    model = 'sales.ShippingMode'


