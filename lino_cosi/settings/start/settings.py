# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino_cosi.settings import *

from django.utils.translation import ugettext_lazy as _


class Site(Site):

    verbose_name = "Lino Start"
    description = _("a Lino application for startup projects.")
    version = "0.1"

    demo_fixtures = 'std intro furniture demo demo2'.split()

    default_ui = 'pages'

    sidebar_width = 3
    user_model = 'users.User'

    languages = 'en et'
    #~ languages = 'de fr et en'.split()

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()

        yield 'lino.modlib.pages'
        yield 'lino.modlib.blogs'
        yield 'lino.modlib.extensible'
        yield 'lino.modlib.cal'
        yield 'lino.modlib.uploads'
        yield 'lino.modlib.outbox'
        yield 'lino.modlib.importfilters'
