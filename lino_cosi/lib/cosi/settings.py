# -*- coding: UTF-8 -*-
# Copyright 2011-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


"""Default settings module for a :ref:`cosi` project.

"""

import lino_cosi
from lino.projects.std.settings import *


class Site(Site):
    """Base class for a :ref:`cosi` application.

    """

    verbose_name = "Lino Cosi"
    version = lino_cosi.SETUP_INFO['version']
    url = lino_cosi.SETUP_INFO['url']

    # migrations_package = 'lino_cosi.lib.cosi'

    demo_fixtures = 'std few_countries minimal_ledger \
    furniture demo demo2'.split()

    # languages = 'en de fr'
    languages = 'en'

    user_types_module = 'lino_cosi.lib.cosi.user_types'
    custom_layouts_module = 'lino_cosi.lib.cosi.layouts'

    default_build_method = 'weasy2pdf'

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
        yield 'lino.modlib.uploads'
        # yield 'lino.modlib.files'
        yield 'lino.modlib.weasyprint'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.tinymce'
        # yield 'lino.modlib.wkhtmltopdf'

        # ledger must come before sales because its demo fixture
        # creates journals (?)

        yield 'lino_xl.lib.sepa'
        # yield 'lino_xl.lib.vat'
        # yield 'lino.modlib.ledger'
        yield 'lino_cosi.lib.products'
        yield 'lino_xl.lib.sales'
        # yield 'lino_xl.lib.invoicing'
        yield 'lino_xl.lib.ledger'
        yield 'lino_xl.lib.finan'
        # yield 'lino_xl.lib.bevat'
        yield 'lino_xl.lib.sheets'
        #~ 'lino.modlib.journals',
        #~ 'lino_xl.lib.projects',
        #~ yield 'lino_xl.lib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        #~ 'lino_xl.lib.thirds',
        #~ yield 'lino_xl.lib.postings'
        # yield 'lino_xl.lib.pages'
        # yield 'lino_cosi.lib.cosi'

    def get_plugin_configs(self):
        """
        Change the default value of certain plugin settings.

        """
        yield super(Site, self).get_plugin_configs()
        yield ('countries', 'hide_region', True)
        yield ('countries', 'country_code', 'BE')
        yield ('ledger', 'use_pcmn', True)
        yield ('products', 'menu_group', 'sales')
