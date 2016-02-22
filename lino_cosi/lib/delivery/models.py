# -*- coding: UTF-8 -*-
# Copyright 2008-2015 Luc Saffre
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

from lino_cosi.lib.vat.utils import add_vat, remove_vat, HUNDRED
from lino_cosi.lib.vat.mixins import QtyVatItemBase, VatDocument
from lino_cosi.lib.vat.mixins import get_default_vat_regime
from lino_cosi.lib.sepa.mixins import Payable
from lino_cosi.lib.ledger.mixins import Matching, SequencedVoucherItem
from lino_cosi.lib.ledger.models import Voucher
from lino_cosi.lib.ledger.choicelists import TradeTypes
from lino_cosi.lib.ledger.choicelists import VoucherTypes
from lino_cosi.lib.ledger.ui import PartnerVouchers, ByJournal

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


