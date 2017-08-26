"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = "lino_cosi.projects.std.settings.test"

from unipath import Path
from lino.utils.pythontest import TestCase
import lino_cosi


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent
    django_settings_module = 'lino_cosi.projects.std.settings.test'


class CodeTests(TestCase):

    def test_packages(self):
        self.run_packages_test(lino_cosi.SETUP_INFO['packages'])


# class DemoTests(TestCase):

#     def test_std(self):
#         self.run_django_manage_test('lino_cosi/projects/std')

