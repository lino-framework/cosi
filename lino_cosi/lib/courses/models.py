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


"""Database models for `lino_cosi.lib.courses`.

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
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext

from lino.api import dd, rt
from lino import mixins

from lino.mixins.human import parse_name
from lino.mixins.duplicable import Duplicable
from lino.mixins.periods import DatePeriod
from lino_xl.lib.excerpts.mixins import Certifiable
from lino_xl.lib.excerpts.mixins import ExcerptTitle
from lino.modlib.users.mixins import UserAuthored
from lino.modlib.printing.mixins import Printable
from lino_xl.lib.cal.mixins import Reservation
from lino_xl.lib.cal.choicelists import Recurrencies

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


class CourseAreas(dd.ChoiceList):
    preferred_width = 10
    verbose_name = _("Course area")
    verbose_name_plural = _("Course areas")
add = CourseAreas.add_item
add('C', _("Courses"), 'default')
# add('J', _("Journeys"), 'journeys')


class StartEndTime(dd.Model):

    class Meta:
        abstract = True
    start_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("Start Time"))
    end_time = models.TimeField(
        blank=True, null=True,
        verbose_name=_("End Time"))


@dd.python_2_unicode_compatible
class Slot(mixins.Sequenced, StartEndTime):

    """
    """
    class Meta:
        app_label = 'courses'
        app_label = 'courses'
        verbose_name = _("Timetable Slot")  # Zeitnische
        verbose_name_plural = _('Timetable Slots')

    name = models.CharField(max_length=200,
                            blank=True,
                            verbose_name=_("Name"))

    def __str__(self):
        return self.name or "%s-%s" % (self.start_time, self.end_time)


class Topic(mixins.BabelNamed, Printable, Duplicable):

    class Meta:
        app_label = 'courses'
        verbose_name = _("Topic")
        verbose_name_plural = _('Topics')


@dd.python_2_unicode_compatible
class Line(ExcerptTitle, Duplicable):
    """A **line** (or **series**) of courses groups courses into a
    configurable list of categories.

    We chose the word "line" instead of "series" because it has a
    plural form (not sure whether this idea was so cool).

    .. attribute:: name

        The designation of this course series as seen by the user
        e.g. when selecting the series of a course.

        One field for every :attr:`language <lino.core.site.Site.language>`.

    .. attribute:: excerpt_title

        The text to print as title in enrolments.

        See also
        :attr:`lino_xl.lib.excerpts.mixins.ExcerptTitle.excerpt_title`.

    .. attribute:: body_template

        The body template to use when printing a course of this
        series.  Leave empty to use the site's default (defined by
        `body_template` on the
        :class:`lino_xl.lib.excerpts.models.ExcerptType` for
        :class:`Course`)

    """
    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')
        verbose_name = pgettext("singular form", "Course series")
        verbose_name_plural = pgettext("plural form", 'Course series')

    ref = dd.NullCharField(_("Reference"), max_length=30, unique=True)
    course_area = CourseAreas.field(blank=True)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    description = dd.BabelTextField(_("Description"), blank=True)

    every_unit = Recurrencies.field(
        _("Recurrency"),
        default=Recurrencies.per_weekday.as_callable,
        blank=True)  # iCal:DURATION
    every = models.IntegerField(_("Repeat every"), default=1)

    event_type = dd.ForeignKey(
        'cal.EventType', null=True, blank=True,
        help_text=_(
            "The type of calendar events to be generated. "
            "If this is empty, no calendar events will be generated."))

    fee = dd.ForeignKey(
        'products.Product',
        blank=True, null=True,
        verbose_name=_("Participation fee"),
        related_name='lines_by_fee')

    guest_role = dd.ForeignKey(
        "cal.GuestRole", blank=True, null=True,
        verbose_name=_("Manage presences as"),
        help_text=_(
            "The default guest role for particpants of events for "
            "courses in this series. "
            "Leave empty if you don't want any presence management."))

    options_cat = dd.ForeignKey(
        'products.ProductCat',
        verbose_name=_("Options category"),
        related_name="courses_lines_by_options_cat",
        blank=True, null=True)

    fees_cat = dd.ForeignKey(
        'products.ProductCat',
        verbose_name=_("Fees category"),
        related_name="courses_lines_by_fees_cat",
        blank=True, null=True)

    body_template = models.CharField(
        max_length=200,
        verbose_name=_("Body template"),
        blank=True, help_text="The body template to use when "
        "printing a course of this series. "
        "Leave empty to use the site's default.")

    def __str__(self):
        if self.ref:
            return self.ref
        # return super(Line, self).__str__()
        return dd.babelattr(self, 'name')  # or unicode(self)
        # return "{0} #{1}".format(self._meta.verbose_name, self.pk)

    @dd.chooser()
    def fee_choices(cls, fees_cat):
        Product = rt.modules.products.Product
        if not fees_cat:
            return Product.objects.none()
        return Product.objects.filter(cat=fees_cat)

    @dd.chooser(simple_values=True)
    def body_template_choices(cls):
        return dd.plugins.jinja.list_templates(
            '.body.html',
            rt.modules.courses.Enrolment.get_template_group(),
            'excerpts')


@dd.python_2_unicode_compatible
class Course(Reservation, Duplicable):
    """A Course is a group of pupils that regularily meet with a given
    teacher in a given room to speak about a given subject.

    The subject of a course is expressed by the :class:`Line`.

    Notes about automatic event generation:
    
    - When an automatically generated event is to be moved to another
      date, e.g. because it falls into a vacation period, then you
      simply change it's date.  Lino will automatically adapt all
      subsequent events.
      
    - Marking an automatically generated event as "Cancelled" will not
      create a replacement event.

    .. attribute:: enrolments_until

    .. attribute:: max_places

        Available places. The maximum number of participants to allow
        in this course.

    """

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')
        verbose_name = _("Course")
        verbose_name_plural = _('Courses')

    line = models.ForeignKey('courses.Line')

    teacher = models.ForeignKey(
        teacher_model,
        verbose_name=_("Instructor"),
        blank=True, null=True)

    #~ room = models.ForeignKey(Room,blank=True,null=True)
    slot = models.ForeignKey(Slot, blank=True, null=True)
    description = dd.BabelTextField(_("Description"), blank=True)
    remark = models.TextField(_("Remark"), blank=True)

    quick_search_fields = 'name line__name line__topic__name'

    state = CourseStates.field(
        default=CourseStates.draft.as_callable)

    max_places = models.PositiveIntegerField(
        pgettext("in a course", "Available places"),
        help_text=("Maximum number of participants"),
        blank=True, null=True)

    name = models.CharField(_("Designation"), max_length=100, blank=True)
    enrolments_until = models.DateField(
        _("Enrolments until"), blank=True, null=True)

    def on_duplicate(self, ar, master):
        self.state = CourseStates.draft
        super(Course, self).on_duplicate(ar, master)

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Course, cls).get_registrable_fields(site):
            yield f
        yield 'line'
        yield 'teacher'
        yield 'name'
        yield 'enrolments_until'

    def __str__(self):
        if self.name:
            return self.name
        if self.room is None:
            return "%s (%s)" % (self.line, dd.fds(self.start_date))
        # Note that we cannot use super() with
        # python_2_unicode_compatible
        return "%s (%s %s)" % (
            self.line,
            dd.fds(self.start_date),
            self.room)

    def update_cal_from(self, ar):
        """Note: if recurrency is per_weekday, actual start may be
        later than self.start_date

        """
        # if self.state in (CourseStates.draft, CourseStates.cancelled):
        # if self.state == CourseStates.cancelled:
        #     ar.info("No start date because state is %s", self.state)
        #     return None
        return self.start_date

    def update_cal_calendar(self):
        return self.line.event_type

    def update_cal_summary(self, i):
        label = dd.babelattr(self.line.event_type, 'event_label')
        return "%s %d" % (label, i)

    def suggest_cal_guests(self, event):
        """Look up enrolments of this course and suggest them as guests."""
        # logger.info("20140314 suggest_guests")
        Guest = rt.modules.cal.Guest
        Enrolment = rt.modules.courses.Enrolment
        if self.line is None:
            return
        gr = self.line.guest_role
        if gr is None:
            return
        # fkw = dict(course=self)
        # states = (EnrolmentStates.requested, EnrolmentStates.confirmed)
        # fkw.update(state__in=states)
        qs = Enrolment.objects.filter(course=self).order_by('pupil__name')
        for obj in qs:
            if obj.is_guest_for(event):
                yield Guest(
                    event=event,
                    partner=obj.pupil,
                    role=gr)

    def get_free_places(self, rng=None):
        Enrolment = rt.modules.courses.Enrolment
        PeriodEvents = rt.modules.system.PeriodEvents
        # from lino.mixins.periods import DatePeriodValue
        # if today is None:
        #     today = dd.today()
        used_states = EnrolmentStates.filter(uses_a_place=True)
        qs = Enrolment.objects.filter(course=self, state__in=used_states)
        if rng is None:
            rng = dd.today()
        qs = PeriodEvents.active.add_filter(qs, rng)
        # logger.info("20160502 %s", qs.query)
        res = qs.aggregate(models.Sum('places'))
        # logger.info("20140819 %s", res)
        used_places = res['places__sum'] or 0
        return self.max_places - used_places

    def full_clean(self, *args, **kw):
        if self.line_id is not None:
            if self.id is None:
                descs = dd.field2kw(self.line, 'description')
                descs = dd.babelkw('description', **descs)
                for k, v in descs.items():
                    setattr(self, k, v)
            if self.every_unit is None:
                self.every_unit = self.line.every_unit
            if self.every is None:
                self.every = self.line.every
        # if self.enrolments_until is None:
        #     self.enrolments_until = self.start_date
        # if self.id is not None:
        #     if self.enrolments_until is None:
        #         qs = self.get_existing_auto_events()
        #         if qs.count():
        #             self.enrolments_until = qs[0].start_date
        super(Course, self).full_clean(*args, **kw)

    def before_auto_event_save(self, event):
        """
        Sets room and start_time for automatic events.
        This is a usage example for
        :meth:`EventGenerator.before_auto_event_save
        <lino_xl.lib.cal.models.EventGenerator.before_auto_event_save>`.
        """
        #~ logger.info("20131008 before_auto_event_save")
        assert not settings.SITE.loading_from_dump
        assert event.owner == self
        #~ event = instance
        if event.is_user_modified():
            return
        #~ if event.is_fixed_state(): return
        #~ course = event.owner
        #~ event.project = self
        event.course = self
        event.room = self.room
        if self.slot:
            event.start_time = self.slot.start_time
            event.end_time = self.slot.end_time
        else:
            event.start_time = self.start_time
            event.end_time = self.end_time

    @dd.displayfield(_("Info"))
    def info(self, ar):
        if ar is None:
            return ''
        return ar.obj2html(self)
        # return unicode(self)

    #~ @dd.displayfield(_("Where"))
    #~ def where_text(self,ar):
        # ~ return unicode(self.room) # .company.city or self.company)

    @dd.displayfield(_("Events"))
    def events_text(self, ar=None):
        return ', '.join([
            dd.plugins.courses.day_and_month(e.start_date)
            for e in self.events_by_course.order_by('start_date')])

    @dd.displayfield(_("Free places"), max_length=5)
    def free_places(self, ar=None):
        if not self.max_places:
            return _("Unlimited")
        return str(self.get_free_places())

    @property
    def events_by_course(self):
        ct = rt.modules.contenttypes.ContentType.objects.get_for_model(
            self.__class__)
        return rt.modules.cal.Event.objects.filter(owner_type=ct, owner_id=self.id)

    @dd.requestfield(_("Requested"))
    def requested(self, ar):
        return rt.modules.courses.EnrolmentsByCourse.request(
            self, param_values=dict(state=EnrolmentStates.requested))

    @dd.requestfield(_("Confirmed"))
    def confirmed(self, ar):
        return rt.modules.courses.EnrolmentsByCourse.request(
            self, param_values=dict(state=EnrolmentStates.confirmed))

    @dd.requestfield(_("Enrolments"))
    def enrolments(self, ar):
        return rt.modules.courses.EnrolmentsByCourse.request(self)


# customize fields coming from mixins to override their inherited
# default verbose_names
dd.update_field(Course, 'every_unit', default=models.NOT_PROVIDED)
dd.update_field(Course, 'every', default=models.NOT_PROVIDED)


if FILL_EVENT_GUESTS:

    @dd.receiver(dd.post_save, sender=cal.Event,
                 dispatch_uid="fill_event_guests_from_course")
    def fill_event_guests_from_course(sender=None, instance=None, **kw):
        #~ logger.info("20130528 fill_event_guests_from_course")
        if settings.SITE.loading_from_dump:
            return
        event = instance
        if event.is_user_modified():
            return
        if event.is_fixed_state():
            return
        if not isinstance(event.owner, Course):
            return
        course = event.owner
        if event.guest_set.count() > 0:
            return
        for e in course.enrolment_set.all():
            cal.Guest(partner=e.pupil, event=event).save()


if False:

    class Option(mixins.BabelNamed):

        class Meta:
            app_label = 'courses'
            abstract = dd.is_abstract_model(__name__, 'Option')
            verbose_name = _("Enrolment option")
            verbose_name_plural = _('Enrolment options')

        course = dd.ForeignKey('courses.Course')

        price = dd.ForeignKey('products.Product',
                              verbose_name=_("Price"),
                              null=True, blank=True)

    class Options(dd.Table):
        model = 'courses.Option'
        required_roles = dd.required(dd.SiteStaff)
        stay_in_grid = True
        column_names = 'name price *'
        auto_fit_column_widths = True
        insert_layout = """
        name
        price
        """
        detail_layout = """
        name
        id course price
        EnrolmentsByOption
        """

    class OptionsByCourse(Options):
        master_key = 'course'
        required_roles = dd.required()


# ENROLMENT


class ConfirmedSubmitInsert(dd.SubmitInsert):
    def run_from_ui(self, ar, **kw):
        obj = ar.create_instance_from_request()
        msg = obj.get_confirm_veto(ar)
        if msg is None:
            obj.state = EnrolmentStates.confirmed
        self.save_new_instance(ar, obj)
        ar.set_response(close_window=True)


@dd.python_2_unicode_compatible
class Enrolment(UserAuthored, Certifiable, DatePeriod):
    """An **enrolment** is when a given pupil plans to participate in a
    given course.
    """
    invoiceable_date_field = 'request_date'
    workflow_state_field = 'state'

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Enrolment")
        verbose_name_plural = _('Enrolments')
        unique_together = ('course', 'pupil')

    course_area = CourseAreas.field(blank=True)

    #~ teacher = models.ForeignKey(Teacher)
    course = dd.ForeignKey('courses.Course')
    pupil = dd.ForeignKey(pupil_model)
    request_date = models.DateField(
        _("Date of request"), default=dd.today)
    state = EnrolmentStates.field(
        default=EnrolmentStates.requested.as_callable)
    places = models.PositiveIntegerField(
        pgettext("in a course", "Places used"),
        help_text=("The number of participants in this enrolment."),
        default=1)

    option = dd.ForeignKey(
        'products.Product', verbose_name=_("Option"),
        related_name='enrolments_by_option',
        blank=True, null=True)

    remark = models.CharField(_("Remark"), max_length=200, blank=True)
    confirmation_details = dd.RichTextField(
        _("Confirmation details"), blank=True,
        # format="html"
    )

    submit_insert = ConfirmedSubmitInsert()

    @dd.chooser()
    def course_choices(cls, course_area, request_date):
        if request_date is None:
            request_date = dd.today()
        flt = Q(enrolments_until__isnull=True)
        flt |= Q(enrolments_until__gte=request_date)
        qs = rt.modules.courses.Course.objects.filter(flt)
        if course_area:
            qs = qs.filter(line__course_area=course_area)
        # dd.logger.info("20160206 %s", qs.query)
        return qs

    @dd.chooser()
    def pupil_choices(cls, course):
        Pupil = dd.resolve_model(pupil_model)
        return Pupil.objects.all()

    def create_pupil_choice(self, text):
        """
        Called when an unknown pupil name was given.
        Try to auto-create it.
        """
        Pupil = dd.resolve_model(pupil_model)
        kw = parse_name(text)
        if len(kw) != 2:
            raise ValidationError(
                "Cannot find first and last names in %r to \
                auto-create pupil", text)
        p = Pupil(**kw)
        p.full_clean()
        p.save()
        return p

    @dd.chooser()
    def option_choices(cls, course):
        if not course.line or not course.line.options_cat:
            return []
        Product = rt.modules.products.Product
        return Product.objects.filter(cat=course.line.options_cat)

    def get_confirm_veto(self, ar):
        """Called from :class:`ConfirmEnrolment
        <lino_cosi.lib.courses.workflows.ConfirmEnrolment>`.  If this
        returns something else than `None`, then the enrolment won't
        be confirmed and the return value will be displayed to the
        user.

        """
        if self.course.max_places is None:
            return  # no veto. unlimited places.
        free = self.course.get_free_places(self)
        if free <= 0:
            return _("No places left in %s") % self.course
        #~ return _("Confirmation not implemented")

    def is_guest_for(self, event):
        """Return `True` if the pupil of this enrolment should be invited to
        the given event.

        """
        return self.state.uses_a_place

    def full_clean(self, *args, **kwargs):
        if not self.course_area:
            if self.course and self.course.line:
                self.course_area = self.course.line.course_area
        super(Enrolment, self).full_clean(*args, **kwargs)

    def get_print_templates(self, bm, action):
        return [self.state.name + bm.template_ext]

    def __str__(self):
        return "%s / %s" % (self.course, self.pupil)

    def get_print_language(self):
        return self.pupil.language

    def get_body_template(self):
        """Overrides :meth:`lino.core.model.Model.get_body_template`."""
        return self.course.line.body_template

    def get_excerpt_title(self):
        return self.course.line.get_excerpt_title()


from .ui import *
