# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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


"""Add functionality to importing lecacy data from a TIM database.

.. autosummary::
    :toctree:

    fixtures.tim2lino
    models

"""

from __future__ import unicode_literals

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Import from TIM")

    needs_plugins = ['lino_cosi.lib.finan']

    languages = None
    """The language distribution used in the database to import. Mandatory
    parameter. No default value.

    """

    use_dbf_py = False
    """The default value `False` means to use
    :mod:`lino.utils.dbfreader`.

    `True` means to use Ethan Furman's `dbf
    <http://pypi.python.org/pypi/dbf/>`_ package to read the file,
    This package is not automatically installed with :mod:`lino_cosi`.

    Set it to `True` when reading data from a TIM with FOXPRO DBE,
    leave it at `False` when reading DBFNTX files.

    """

    dbf_table_ext = '.DBF'
    # dbf_table_ext = '.FOX'
    """The file extension of TIM tables. Meaningful values are `'.DBF'` or
    `.FOX`.

    """

    load_listeners = []

    siteconfig_accounts = dict(
        clients_account='400000',
        suppliers_account='440000',
        wages_account='460000',
        sales_account='704000',
        sales_vat_account='411000',  # vat paid 411000, 472100
        purchases_account='610000',
        purchases_vat_account='451000',  # due vat 451000, 472200
        clearings_account='499000')  # 462100

    def add_load_listener(self, tableName, func):
        self.load_listeners.append((tableName, func))
