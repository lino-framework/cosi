# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)


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

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu("sales", self.verbose_name)
        # m.add_action('sales.InvoicingModes')
        m.add_action('delivery.ShippingModes')


