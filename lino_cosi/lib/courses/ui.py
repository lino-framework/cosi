# -*- coding: UTF-8 -*-
# Copyright 2012-2016 Luc Saffre
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


"""User interface for `lino_cosi.lib.courses`.

"""

from __future__ import unicode_literals
from __future__ import print_function

"""Database models for :mod:`lino_cosi.lib.courses`.

.. autosummary::

"""

import logging
logger = logging.getLogger(__name__)

from decimal import Decimal
ZERO = Decimal()
ONE = Decimal(1)

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt
from lino import mixins

from lino.utils import join_elems
from lino.utils.xmlgen.html import E

from lino.modlib.system.choicelists import PeriodEvents

from .choicelists import EnrolmentStates, CourseStates

cal = dd.resolve_app('cal')

try:
    teacher_model = dd.plugins.courses.teacher_model
    pupil_model = dd.plugins.courses.pupil_model
except AttributeError:
    # Happens only when Sphinx autodoc imports it and this module is
    # not installed.
    teacher_model = 'foo.Bar'
    pupil_model = 'foo.Bar'

FILL_EVENT_GUESTS = False


class Slots(dd.Table):
    model = 'courses.Slot'
    required_roles = dd.required(dd.SiteAdmin)
    insert_layout = """
    start_time end_time
    name
    """
    detail_layout = """
    name start_time end_time
    courses.CoursesBySlot
    """


class Topics(dd.Table):
    model = 'courses.Topic'
    required_roles = dd.required(dd.SiteAdmin)
    detail_layout = """
    id name
    courses.LinesByTopic
    courses.CoursesByTopic
    """


class Lines(dd.Table):
    model = 'courses.Line'
    column_names = ("ref name topic #course_area "
                    "event_type guest_role every_unit every *")
    order_by = ['ref', 'name']
    detail_layout = """
    id name ref
    #course_area topic fees_cat fee options_cat body_template
    event_type guest_role every_unit every
    description
    excerpt_title
    courses.CoursesByLine
    """
    insert_layout = dd.FormLayout("""
    name
    ref topic
    every_unit every event_type
    description
    """, window_size=(70, 16))


class LinesByTopic(Lines):
    master_key = "topic"


class EventsByTeacher(cal.Events):
    help_text = _("Shows events of courses of this teacher")
    master = teacher_model
    column_names = 'when_text:20 owner room state'
    # column_names = 'when_text:20 course__line room state'
    auto_fit_column_widths = True

    @classmethod
    def get_request_queryset(self, ar):
        teacher = ar.master_instance
        if teacher is None:
            return []
        if True:
            return []
        # TODO: build a list of courses, then show events by course
        qs = super(EventsByTeacher, self).get_request_queryset(ar)
        # mycourses = rt.modules.Course.objects.filter(teacher=teacher)
        qs = qs.filter(course__in=teacher.course_set.all())
        return qs


class CourseDetail(dd.FormLayout):
    """The detail layout of a :class:`Course`.
    """
    # start = "start_date start_time"
    # end = "end_date end_time"
    # freq = "every every_unit"
    # start end freq
    main = "general events courses.EnrolmentsByCourse"
    general = dd.Panel("""
    line teacher start_date end_date start_time end_time
    enrolments_until room #slot workflow_buttons id:8 user
    name
    description
    """, label=_("General"))
    events = dd.Panel("""
    max_places max_events max_date every_unit every
    monday tuesday wednesday thursday friday saturday sunday
    cal.EventsByController
    """, label=_("Events"))
    # enrolments = dd.Panel("""
    # OptionsByCourse:20 EnrolmentsByCourse:40
    # """, label=_("Enrolments"))


