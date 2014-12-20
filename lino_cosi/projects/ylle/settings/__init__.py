# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings for an Estonian :ref:`cosi` site à la Ülle.

- `Estonian VAT rates
  <http://www.emta.ee/index.php?id=28460>`_


"""

from __future__ import unicode_literals
from decimal import Decimal
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import string_concat

from lino_cosi.projects.std.settings import *


class Site(Site):
    # title = string_concat(Site.title, " ", _("Estonia"))
    title = Site.title + " Eesti"
    languages = 'en et'
    demo_fixtures = 'std all_countries euvatrates eesti furniture \
    demo demo2'.split()

    def setup_plugins(self):
        self.plugins.contacts.configure(hide_region=False)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.vat.configure(country_code='BE')

        super(Site, self).setup_plugins()

