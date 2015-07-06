# -*- coding: utf-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

"""
This module contains "quick" tests that are run on a demo database
without any fixture. You can run only these tests by issuing::

  $ cd lino_projects/std
  $ python manage.py test

"""

from __future__ import unicode_literals
from __future__ import print_function

import logging
logger = logging.getLogger(__name__)

from lino.api.shell import *

from lino.utils.djangotest import RemoteAuthTestCase


class QuickTest(RemoteAuthTestCase):

    def test00(self):
        """
        Initialization.
        """
        #~ print "20130321 test00 started"
        self.user_root = settings.SITE.user_model(
            username='root', language='en', profile='900')
        self.user_root.save()

        #~ def test01(self):
        self.assertEqual(1 + 1, 2)
        o1 = contacts.Company(name="Example")
        o1.save()
        o2 = contacts.Company(name="Example")
        o2.save()

        p1 = contacts.Person(first_name="John", last_name="Doe")
        p1.save()
        p2 = contacts.Person(first_name="Johny", last_name="Doe")
        p2.save()

        contacts.Role(person=p1, company=o1).save()
        contacts.Role(person=p2, company=o2).save()

        #~ s = contacts.ContactsByOrganisation.request(o1).to_rst()
        s = contacts.RolesByCompany.request(o1).to_rst()
        #~ print('\n'+s)
        self.assertEqual(s, """\
========== ==============
 Person     Contact Role
---------- --------------
 John Doe
========== ==============
""")

        s = contacts.RolesByCompany.request(o2).to_rst()
        #~ print('\n'+s)
        self.assertEqual(s, """\
=========== ==============
 Person      Contact Role
----------- --------------
 Johny Doe
=========== ==============
""")
        url = "/api/contacts/Persons/115?fv=115&fv=fff&an=merge_row"
        #~ self.fail("TODO: execute a merge action using the web interface")
        res = self.client.get(url, REMOTE_USER='root')

        # 20130418 server traceback caused when a pdf view of a table
        # was requested through the web interface.  TypeError:
        # get_handle() takes exactly 1 argument (2 given)
        url = settings.SITE.buildurl(
            'api/countries/Countries?cw=189&cw=45&cw=45&cw=36&ch=&ch=&ch=&ch=&ch=&ch=&ci=name&ci=isocode&ci=short_code&ci=iso3&name=0&an=as_pdf')
        msg = 'Using remote authentication, but no user credentials found.'
        try:
            response = self.client.get(url)
            self.fail("Expected '%s'" % msg)
        except Exception as e:
            self.assertEqual(str(e), msg)

        response = self.client.get(url, REMOTE_USER='foo')
        self.assertEqual(response.status_code, 403,
                         "Status code for anonymous on GET %s" % url)
        from appy.pod import PodError

        """
        If oood is running, we get a 302, otherwise a PodError
        """
        try:
            response = self.client.get(url, REMOTE_USER='root')
            #~ self.assertEqual(response.status_code,200)
            result = self.check_json_result(response, 'success open_url')
            self.assertEqual(
                result['open_url'], "/media/cache/appypdf/127.0.0.1/countries.Countries.pdf")

        except PodError as e:
            pass
            #~ self.assertEqual(str(e), PodError: Extension of result file is "pdf".
