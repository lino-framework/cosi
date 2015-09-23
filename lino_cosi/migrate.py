# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
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
This is a real-world example of how the application developer
can provide automatic data migrations for :ref:`dpy`.

This module is used because a :ref:`cosi`
Site has :setting:`migration_class` set to ``"lino_cosi.migrate.Migrator"``.

"""

import logging
logger = logging.getLogger(__name__)

import datetime
from decimal import Decimal
from django.conf import settings
from lino.core.utils import resolve_model
from lino.utils import mti
from lino.utils import dblogger
from lino.api import dd, rt

from lino.utils.dpy import Migrator


class Migrator(Migrator):


    def migrate_from_0_0_1(globals_dict):
        """
        - Renamed `countries.City` to `countries.Place`
        """
        countries_Place = resolve_model("countries.Place")
        globals_dict.update(countries_City=countries_Place)
        return '0.0.2'
