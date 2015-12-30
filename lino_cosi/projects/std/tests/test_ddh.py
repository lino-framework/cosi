# -*- coding: utf-8 -*-
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

"""Runs some tests about the disable-delete handler and cascading deletes.

Reproduces :ticket:`582`.

You can run only these tests by issuing::

  $ go cosi
  $ cd lino_cosi/projects/std
  $ python manage.py test tests.test_ddh

Or::

  $ python setup.py test -s tests.DemoTests.test_std

"""

from __future__ import unicode_literals
from __future__ import print_function

from django.core.exceptions import ValidationError
from lino.utils.djangotest import RemoteAuthTestCase
from lino.api import rt
from lino.utils.mti import delete_child


def create(m, **kwargs):
    obj = m(**kwargs)
    obj.full_clean()
    obj.save()
    return obj
    

class DDHTests(RemoteAuthTestCase):
    maxDiff = None

    def test01(self):
        from lino.modlib.users.choicelists import UserProfiles
        User = rt.modules.users.User
        Partner = rt.modules.contacts.Partner
        Person = rt.modules.contacts.Person
        Company = rt.modules.contacts.Company
        Role = rt.modules.contacts.Role
        Account = rt.modules.sepa.Account
        Invoice = rt.modules.vat.VatAccountInvoice
        Journal = rt.modules.ledger.Journal
        VoucherTypes = rt.modules.ledger.VoucherTypes
        JournalGroups = rt.modules.ledger.JournalGroups

        u = User(username='robin',
                 profile=UserProfiles.admin,
                 language="en")
        u.save()

        def createit():
            obj = Person(first_name="John", last_name="Doe")
            obj.full_clean()
            obj.save()
            pk = obj.pk
            return (obj, Partner.objects.get(pk=pk))

        #
        # If there are no vetos, user can ask to delete from any MTI form
        #
        pe, pa = createit()
        pe.delete()

        pe, pa = createit()
        pa.delete()

        #
        # Cascade-related objects (e.g. addresses) are deleted
        # independently of the polymorphic form which initiated
        # deletion.
        #

        def check_cascade(model):
            pe, pa = createit()
            obj = model.objects.get(pk=pa.pk)
            rel = Account(partner=pa, iban="AL32293653370340154130927280")
            rel.full_clean()
            rel.save()
            obj.delete()
            self.assertEqual(Account.objects.count(), 0)

        check_cascade(Partner)
        check_cascade(Person)

        #
        # Vetos of one form are deteced by all other forms.
        #
        def check_veto(obj, expected):
            try:
                obj.delete()
                self.fail("Failed to raise Warning({0})".format(expected))
            except Warning as e:
                self.assertEqual(str(e), expected)

        VKR = create(
            Journal,
            ref="VKR", name="VKR",
            voucher_type=VoucherTypes.get_for_model(Invoice),
            journal_group=JournalGroups.sales)
        
        pe, pa = createit()

        def check_vetos(obj, msg):
            m = obj.__class__
            obj.full_clean()
            obj.save()
            check_veto(pa, msg)
            check_veto(pe, msg)
            self.assertEqual(m.objects.count(), 1)
            obj.delete()
            self.assertEqual(m.objects.count(), 0)

        msg = "Cannot delete Partner Doe John because 1 Invoices refer to it."
        check_vetos(Invoice(partner=pa, journal=VKR), msg)

        #
        # Having an invoice does not prevent from removing the Person
        # child of the partner.
        #
        
        invoice = create(Invoice, partner=pa, journal=VKR)
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 1)
        self.assertEqual(Invoice.objects.count(), 1)

        delete_child(pa, Person)

        # tidy up:
        self.assertEqual(Partner.objects.count(), 1)
        self.assertEqual(Person.objects.count(), 0)
        invoice.delete()
        pa.delete()
        self.assertEqual(Partner.objects.count(), 0)

        # But Lino refuses to remove the Person child if it has vetos.
        # For example if the person form is being used as a contact person.

        pe, pa = createit()
        co = create(Company, name="Test")
        create(Role, company=co, person=pe)
        msg = "[u'Cannot delete Partner Doe John because " \
              "1 Contact Persons refer to it.']"
        try:
            delete_child(pa, Person)
            self.fail("Expected ValidationError")
        except ValidationError as e:
            self.assertEqual(str(e), msg)

