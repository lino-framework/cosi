# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings for a :ref:`cosi` "à la APC".

"""

from __future__ import unicode_literals

from lino_cosi.projects.std.settings import *


class Site(Site):
    languages = 'de fr nl'
    demo_fixtures = 'std all_countries be euvatrates furniture \
    minimal_ledger demo demo2'.split()

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.contacts.configure(hide_region=False)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.countries.configure(country_code='BE')

