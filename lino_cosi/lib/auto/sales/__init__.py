# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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


"""Extends :mod:`lino_cosi.lib.sales` to add functionality for
automatically generating invoices.

**Deprecated** : this module is no longer used. Use
:mod:`lino_cosi.lib.invoicing` instead

.. autosummary::
    :toctree:

    models
    mixins

"""

from lino_cosi.lib.sales import Plugin


class Plugin(Plugin):

    extends_models = ['VatProductInvoice',  'InvoiceItem']

    def setup_main_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('sales.InvoicesToCreate')

        raise DeprecationWarning(
            "This module is no longer used. "
            "Use `lino_cosi.lib.invoicing` instead")


