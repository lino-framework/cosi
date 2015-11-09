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


"""Adds delivery notes to the sales workflow.

.. autosummary::
    :toctree:

    models



"""

from lino.api import ad
from django.utils.translation import ugettext_lazy as _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Delivery")

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu("sales", self.verbose_name)
        # m.add_action('sales.InvoicingModes')
        m.add_action('delivery.ShippingModes')


