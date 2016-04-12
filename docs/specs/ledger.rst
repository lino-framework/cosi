.. _cosi.specs.ledger:
.. _cosi.tested.ledger:

===================================================
The :mod:`lino_cosi.lib.ledger` plugin (Accounting)
===================================================

.. to test only this document:

      $ python setup.py test -s tests.DocsTests.test_ledger
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_cosi.projects.std.settings.demo')
    >>> from lino.api.doctest import *
    >>> ses = rt.login("robin")
    >>> translation.activate('en')

This document describes some basic features of "general accounting"
implemented by the :mod:`lino_cosi.lib.ledger` plugin.

This document is based on the following specifications:

- :ref:`cosi.specs.accounting`



.. contents::
   :depth: 1
   :local:


Basic truths of accounting
==========================

- A purchase invoice credits the partner account.
- A sales invoice debits the partner account.
- The payment of a purchases invoice debits the partner account.
- The payment of a sales invoice credits the partner account.

>>> ses.show(ledger.Journals,
...     column_names="ref name trade_type account dc")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========== =============================== ============ ================================ ===========================
 Reference   Designation                     Trade type   Account                          Primary booking direction
----------- ------------------------------- ------------ -------------------------------- ---------------------------
 SLS         Sales invoices                  Sales                                         Credit
 PRC         Purchase invoices               Purchases                                     Debit
 BNK         Bestbank                        Purchases    (5500) Bestbank                  Debit
 PMO         Payment Orders                  Purchases    (5810) Payment Orders Bestbank   Debit
 CSH         Cash                                         (5700) Cash                      Debit
 MSG         Miscellaneous Journal Entries                (5700) Cash                      Debit
=========== =============================== ============ ================================ ===========================
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
Journal #4 ('Payment Orders (PMO)')

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
Journal #1 ('Sales invoices (SLS)')
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
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== ============== ========== ==========
 Due date             Balance        Debts      Payments
-------------------- -------------- ---------- ----------
 5/10/15              535,00         *SLS 23*
 5/11/15              3 319,78       *SLS 24*
 **Total (2 rows)**   **3 854,78**
==================== ============== ========== ==========
<BLANKLINE>



Fiscal years
============

Each ledger movement happens in a given **fiscal year**.  Lino has a
table with **fiscal years**.

In a default configuration there is one fiscal year for each calendar
year between :attr:`start_year
<lino_cosi.lib.ledger.Plugin.start_year>` and ":func:`today
<lino.core.site.Site.today>` plus 5 years".

>>> dd.plugins.ledger.start_year
2015

>>> dd.today().year + 5
2020

>>> rt.show(ledger.FiscalYears)
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======= ====== ======
 value   name   text
------- ------ ------
 15             2015
 16             2016
 17             2017
 18             2018
 19             2019
 20             2020
======= ====== ======
<BLANKLINE>


Accounting periods
==================

Each ledger movement happens in a given **accounting period**.  
An accounting period usually corresponds to a month of the calendar.
Accounting periods are automatically created the first time they are
needed by some operation.


>>> rt.show(ledger.AccountingPeriods)
=========== ============ ========== ============= ======= ========
 Reference   Start date   End date   Fiscal Year   State   Remark
----------- ------------ ---------- ------------- ------- --------
 2015-01     1/1/15       1/31/15    2015          Open
 2015-02     2/1/15       2/28/15    2015          Open
 2015-03     3/1/15       3/31/15    2015          Open
 2015-04     4/1/15       4/30/15    2015          Open
 2015-05     5/1/15       5/31/15    2015          Open
=========== ============ ========== ============= ======= ========
<BLANKLINE>

The *reference* of a new accounting period is computed by applying the
voucher's entry date to the template defined in the
:attr:`date_to_period_tpl
<lino_cosi.lib.ledger.models.AccountingPeriod.get_for_date>` setting.  
The default implementation leads to the following references:

>>> print(ledger.AccountingPeriod.get_ref_for_date(i2d(19940202)))
1994-02
>>> print(ledger.AccountingPeriod.get_ref_for_date(i2d(20150228)))
2015-02
>>> print(ledger.AccountingPeriod.get_ref_for_date(i2d(20150401)))
2015-04

You may manually create other accounting periods. For example

- `2015-00` might stand for a fictive "opening" period before January
  2015 and after December 2014.

- `2015-13` might stand for January 2016 in a company which is
  changing their fiscal year from "January-December" to "July-June".



