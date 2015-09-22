.. _cosi.tested.ledger:

=======
Ledger
=======

.. include:: /include/tested.rst

.. to test only this document:

  $ python setup.py test -s tests.DocsTests.test_ledger


>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> import os
>>> import json
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.std.settings.demo'
>>> from lino.api.shell import *
>>> from django.test.client import Client
>>> from django.utils import translation
>>> ses = rt.login("robin")
>>> translation.activate('en')


Basic truths of accounting
==========================

- A purchases invoice credits the partner.
- A sales invoice debits the partner.
- The payment of a purchases invoice debits  the partner.
- The payment of a sales invoice credits the partner.

>>> ses.show(ledger.Journals, column_names="ref name trade_type account dc")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== =============================== ============ ================================ ========
 Reference            Designation                     Trade type   Account                          dc
-------------------- ------------------------------- ------------ -------------------------------- --------
 SLS                  Sales invoices                  Sales                                         Credit
 PRC                  Purchase invoices               Purchases                                     Debit
 BNK                  Bestbank                        Purchases    (5500) Bestbank                  Debit
 PMO                  Payment Orders                  Purchases    (5810) Payment Orders Bestbank   Debit
 CSH                  Cash                                         (5700) Cash                      Debit
 MSG                  Miscellaneous Journal Entries                (5700) Cash                      Debit
 VAT                  VAT declarations                             (4513) VAT to declare            Debit
 **Total (7 rows)**                                                                                 **6**
==================== =============================== ============ ================================ ========
<BLANKLINE>

Match rules
===========

A **match rule** specifies that a movement into given account can be
*cleared* using a given journal.

>>> ses.show(ledger.MatchRules)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==== ================== =====================================
 ID   Account            Journal
---- ------------------ -------------------------------------
 1    (4000) Customers   Sales invoices (SLS)
 2    (4400) Suppliers   Purchase invoices (PRC)
 3    (4000) Customers   Bestbank (BNK)
 4    (4400) Suppliers   Bestbank (BNK)
 5    (4000) Customers   Payment Orders (PMO)
 6    (4400) Suppliers   Payment Orders (PMO)
 7    (4000) Customers   Cash (CSH)
 8    (4400) Suppliers   Cash (CSH)
 9    (4000) Customers   Miscellaneous Journal Entries (MSG)
 10   (4400) Suppliers   Miscellaneous Journal Entries (MSG)
==== ================== =====================================
<BLANKLINE>


Debtors
=======

The table of debtors 

>>> ses.show(ledger.Debtors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ========= ==============
 Partner              ID        Balance
-------------------- --------- --------------
 Jacobs Jacqueline    136       999,95
 Johnen Johann        137       359,97
 **Total (2 rows)**   **273**   **1 359,92**
==================== ========= ==============
<BLANKLINE>


**Creditors** are partners hwo gave us credit. The most common
creditors are providers, i.e. partners who send us a purchase invoice.

>>> ses.show(ledger.Creditors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ========= ==============
 Partner               ID        Balance
--------------------- --------- --------------
 Rumma & Ko OÜ         100       40,40
 Bäckerei Ausdemwald   101       142,70
 Bäckerei Mießen       102       609,60
 Bäckerei Schmitz      103       1 211,90
 Garage Mergelsberg    104       3 274,08
 **Total (5 rows)**    **510**   **5 278,68**
===================== ========= ==============
<BLANKLINE>


Partner 136 has 2 open sales invoices:

>>> obj = contacts.Partner.objects.get(pk=136)
>>> ses.show(ledger.DebtsByPartner, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============ =========== ==========
 Due date             Balance      Debts       Payments
-------------------- ------------ ----------- ----------
 4/13/12              999,95       *SLS#130*
 **Total (1 rows)**   **999,95**
==================== ============ =========== ==========
<BLANKLINE>


