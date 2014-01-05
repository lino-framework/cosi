.. _cosi.tested.cosi:

Cosi
=======

.. include:: /include/tested.rst

>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from django.conf import settings
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> from django.utils.translation import get_language
>>> from django.utils import translation
>>> import json

>>> print(settings.SETTINGS_MODULE)
lino_cosi.settings.test
>>> print([lng.name for lng in settings.SITE.languages])
[u'en', u'de', u'fr']



Printing invoices
-----------------

We take a sales invoice, clear the cache, ask Lino to print it and 
check whether we get the expected response.

>>> ses = settings.SITE.login("robin")
>>> translation.activate('en')
>>> obj = sales.Invoice.objects.get(pk=1)
>>> obj.clear_cache()
>>> print(ses.run(obj.do_print)) #doctest: +NORMALIZE_WHITESPACE +ELLIPSIS
{'refresh': True, 'open_url': u'/media/cache/appypdf/sales.Invoice-1.pdf', 
'message': u'S#1 printable has been built.', 'success': True}

Note that this test should fail if you run the test suite without a 
LibreOffice server running.


Basic truths of accounting
--------------------------

- A purchases invoice creditates the partner.
- A sales invoice debitates the partner.
- The payment of a purchases invoice debitates  the partner.
- The payment of a sales invoice creditates the partner.

>>> ses.show(ledger.Journals,column_names="ref name trade_type account dc")
==================== =============================== ============ ====================================== ========
 ref                  Designation                     Trade Type   Account                                dc
-------------------- ------------------------------- ------------ -------------------------------------- --------
 S                    Sales invoices                  Sales                                               Credit
 P                    Purchase invoices               Purchases                                           Debit
 B                    Bestbank                                     (bestbank) Bestbank                    Debit
 PO                   Payment Orders                  Purchases    (bestbankpo) Payment Orders Bestbank   Debit
 C                    Cash                                         (cash) Cash                            Debit
 M                    Miscellaneous Journal Entries                                                       Debit
 **Total (6 rows)**                                                                                       **5**
==================== =============================== ============ ====================================== ========
<BLANKLINE>

