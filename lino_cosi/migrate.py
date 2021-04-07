# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)


"""
This is a real-world example of how the application developer
can provide automatic data migrations for Python dumps.

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
