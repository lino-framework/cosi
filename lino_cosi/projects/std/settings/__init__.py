# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
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

    verbose_name = "Lino Così"
    version = lino_cosi.SETUP_INFO['version']
    url = lino_cosi.SETUP_INFO['url']

    demo_fixtures = 'std few_countries euvatrates few_languages furniture \
    minimal_ledger demo demo2 demo_bookings'.split()

    # languages = 'en de fr'
    languages = 'en'

    enable_role_based_permissions = True

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'lino.modlib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        yield 'lino.modlib.countries'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.sepa'

        yield 'lino.modlib.excerpts'

        # yield 'lino.modlib.outbox'
        # yield 'lino.modlib.uploads'
        # yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

        # ledger must come before sales because its demo fixture
        # creates journals

        # yield 'lino.modlib.ledger'
        yield 'lino.modlib.vat'
        yield 'lino.modlib.sales'
        yield 'lino.modlib.declarations'
        yield 'lino.modlib.finan'
        #~ 'lino.modlib.journals',
        #~ 'lino.modlib.projects',
        #~ yield 'lino.modlib.blogs'
        #~ yield 'lino.modlib.tickets'
        #~ 'lino.modlib.links',
        #~ 'lino.modlib.thirds',
        #~ yield 'lino.modlib.cal'
        #~ yield 'lino.modlib.postings'
        # yield 'lino.modlib.pages'
        yield 'lino_cosi.lib.cosi'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.contacts.configure(hide_region=True)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.countries.configure(country_code='BE')

    def setup_user_profiles(self):
        """This defines default user profiles.

        """
        from lino.modlib.users.choicelists import UserProfiles
        from lino_cosi.lib.cosi.roles import *

        UserProfiles.clear()

        add = UserProfiles.add_item
        
        add('000', _("Anonymous"), Anonymous, name='anonymous',
            readonly=True, authenticated=False)
        add('100', _("User"),           SiteUser)
        add('900', _("Administrator"),  SiteAdmin, name='admin')

