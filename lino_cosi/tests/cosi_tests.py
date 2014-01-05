# -*- coding: utf-8 -*-
# Copyright 2013-2014 Luc Saffre
# This file is part of the Lino-Cosi project.
# Lino-Cosi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Cosi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Cosi; if not, see <http://www.gnu.org/licenses/>.

"""
This module contains "quick" tests that are run on a demo database 
without any fixture. You can run only these tests by issuing::

  python manage.py test lino_cosi.QuickTest

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)

import decimal

#~ from django.utils import unittest
#~ from django.test.client import Client
#~ from django.conf import settings
from lino.runtime import *

from django.utils import translation
from django.utils.encoding import force_unicode
from django.core.exceptions import ValidationError

from lino import dd
from lino.utils import i2d
from djangosite.utils.djangotest import RemoteAuthTestCase


class DemoTest(RemoteAuthTestCase):
    maxDiff = None
    #~ fixtures = 'std demo'.split()
    fixtures = settings.SITE.demo_fixtures

    def test001(self):
        """
        test whether the demo fixtures load correctly.
        """
