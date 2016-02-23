# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
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


from __future__ import unicode_literals
from __future__ import print_function

"""
Choicelists for :mod:`lino_cosi.lib.courses`.

"""

import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from lino.api import dd


class CourseStates(dd.Workflow):
    required_roles = dd.required(dd.SiteAdmin)
    invoiceable = models.BooleanField(_("invoiceable"), default=True)

add = CourseStates.add_item
add('10', _("Draft"), 'draft', editable=True, invoiceable=False)
add('20', _("Registered"), 'registered', editable=False, invoiceable=True)
# add('30', _("Started"), 'started', editable=False)
# add('40', _("Ended"), 'ended', editable=False)
# add('50', _("Cancelled"), 'cancelled', editable=True)

# #~ ACTIVE_COURSE_STATES = set((CourseStates.published,CourseStates.started))
# ACTIVE_COURSE_STATES = set((CourseStates.registered, CourseStates.started))


class EnrolmentStates(dd.Workflow):
    verbose_name_plural = _("Enrolment states")
    required_roles = dd.required(dd.SiteAdmin)
    invoiceable = models.BooleanField(_("invoiceable"), default=True)
    uses_a_place = models.BooleanField(_("Uses a place"), default=True)

add = EnrolmentStates.add_item
add('10', _("Requested"), 'requested', invoiceable=False, uses_a_place=False)
add('20', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('30', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
# add('40', _("Certified"), 'certified', invoiceable=True, uses_a_place=True)
#~ add('40', _("Started"),'started')
#~ add('50', _("Success"),'success')
#~ add('60', _("Award"),'award')
#~ add('90', _("Abandoned"),'abandoned')


