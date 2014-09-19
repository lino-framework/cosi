# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Default settings for an Estonian :ref:`cosi` site.

- `Estonian VAT rates
  <http://www.emta.ee/index.php?id=28460>`_


"""

from __future__ import unicode_literals
from decimal import Decimal
# from django.utils.translation import ugettext_lazy as _
# from django.utils.translation import string_concat

from lino_cosi.settings import *

class Site(Site):
    # title = string_concat(Site.title, " ", _("Estonia"))
    title = Site.title + " Eesti"
    languages = 'en et'
    demo_fixtures = 'std all_countries eesti furniture \
    demo demo2'.split()

    def setup_plugins(self):
        self.plugins.contacts.configure(hide_region=False)
        self.plugins.ledger.configure(use_pcmn=True)
        self.plugins.vat.VAT_CLASS_TO_RATE.update(
            reduced=Decimal('0.09'),
            normal=Decimal('0.20'))

        super(Site, self).setup_plugins()

