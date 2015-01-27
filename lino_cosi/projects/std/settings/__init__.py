# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""Default settings module for a :ref:`cosi` project. This is being
inherited by the other applications below :mod:`lino_cosi.projects`.

"""

from __future__ import unicode_literals

from lino.projects.std.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):
    """
    Base class for a :ref:`cosi` application.

    """

    title = "Lino Così"
    verbose_name = "Lino Così"
    description = _("a Lino application to make Belgian accounting simple.")
    version = "0.1"
    url = "http://cosi.lino-framework.org"
    #~ author = 'Luc Saffre'
    #~ author_email = 'luc.saffre@gmail.com'

    demo_fixtures = 'std few_languages furniture \
    demo demo2 demo_bookings'.split()

    # languages = 'en de fr'
    languages = 'en'

    def setup_user_profiles(self):
        """
        Defines application-specific default user profiles.
        Local site administrators can override this in their :xfile:.
        """
        from lino.modlib.users.choicelists import UserProfiles
        from django.utils.translation import ugettext_lazy as _
        UserProfiles.reset('* office accounts')
        add = UserProfiles.add_item
        add('000', _("Anonymous"),       '_ _ _',
            'anonymous', readonly=True, authenticated=False)
        add('100', _("User"),            'U U U', 'user')
        add('900', _("Administrator"),   'A A A', 'admin')

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
        super(Site, self).setup_plugins()
        self.plugins.contacts.configure(hide_region=True)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.countries.configure(country_code='BE')

