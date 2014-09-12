# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

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

