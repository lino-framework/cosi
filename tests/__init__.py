"""
Examples how to run these tests::

  $ python setup.py test
  $ python setup.py test -s tests.DocsTests
  $ python setup.py test -s tests.DocsTests.test_debts
  $ python setup.py test -s tests.DocsTests.test_docs
"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "lino_cosi.settings.test"

from unipath import Path
from djangosite.utils.pythontest import TestCase
import lino_cosi


class BaseTestCase(TestCase):
    project_root = Path(__file__).parent.parent
    demo_settings_module = 'lino_cosi.settings.test'


class DocsTests(BaseTestCase):
    # def test_cosi(self):
    #     return self.run_docs_doctests('tested/cosi.rst')

    # def test_general(self):
    #     return self.run_docs_doctests('tested/general.rst')

    def test_packages(self):
        self.run_packages_test(lino_cosi.SETUP_INFO['packages'])

    def test_est(self):
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

