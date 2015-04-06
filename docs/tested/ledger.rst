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
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== =============================== ============ ================================ ========
 ref                  Designation                     Trade Type   Account                          dc
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

A **match rule** specifies that a movement into given account can
be cleared using a given journal.

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


Partner 112 has 2 open sales invoices:

>>> obj = contacts.Partner.objects.get(pk=112)
>>> ses.show(ledger.DebtsByPartner, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== =========== ========== ==========
 Due date             Balance     Debts      Payments
-------------------- ----------- ---------- ----------
 3/6/15               35,00       *SLS#13*
 **Total (1 rows)**   **35,00**
==================== =========== ========== ==========
<BLANKLINE>



Debtors
=======

The table of debtors 

>>> ses.show(ledger.Debtors, column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
============================= ==============
 Partner                       Balance
----------------------------- --------------
 *Arens Andreas*               35,00
 *Arens Annette*               65,00
 *Bäckerei Ausdemwald*         87,28
 *Rumma & Ko OÜ*               159,59
 *Altenberg Hans*              429,97
 *Ausdemwald Alfons*           79,99
 *Jacobs Jacqueline*           999,95
 *Johnen Johann*               359,97
 *Donderweer BV*               429,97
 *Van Achter NV*               79,99
 *Hans Flott & Co*             33,99
 *Bernd Brechts Bücherladen*   100,00
 *Reinhards Baumschule*        199,99
 *Moulin Rouge*                229,96
 *Auto École Verte*            113,97
 **Total (15 rows)**           **3 404,62**
============================= ==============
<BLANKLINE>


>>> ses.show(ledger.Creditors, column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
====================== ==============
 Partner                Balance
---------------------- --------------
 *Bäckerei Mießen*      495,62
 *Bäckerei Schmitz*     1 176,90
 *Garage Mergelsberg*   3 209,08
 **Total (3 rows)**     **4 881,60**
====================== ==============
<BLANKLINE>
