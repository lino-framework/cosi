# -*- coding: UTF-8 -*-
# Copyright 2011-2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""Default settings module for a :ref:`cosi` project. This is being
inherited by the other applications below :mod:`lino_cosi.projects`.

"""

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _

import lino_cosi


class Site(Site):
    """Base class for a :ref:`cosi` application.

    """

    verbose_name = "Lino Cosi"
    version = lino_cosi.SETUP_INFO['version']
    url = lino_cosi.SETUP_INFO['url']

    demo_fixtures = 'std few_countries minimal_ledger \
    furniture demo demo2'.split()

    # languages = 'en de fr'
    languages = 'en'

    user_types_module = 'lino_cosi.lib.cosi.user_types'
    custom_layouts_module = 'lino_cosi.lib.cosi.layouts'

    # default_build_method = 'wkhtmltopdf'

    # textfield_format = 'html'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.gfks'
        # yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino_xl.lib.countries'
        yield 'lino_cosi.lib.contacts'
        #~ yield 'lino_xl.lib.households'

        yield 'lino_xl.lib.excerpts'

        # yield 'lino_xl.lib.outbox'
        # yield 'lino.modlib.uploads'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.wkhtmltopdf'

        # ledger must come before sales because its demo fixture
        # creates journals (?)

        # yield 'lino.modlib.ledger'
        yield 'lino_xl.lib.sales'
        yield 'lino_xl.lib.invoicing'
        yield 'lino_xl.lib.products'
        yield 'lino_xl.lib.ledger'
        yield 'lino_xl.lib.sepa'
        yield 'lino_xl.lib.vat'
        yield 'lino_xl.lib.finan'
        yield 'lino_xl.lib.bevat'
        #~ 'lino.modlib.journals',
        #~ 'lino_xl.lib.projects',
        #~ yield 'lino_xl.lib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        #~ 'lino_xl.lib.thirds',
        #~ yield 'lino_xl.lib.postings'
        # yield 'lino_xl.lib.pages'
        # yield 'lino_cosi.lib.cosi'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.countries.configure(hide_region=True)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.countries.configure(country_code='BE')
        self.plugins.products.configure(menu_group='sales')

    # def setup_actions(self):
    #     super(Site, self).setup_actions()
    #     partners = self.modules.contacts
    #     from lino.core.merge import MergeAction
    #     for m in (partners.Person, partners.Organisation):
    #         m.define_action(merge_row=MergeAction(m))

    # def setup_layouts(self):
    #     super(Site, self).setup_layouts()

    #     self.models.system.SiteConfigs.set_detail_layout("""
    #     site_company next_partner_id:10
    #     default_build_method
    #     clients_account   sales_account
    #     suppliers_account purchases_account tax_offices_account
    #     """)

    #     self.models.ledger.Accounts.set_detail_layout("""
    #     ref:10 name id:5
    #     seqno group type clearable
    #     ledger.MovementsByAccount
    #     """)


# class DocsSite(Site):
#     """A special variant used to build the docs.
#     """
#     def get_installed_apps(self):
#         yield super(DocsSite, self).get_installed_apps()
#         yield 'lino_xl.lib.courses'  # needed for Sphinx autosummary
#         yield 'lino_xl.lib.vatless'

    # def get_apps_modifiers(self, **kw):
    #     kw = super(DocsSite, self).get_apps_modifiers(**kw)
    #     kw.update(sales='lino_cosi.lib.auto.sales')
    #     return kw
