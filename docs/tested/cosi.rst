.. _cosi.tested.cosi:

Cosi
=======

.. include:: /include/tested.rst

>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.settings.demo'
>>> from lino.api.shell import *
>>> from lino import dd
>>> from django.test.client import Client

>>> print(settings.SETTINGS_MODULE)
lino_cosi.settings.test
>>> print([lng.name for lng in settings.SITE.languages])
[u'en', u'de', u'fr']



Printing invoices
-----------------

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> dd.translation.activate('en')
>>> obj = sales.Invoice.objects.get(pk=1)
>>> obj.clear_cache()
>>> print(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
{'success': True, 
'open_url': u'/media/userdocs/appyodt/sales.Invoice-1.odt', 
'message': u'sales.Invoice-1.odt has been built.', 
'refresh': True}

Note that this test should fail if you run the test suite without a 
LibreOffice server running.


