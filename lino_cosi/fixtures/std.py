# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
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

from __future__ import unicode_literals

from lino.utils.instantiator import Instantiator, i2d
from django.utils.translation import ugettext_lazy as _


from django.conf import settings
from north.dbutils import babelkw
from lino import dd


def unused_objects():

    mailType = Instantiator('notes.NoteType').build

    yield mailType(**babelkw('name',
                             en="Enrolment",
                             fr=u'Inscription',
                             de=u"Einschreibeformular"))
    yield mailType(**babelkw('name',
                             en="Timetable",
                             fr=u'Horaire', de=u"Stundenplan"))
    yield mailType(**babelkw('name',
                             en="Letter",
                             fr=u'Lettre', de=u"Brief"))
