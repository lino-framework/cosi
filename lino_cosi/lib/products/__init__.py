# -*- coding: UTF-8 -*-
# Copyright 2017-2019 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
The :ref:`cosi` extension of :mod:`lino_xl.lib.products`.

"""

from lino_xl.lib.products import Plugin, _


class Plugin(Plugin):

    extends_models = ['Product']
    menu_group = 'sales'

    # def setup_main_menu(self, site, user_type, m):
    #     pass
    #
    # def setup_config_menu(self, site, user_type, m):
    #     m = m.add_menu(self.app_label, self.verbose_name)
    #     for pt in site.models.products.ProductTypes.get_list_items():
    #         m.add_action('products.ProductsByType', pt)
    #     m.add_action('products.Categories')