class Courses(dd.Table):
    """Base table for all courses.
    """
    model = 'courses.Course'
    detail_layout = CourseDetail()
    insert_layout = """
    start_date
    line teacher
    """
    column_names = "start_date enrolments_until line teacher " \
                   "room workflow_buttons *"
    # order_by = ['start_date']
    # order_by = 'line__name room__name start_date'.split()
    # order_by = ['name']
    order_by = ['-start_date', '-start_time']
    auto_fit_column_widths = True

    parameters = mixins.ObservedPeriod(
        line=models.ForeignKey('courses.Line', blank=True, null=True),
        topic=models.ForeignKey('courses.Topic', blank=True, null=True),
        teacher=models.ForeignKey(
            teacher_model,
            blank=True, null=True),
        user=models.ForeignKey(
            settings.SITE.user_model,
            blank=True, null=True),
        state=CourseStates.field(blank=True),
        can_enroll=dd.YesNo.field(blank=True),
    )

    params_layout = """topic line teacher state can_enroll:10 \
    start_date end_date"""

    # simple_parameters = 'line teacher state user'.split()

    @classmethod
    def get_simple_parameters(cls):
        s = super(Courses, cls).get_simple_parameters()
        s.add('line')
        s.add('teacher')
        s.add('state')
        s.add('user')
        return s

    @classmethod
    def get_request_queryset(self, ar):
        # dd.logger.info("20160223 %s", self)
        qs = super(Courses, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        pv = ar.param_values
        if pv.topic:
            qs = qs.filter(line__topic=pv.topic)

        flt = Q(enrolments_until__isnull=True)
        flt |= Q(enrolments_until__gte=dd.today())
        if pv.can_enroll == dd.YesNo.yes:
            qs = qs.filter(flt)
        elif pv.can_enroll == dd.YesNo.no:
            qs = qs.exclude(flt)
        qs = PeriodEvents.active.add_filter(qs, pv)
        # if pv.start_date:
        #     # dd.logger.info("20160512 start_date is %r", pv.start_date)
        #     qs = PeriodEvents.started.add_filter(qs, pv)
        #     # qs = qs.filter(start_date__gte=pv.start_date)
        # if pv.end_date:
        #     qs = PeriodEvents.ended.add_filter(qs, pv)
        #     # qs = qs.filter(end_date__lte=pv.end_date)
        # dd.logger.info("20160512 %s", qs.query)
        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Courses, self).get_title_tags(ar):
            yield t

        if ar.param_values.topic:
            yield unicode(ar.param_values.topic)
        # for n in self.simple_param_fields:
        #     v = ar.param_values.get(n)
        #     if v:
        #         yield unicode(v)


class AllCourses(Courses):
    pass


class CoursesByTeacher(Courses):
    master_key = "teacher"
    column_names = "start_date start_time end_time line room *"
    order_by = ['-start_date']


class CoursesByLine(Courses):
    """Show the courses per course line."""
    master_key = "line"
    column_names = "info weekdays_text room times_text teacher *"
    order_by = ['room__name', '-start_date']


class CoursesByTopic(Courses):
    """Shows the courses of a given topic.

    """
    
    master = 'courses.Topic'
    order_by = ['-start_date']
    column_names = "start_date:8 line:20 room:10 " \
                   "weekdays_text:10 times_text:10"
    params_layout = """line teacher user state can_enroll:10"""

    @classmethod
    def get_filter_kw(self, ar, **kw):
        kw.update(line__topic=ar.master_instance)
        return kw

    # @classmethod
    # def get_request_queryset(self, ar):
    #     Course = rt.modules.courses.Course
    #     topic = ar.master_instance
    #     if topic is None:
    #         return Course.objects.none()
    #     return Course.objects.filter(line__topic=topic)


class CoursesBySlot(Courses):
    master_key = "slot"


class DraftCourses(Courses):
    label = _("Draft courses")
    column_names = 'info teacher room *'
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.draft)
        kw.update(user=ar.get_user())
        # kw.update(can_enroll=dd.YesNo.yes)
        return kw


