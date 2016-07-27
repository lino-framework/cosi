# -*- coding: UTF-8 -*-
# Copyright 2013-2016 Luc Saffre
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


"""Adds functionality for managing activities.

An **activity** is a series of scheduled calendar events where a given
teacher teaches a given group of participants about a given topic.

There is a configurable list of **topics**.  Activities are grouped
into **activity lines** (meaning "series").  An activity line is a
series of activities having a same **topic**.

The participants of an activity are stored as **Enrolments**.

The internal name "courses" of this plugin and the main model is for
historic reasons.  


.. autosummary::
   :toctree:

   models
   choicelists
   workflows
   desktop

"""


from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("Activities")
    teacher_model = 'contacts.Person'
    pupil_model = 'contacts.Person'

    needs_plugins = ['lino_xl.lib.cal']

    def day_and_month(self, d):
        if d is None:
            return "-"
        return d.strftime("%d.%m.")

    def setup_main_menu(self, site, profile, main):
        m = main.add_menu(self.app_label, self.verbose_name)
        for ca in site.models.courses.CourseAreas.objects():
            m.add_action(ca.courses_table)
        # m.add_action('courses.BasicCourses')
        # m.add_action('courses.JobCourses')
        # m.add_action('courses.DraftCourses')
        # m.add_action('courses.ActiveCourses')
        # m.add_action('courses.InactiveCourses')
        # m.add_action('courses.ClosedCourses')
        m.add_separator()
        m.add_action('courses.Lines')
        m.add_action('courses.PendingRequestedEnrolments')
        m.add_action('courses.PendingConfirmedEnrolments')

    def setup_config_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.Topics')
        m.add_action('courses.Slots')

    def setup_explorer_menu(self, site, profile, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.AllActivities')
        m.add_action('courses.AllEnrolments')
        m.add_action('courses.EnrolmentStates')

