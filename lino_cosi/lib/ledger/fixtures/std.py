# -*- coding: UTF-8 -*-
# Copyright 2012-2014 Luc Saffre
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

"""

from __future__ import unicode_literals

from lino.api import dd, rt, _
notes = dd.resolve_app('notes')


def objects():
    if False and notes:
        NoteType = dd.resolve_model('notes.NoteType')
        yield NoteType(
            template="Letter.odt",
            build_method="appyodt",
            body_template="payment_reminder.body.html",
            **dd.babel_values('name',
                              en="Payment reminder",
                              fr="Rappel de paiement",
                              de="Zahlungserinnerung"))

    ExcerptType = rt.modules.excerpts.ExcerptType
    ContentType = rt.modules.contenttypes.ContentType

    yield ExcerptType(
        body_template="payment_reminder.body.html",
        content_type=ContentType.objects.get_for_model(
            dd.resolve_model('contacts.Partner')),
        **dd.str2kw('name', _("Payment reminder")))
