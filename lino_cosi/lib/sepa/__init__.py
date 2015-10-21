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


"""Adds models and tables for managing bank accounts for your
partners.  It requires the :mod:`lino.modlib.contacts` app.

.. autosummary::
   :toctree:

    models
    ui
    mixins
    utils
    fields
    roles
    camt
    parserlib
    fixtures.demo
    fixtures.sample_ibans

"""

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("SEPA")
    site_js_snippets = ['iban/uppercasetextfield.js']

    import_statements_path = None
    """A path wildcard pointing to xml files which need to get imported.

    As a system admin you can set this e.g. by specifying in your
    :xfile:`settings.py` (*before* instantiating your
    :setting:`SITE`)::

       ad.configure_plugin('sepa', import_statements_path="/var/sepa")

    End-users are supposed to download SEPA statement files to that
    directory and then to invoke the
    :class:`lino_cosi.lib.sepa.models.ImportStatements` action.

    """

    delete_imported_xml_files = False
    """This attribute define whether, Cosi have to delete the SEPA file after it get imported.
    """

    needs_plugins = ['lino_cosi.lib.ledger']

    def setup_main_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('system.SiteConfig', 'import_sepa')
        m.add_action('sepa.OrphanedAccounts')

    def setup_explorer_menu(config, site, profile, m):
        m = m.add_menu(config.app_label, config.verbose_name)
        m.add_action('sepa.Accounts')
        m.add_action('sepa.Statements')
        m.add_action('sepa.Movements')
