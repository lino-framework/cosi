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


"""Add functionality for automatically generating invoices.

.. autosummary::
    :toctree:

    models
    mixins
    actions
    fixtures.demo2

"""

from lino.api.ad import Plugin, _


class Plugin(Plugin):

    # needs_plugins = ['lino_cosi.lib.ledger']
    needs_plugins = ['lino_cosi.lib.sales']

    voucher_model = 'sales.VatProductInvoice'
    item_model = 'sales.InvoiceItem'
    invoiceable_label = _("Invoiceable")

    def get_voucher_type(self):
        from lino.core.utils import resolve_model
        model = resolve_model(self.voucher_model)
        return self.site.modules.ledger.VoucherTypes.get_for_model(model)

