# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""Default settings module for a :ref:`cosi` project. This is being
inherited by the other applications below :mod:`lino_cosi.projects`.

"""

from __future__ import unicode_literals

from decimal import Decimal

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    """
    Base class for a :ref:`cosi` application,
    designed to be instantiated into the :setting:`SITE` setting.
    
    """

    title = "Lino Così"
    verbose_name = "Lino Così"
    description = _("a Lino application to make Belgian accounting simple.")
    version = "0.1"
    url = "http://www.lino-framework.org/cosi"
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'std few_languages furniture \
    demo demo2 demo_bookings'.split()

    languages = 'en de fr'
    #~ languages = 'de fr et en'.split()

    #~ project_model = 'tickets.Project'
    user_model = 'users.User'

    #~ remote_user_header = "REMOTE_USER"

    #~ def get_application_info(self):
        #~ return (__name__,__version__,__url__)

    #~ def get_main_action(self,user):
        #~ return self.modules.system.Home.default_action

    #~ def setup_quicklinks(self,ui,user,tb):
        #~ tb.add_action(self.modules.contacts.Persons.detail_action)

    def setup_choicelists(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino import dd, rt
        from django.utils.translation import ugettext_lazy as _
        dd.UserProfiles.reset('* office accounts')
        add = dd.UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _ _',
            'anonymous', readonly=True, authenticated=False)
        add('100', _("User"),            'U U U', 'user')
        add('900', _("Administrator"),   'A A A', 'admin')

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        yield 'django.contrib.contenttypes'
        yield 'lino.modlib.system'
        yield 'lino.modlib.users'
        #~ yield 'django.contrib.auth'
        yield 'lino.modlib.countries'
        #~ yield 'lino.modlib.properties'
        yield 'lino.modlib.contacts'
        #~ yield 'lino.modlib.households'
        yield 'lino.modlib.products'
        yield 'lino.modlib.accounts'
        yield 'lino.modlib.sepa'

        yield 'lino.modlib.excerpts'

        # yield 'lino.modlib.outbox'
        # yield 'lino.modlib.uploads'
        yield 'lino.modlib.appypod'
        yield 'lino.modlib.export_excel'

        # ledger must come before sales because its demo fixture
        # creates journals

        yield 'lino.modlib.ledger'
        yield 'lino.modlib.sales'
        yield 'lino.modlib.vat'
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
        yield 'lino_cosi'

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        # self.plugins.contacts.configure(hide_region=True)
        self.plugins.ledger.configure(use_pcmn=True)
        # self.plugins.vat.configure(
        #     VAT_CLASS_TO_RATE=dict(
        #         exempt=Decimal(),
        #         reduced=Decimal('0.06'),
        #         normal=Decimal('0.21')
        #     ))
        self.plugins.vat.VAT_CLASS_TO_RATE.update(
            reduced=Decimal('0.06'),
            normal=Decimal('0.21'))

        super(Site, self).setup_plugins()

