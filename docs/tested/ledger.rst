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
    >>> import lino
    >>> lino.startup('lino_cosi.projects.std.settings.demo')
    >>> from lino.api.doctest import *
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

**Debtors** are partners who received credit from us and thereefore
are in debt towards us. The most common debtors are customers,
i.e. partners who received a sales invoice from us (and did not yet
pay that invoice).

>>> ses.show(ledger.Debtors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ========= ==============
 Partner              ID        Balance
-------------------- --------- --------------
 Kaivers Karl         140       2 999,85
 Lambertz Guido       141       2 039,82
 Malmendier Marc      145       679,81
 Mießen Michael       147       280,00
 Emonts Erich         149       3 854,78
 **Total (5 rows)**   **722**   **9 854,26**
==================== ========= ==============
<BLANKLINE>


**Creditors** are partners hwo gave us credit. The most common
creditors are providers, i.e. partners who send us a purchase invoice
(which we did not yet pay).

>>> ses.show(ledger.Creditors, column_names="partner partner_id balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== ========= ==============
 Partner              ID        Balance
-------------------- --------- --------------
 AS Express Post      181       41,10
 AS Matsalu Veevärk   182       143,40
 Eesti Energia AS     183       5 045,18
 **Total (3 rows)**   **546**   **5 229,68**
==================== ========= ==============
<BLANKLINE>


Partner 149 has 2 open sales invoices:

>>> obj = contacts.Partner.objects.get(pk=149)
>>> ses.show(ledger.DebtsByPartner, obj)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
==================== ============== ========== ==========
 Due date             Balance        Debts      Payments
-------------------- -------------- ---------- ----------
 5/10/15              535,00         *SLS#43*
 5/11/15              3 319,78       *SLS#44*
 **Total (2 rows)**   **3 854,78**
==================== ============== ========== ==========
<BLANKLINE>



