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
    def test_sample_ibans(self):
        self.run_simple_doctests('lino_cosi/lib/sepa/fixtures/sample_ibans.py')

    def test_febelfin(self):
        self.run_simple_doctests('lino_cosi/lib/b2c/febelfin.py')


class DocsTests(BaseTestCase):
    # def test_cosi(self):
    #     return self.run_docs_doctests('tested/cosi.rst')

    def test_accounting(self):
        self.run_simple_doctests('docs/specs/accounting.rst')

    def test_packages(self):
        self.run_packages_test(lino_cosi.SETUP_INFO['packages'])

    def test_est(self):
        self.run_simple_doctests('docs/specs/est.rst')

    def test_sales(self):
        self.run_simple_doctests('docs/specs/sales.rst')

    def test_bel_de(self):
        self.run_simple_doctests('docs/specs/bel_de.rst')

    def test_demo(self):
        self.run_simple_doctests('docs/specs/demo.rst')

    def test_ledger(self):
        self.run_simple_doctests('docs/specs/ledger.rst')

    def test_general(self):
        return self.run_simple_doctests('docs/specs/general.rst')

    def test_contacts(self):
        return self.run_simple_doctests('docs/specs/contacts.rst')

    def test_tim2lino(self):
        return self.run_simple_doctests('docs/specs/tim2lino.rst')


class DemoTests(TestCase):

    def test_std(self):
        self.run_django_manage_test('lino_cosi/projects/std')


class DjangoTests(BaseTestCase):
    """
    $ python setup.py test -s tests.DemoTests.test_admin
    """

    def test_admin(self):
        self.run_django_manage_test('lino_cosi/projects/apc')
        self.run_django_manage_test('lino_cosi/projects/ylle')
        # self.run_django_manage_test('lino_cosi/projects/std/settings/start')

