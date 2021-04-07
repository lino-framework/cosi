# Copyright 2008-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Orders")

    def setup_main_menu(config, site, user_type, m):
        m = m.add_menu(vat.TradeTypes.sales.name, vat.TradeTypes.sales.text)
        m.add_action(Orders)

    def setup_config_menu(config, site, user_type, m):
        m = m.add_menu("sales", MODULE_LABEL)
        m.add_action(InvoicingModes)
        m.add_action(ShippingModes)
        m.add_action(PaymentTerms)

        