class ActiveCourses(Courses):

    label = _("Active courses")
    column_names = 'info enrolments:8 free_places teacher room *'
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


class InactiveCourses(Courses):

    label = _("Inactive courses")
    column_names = 'info enrolments:8 free_places teacher room *'
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.inactive)
        return kw


class ClosedCourses(Courses):

    label = _("Closed courses")
    column_names = 'info enrolments:8 teacher room *'
    hide_sums = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(state=CourseStates.closed)
        return kw


class Enrolments(dd.Table):
    """Base class for all enrolment tables."""
    # debug_permissions=20130531
    model = 'courses.Enrolment'
    stay_in_grid = True
    parameters = mixins.ObservedPeriod(
        author=dd.ForeignKey(
            settings.SITE.user_model, blank=True, null=True),
        state=EnrolmentStates.field(blank=True, null=True),
        course_state=CourseStates.field(
            _("Course state"), blank=True, null=True),
        participants_only=models.BooleanField(
            _("Participants only"),
            help_text=_(
                "Hide cancelled enrolments. "
                "Ignored if you specify an explicit enrolment state."),
            default=True),
    )
    params_layout = """start_date end_date author state \
    course_state participants_only"""
    order_by = ['request_date']
    column_names = 'request_date course pupil workflow_buttons user *'
    # hidden_columns = 'id state'
    insert_layout = """
    request_date user
    course pupil
    remark
    """
    detail_layout = """
    request_date user start_date end_date
    course pupil
    remark workflow_buttons
    confirmation_details
    """

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(Enrolments, self).get_request_queryset(ar)
        if isinstance(qs, list):
            return qs
        pv = ar.param_values
        if pv.author is not None:
            qs = qs.filter(user=pv.author)

        if pv.state:
            qs = qs.filter(state=pv.state)
        else:
            if pv.participants_only:
                qs = qs.exclude(state=EnrolmentStates.cancelled)

        if pv.course_state:
            qs = qs.filter(course__state=pv.course_state)

        if pv.start_date or pv.end_date:
            qs = PeriodEvents.active.add_filter(qs, pv)

        # if pv.start_date is None or pv.end_date is None:
        #     period = None
        # else:
        #     period = (pv.start_date, pv.end_date)
        # if period is not None:
        #     qs = qs.filter(dd.inrange_filter('request_date', period))

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Enrolments, self).get_title_tags(ar):
            yield t

        if ar.param_values.state:
            yield unicode(ar.param_values.state)
        elif not ar.param_values.participants_only:
            yield unicode(_("Also ")) + unicode(EnrolmentStates.cancelled.text)
        if ar.param_values.course_state:
            yield unicode(
                settings.SITE.modules.courses.Course._meta.verbose_name) \
                + ' ' + unicode(ar.param_values.course_state)
        if ar.param_values.author:
            yield unicode(ar.param_values.author)


class AllEnrolments(Enrolments):
    """Show global list of all enrolments."""
    required_roles = dd.required(dd.SiteStaff)
    order_by = ['-id']
    column_names = 'id request_date start_date end_date user course pupil *'


class ConfirmAllEnrolments(dd.Action):
    label = _("Confirm all")
    select_rows = False
    http_method = 'POST'

    def run_from_ui(self, ar, **kw):
        obj = ar.selected_rows[0]
        assert obj is None

        def ok(ar):
            for obj in ar:
                obj.state = EnrolmentStates.confirmed
                obj.save()
                ar.set_response(refresh_all=True)

        msg = _(
            "This will confirm all %d enrolments in this list.") % ar.get_total_count()
        ar.confirm(ok, msg, _("Are you sure?"))


class PendingRequestedEnrolments(Enrolments):

    label = _("Pending requested enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True
    column_names = 'request_date course pupil remark user workflow_buttons'
    hidden_columns = 'id state'

    # confirm_all = ConfirmAllEnrolments()

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PendingRequestedEnrolments, self).param_defaults(ar, **kw)
        kw.update(state=EnrolmentStates.requested)
        return kw


