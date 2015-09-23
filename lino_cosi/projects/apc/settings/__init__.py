# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# This file is part of Lino Cosi.
#
# Lino Cosi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Cosi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Cosi.  If not, see
# <http://www.gnu.org/licenses/>.


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

