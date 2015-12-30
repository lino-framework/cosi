# -*- coding: UTF-8 -*-
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


"""This is Lino's standard plugin for General Ledger.

.. autosummary::
    :toctree:

    utils
    choicelists
    roles
    mixins
    models

"""

from __future__ import unicode_literals

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Ledger")

    needs_plugins = ['lino_cosi.lib.accounts']

    use_pcmn = False
    """
    Whether to use the PCMN notation.

    PCMN stands for "plan compatable minimum normalisé" and is a
    standardized nomenclature for accounts used in France and Belgium.

    """

    project_model = None
    """Leave this to `None` for normal behaviour.  Set this to a string of
    the form `'<app_label>.<ModelName>'` if you want to add an
    additional field `project` to all models which inherit from
    :class:`lino_cosi.lib.ledger.mixins.ProjectRelated`.

    """

    intrusive_menu = False
    """Whether the plugin should integrate into the application's main
    menu in an intrusive way.  Intrusive means that the main menu gets
    one top-level item per journal group.

    The default behaviour is `False`, meaning that these items are
    gathered below a single item "Accounting".

    """
    
    start_year = 2012
    """An integer with the calendar year in which this site starts working.

    This is used to fill the default list of :class:`FiscalYears
    <lino_cosi.lib.ledger.choicelists.FiscalYears>`, and by certain
    fixtures for generating demo invoices.

    """

    def on_site_startup(self, site):
        if site.the_demo_date is not None:
            if self.start_year > site.the_demo_date.year:
                raise Exception("start_year is after the_demo_date")

    def setup_main_menu(self, site, profile, m):
        if not self.intrusive_menu:
            mg = site.plugins.accounts
            m = m.add_menu(mg.app_label, mg.verbose_name)

        Journal = site.modules.ledger.Journal
        JournalGroups = site.modules.ledger.JournalGroups
        for grp in JournalGroups.objects():
            subm = m.add_menu(grp.name, grp.text)
            for jnl in Journal.objects.filter(journal_group=grp):
                subm.add_action(jnl.voucher_type.table_class,
                                label=unicode(jnl),
                                params=dict(master_instance=jnl))

    def setup_reports_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Situation')
        m.add_action('ledger.ActivityReport')
        m.add_action('ledger.Debtors')
        m.add_action('ledger.Creditors')

    def setup_config_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.Journals')
        m.add_action('ledger.PaymentTerms')

    def setup_explorer_menu(self, site, profile, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('ledger.MatchRules')
        m.add_action('ledger.AllVouchers')
        m.add_action('ledger.VoucherTypes')
        m.add_action('ledger.AllMovements')
        m.add_action('ledger.FiscalYears')
        m.add_action('ledger.TradeTypes')


