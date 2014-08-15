"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
from unipath import Path

ROOTDIR = Path(__file__).parent.parent

# load  SETUP_INFO:
execfile(ROOTDIR.child('lino_cosi','project_info.py'),globals())

from djangosite.utils.pythontest import TestCase

import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_cosi.settings.test"


class BaseTestCase(TestCase):
    project_root = ROOTDIR
    demo_settings_module = 'lino_cosi.settings.test'


class DocsTests(BaseTestCase):
    # def test_cosi(self):
    #     return self.run_docs_doctests('tested/cosi.rst')

    # def test_general(self):
    #     return self.run_docs_doctests('tested/general.rst')

    def test_packages(self):
        self.run_packages_test(SETUP_INFO['packages'])

    def test_demo(self):
        self.run_simple_doctests('docs/tested/est.rst')


class DjangoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """

    def test_admin(self):
        self.run_django_manage_test('lino_cosi/settings')
        self.run_django_manage_test('lino_cosi/settings/be')
        self.run_django_manage_test('lino_cosi/settings/est')
        self.run_django_manage_test('lino_cosi/settings/start')

