.. _cosi.tested.sales:

=========================================
Sales
=========================================

.. This document is part of the Lino Così test suite. To run only this
   test:

    $ python setup.py test -s tests.DocsTests.test_sales
    
    doctest init:

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.std.settings.doctests'
    >>> from lino.api.doctest import *
    >>> ses = rt.login('robin')


>>> mt = 26
>>> url = '/api/sales/InvoicesByJournal/20'
>>> url += '?mt={0}&mk=1&an=detail&fmt=json'.format(mt)
>>> res = test_client.get(url, REMOTE_USER='robin')
>>> r = check_json_result(res, "navinfo data disable_delete id title")
>>> r['title']
u'Sales invoices (SLS) \xbb SLS#20'
