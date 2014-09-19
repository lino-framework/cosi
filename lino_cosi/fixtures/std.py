# -*- coding: UTF-8 -*-
# Copyright 2013 Luc Saffre
# License: BSD (see file COPYING for details)

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
