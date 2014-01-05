# -*- coding: UTF-8 -*-
## Copyright 2013 Luc Saffre
## This file is part of the Lino-Faggio project.
## Lino-Faggio is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino-Faggio is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino-Faggio; if not, see <http://www.gnu.org/licenses/>.

"""

To run only this test::

  $ go faggio
  $ python setup.py test -s tests.faggio_demo_tests

 

"""
from lino.utils.test import DemoTestCase
from django.contrib.contenttypes.models import ContentType
from lino.runtime import *

class MyTestCase(DemoTestCase):
    
    def test_001(self):
        
        json_fields = 'count rows title success no_data_text param_values'
        kw = dict(fmt='json',limit=10,start=0)
        mt = ContentType.objects.get_for_model(courses.Line).pk

        self.demo_get('rolf','api/courses/CoursesByLine',json_fields,4,mt=mt,mk=1,**kw)