class PendingConfirmedEnrolments(Enrolments):
    label = _("Pending confirmed enrolments")
    auto_fit_column_widths = True
    params_panel_hidden = True

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(PendingConfirmedEnrolments, self).param_defaults(ar, **kw)
        kw.update(state=EnrolmentStates.confirmed)
        # kw.update(course_state=CourseStates.ended)
        return kw


class EnrolmentsByPupil(Enrolments):
    params_panel_hidden = True
    required_roles = dd.required()
    master_key = "pupil"
    column_names = 'request_date course user:10 remark workflow_buttons *'
    auto_fit_column_widths = True
    _course_area = None  # CourseAreas.default

    @classmethod
    def get_known_values(self):
        if self._course_area is not None:
            return dict(course_area=self._course_area)
        return dict()

    @classmethod
    def get_actor_label(self):
        if self._course_area is not None:
            return self._course_area.text
        return _("Enrolments")

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(EnrolmentsByPupil, self).param_defaults(ar, **kw)
        kw.update(participants_only=False)
        return kw

    insert_layout = """
    course
    places option
    remark
    request_date user
    """


class EnrolmentsByCourse(Enrolments):
    params_panel_hidden = True
    required_roles = dd.required()
    master_key = "course"
    column_names = 'request_date pupil places option ' \
                   'remark workflow_buttons *'
    auto_fit_column_widths = True
    # cell_edit = False
    slave_grid_format = 'html'

    insert_layout = """
    pupil
    places option
    remark
    request_date user
    """


class EnrolmentsByOption(Enrolments):
    label = _("Enrolments using this option")
    master_key = 'option'
    column_names = 'course pupil remark amount request_date *'
    order_by = ['request_date']
    

# class EventsByCourse(cal.Events):
#     required = dd.required(user_groups='office')
#     master_key = 'course'
#     column_names = 'when_text:20 when_html summary workflow_buttons *'
#     auto_fit_column_widths = True


# dd.inject_field(
#     'cal.Event',
#     'course',
#     dd.ForeignKey(
#         'courses.Course',
#         blank=True, null=True,
#         help_text=_("Fill in only if this event is a session of a course."),
#         related_name="events_by_course"))


class SuggestedCoursesByPupil(ActiveCourses):
    label = _("Suggested courses")
    column_names = 'info enrolments free_places custom_actions *'
    auto_fit_column_widths = True
    hide_sums = True
    master = pupil_model
    details_of_master_template = _("%(details)s for %(master)s")
    params_layout = 'topic line teacher can_enroll'

    @classmethod
    def get_request_queryset(self, ar):
        qs = super(SuggestedCoursesByPupil, self).get_request_queryset(ar)
        pupil = ar.master_instance
        if pupil is not None:
            qs = qs.exclude(enrolment__pupil=pupil)
        return qs

    @dd.displayfield(_("Actions"))
    def custom_actions(self, course, ar, **kw):
        mi = ar.master_instance
        if mi is None:
            return ''
        kv = dict(course=course)
        # kv.update(granting=self)
        # at = self.aid_type
        # ct = at.confirmation_type
        # if not ct:
        #     return ''
        # free = course.get_free_places()
        EnrolmentsByPupil = rt.modules.courses.EnrolmentsByPupil
        sar = ar.spawn_request(
            actor=EnrolmentsByPupil, master_instance=mi, known_values=kv)
        if sar.get_total_count() == 0:
            txt = _("Enrol")
            iar = EnrolmentsByPupil.insert_action.request_from(sar)
            btn = iar.ar2button(txt, icon_name=None)
            # btn = sar.insert_button(txt, icon_name=None)
        else:
            txt = _("Show enrolment")
            btn = ar.obj2html(sar.data_iterator[0])
        return E.span(btn)  # E.p(...) until 20150128


