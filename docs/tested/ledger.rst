.. _cosi.tested.ledger:

=======
Ledger
=======

This document introduces some basic features of accounting.

.. to test only this document:

      $ python setup.py test -s tests.DocsTests.test_ledger
    
    doctest init:

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


For example a payment order can be used to pay an open suppliers
invoice or (less frequently) to send back money that a customer had
paid too much.

>>> jnl = ledger.Journal.objects.get(ref="PMO")
>>> jnl
Journal #4 (u'Payment Orders (PMO)')
>>> rt.show(ledger.MatchRulesByJournal, jnl)
==================
 Account
------------------
 (4000) Customers
 (4400) Suppliers
==================
<BLANKLINE>

Or a sales invoice can be used to clear another sales invoice.

>>> jnl = ledger.Journal.objects.get(ref="SLS")
>>> jnl
Journal #1 (u'Sales invoices (SLS)')
>>> rt.show(ledger.MatchRulesByJournal, jnl)
==================
 Account
------------------
 (4000) Customers
==================
<BLANKLINE>



Debtors
=======

The table of debtors 

>>> ses.show(ledger.Debtors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
===================== ========= ==============
 Partner               ID        Balance
--------------------- --------- --------------
 Bäckerei Ausdemwald   101       3,32
 Garage Mergelsberg    104       3,30
 Jacobs Jacqueline     136       999,95
 Johnen Johann         137       359,97
 **Total (4 rows)**    **478**   **1 366,54**
===================== ========= ==============
<BLANKLINE>


**Creditors** are partners hwo gave us credit. The most common
creditors are providers, i.e. partners who send us a purchase invoice.

>>> ses.show(ledger.Creditors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
=================================== ========== ===============
 Partner                             ID         Balance
----------------------------------- ---------- ---------------
 Rumma & Ko OÜ                       100        0,70
 Bäckerei Mießen                     102        2,59
 Bäckerei Schmitz                    103        0,70
 Arens Andreas                       112        999,95
 Arens Annette                       113        359,97
 Altenberg Hans                      114        289,92
 Ausdemwald Alfons                   115        70,00
 Bastiaensen Laurent                 116        245,00
 Collard Charlotte                   117        4 569,70
 Chantraine Marc                     119        359,97
 Charlier Ulrike                     118        999,95
 Demeulenaere Dorothée               121        70,00
 Dericum Daniel                      120        289,92
 Dobbelstein-Demeulenaere Dorothée   122        245,00
 Dobbelstein Dorothée                123        4 569,70
 Ernst Berta                         124        999,95
 Evertz Bernd                        125        359,97
 Emonts Daniel                       127        70,00
 Evers Eberhart                      126        289,92
 Engels Edgar                        128        245,00
 Faymonville Luc                     129        4 569,70
 Gernegroß Germaine                  130        999,95
 Groteclaes Gregory                  131        359,97
 Hilgers Henri                       133        70,00
 Hilgers Hildegard                   132        289,92
 Ingels Irene                        134        245,00
 Jansen Jérémy                       135        4 569,70
 **Total (27 rows)**                 **3269**   **26 142,15**
=================================== ========== ===============
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



