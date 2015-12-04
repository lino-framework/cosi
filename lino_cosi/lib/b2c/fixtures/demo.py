# -*- coding: UTF-8 -*-
# Copyright 2015 Luc Saffre
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

"""Import a fictive B2C XML file.

"""

import os
HERE = os.path.dirname(__file__)

from lino.api import dd, rt

from lino.utils.cycler import Cycler

from django.conf import settings


def objects():

    ses = rt.login('wilfried')
    dd.plugins.b2c.import_statements_path = HERE
    settings.SITE.site_config.import_b2c(ses)

    # That file contains a few dozen of accounts which are now
    # "orphaned".  We are now going to assign theses accounts to a
    # random partner TODO: find a more realistic rule for selecting
    # the candidates. The filter might be a plugin attribute.

    IA = rt.modules.b2c.Account
    SA = rt.modules.sepa.Account
    PARTNERS = Cycler(rt.modules.contacts.Partner.objects.all())

    count = 0
    for ia in IA.objects.all():
        try:
            SA.objects.get(iban=ia.iban)
        except SA.DoesNotExist:
            yield SA(partner=PARTNERS.pop(), iban=ia.iban)
            count += 1
    if count == 0:
        dd.logger.info(
            "%d statements", rt.modules.b2c.Statement.objects.count())
        raise Exception(
            "There's something wrong: no accounts have been imported")
