.. _cosi.tested.ledger:

Ledger
=======

.. include:: /include/tested.rst

>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.runtime import *
>>> from lino import dd
>>> from django.test.client import Client
>>> ses = dd.login("robin")
>>> dd.translation.activate('en')


Basic truths of accounting
--------------------------

- A purchases invoice creditates the partner.
- A sales invoice debitates the partner.
- The payment of a purchases invoice debitates  the partner.
- The payment of a sales invoice creditates the partner.

>>> ses.show(ledger.Journals,column_names="ref name trade_type account dc")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
==================== =============================== ============ ====================================== ========
 ref                  Designation                     Trade Type   Account                                dc
-------------------- ------------------------------- ------------ -------------------------------------- --------
 S                    Sales invoices                  Sales                                               Credit
 P                    Purchase invoices               Purchases                                           Debit
 B                    Bestbank                                     (bestbank) Bestbank                    Debit
 PO                   Payment Orders                  Purchases    (bestbankpo) Payment Orders Bestbank   Debit
 C                    Cash                                         (cash) Cash                            Debit
 M                    Miscellaneous Journal Entries                                                       Debit
 V                    VAT declarations                             (vatdcl) VAT                           Debit
 **Total (7 rows)**                                                                                       **6**
==================== =============================== ============ ====================================== ========
<BLANKLINE>



>>> ses.show(ledger.Debtors,column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=============================== ==============
 Partner                         Balance
------------------------------- --------------
 **Arens Andreas**               35,00
 **Arens Annette**               65,00
 **Bäckerei Ausdemwald**         85,17
 **Rumma & Ko OÜ**               158,59
 **Altenberg Hans**              429,95
 **Ausdemwald Alfons**           79,99
 **Radermacher Daniela**         359,96
 **Radermacher Edgard**          289,92
 **Radermacher Fritz**           70,00
 **Donderweer BV**               429,95
 **Van Achter NV**               79,99
 **Hans Flott & Co**             33,98
 **Bernd Brechts Bücherladen**   100,00
 **Reinhards Baumschule**        199,99
 **Moulin Rouge**                229,96
 **Auto École Verte**            113,97
 **Total (16 rows)**             **2 761,42**
=============================== ==============
<BLANKLINE>


>>> ses.show(ledger.Creditors,column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================== ==============
 Partner                  Balance
------------------------ --------------
 **Bäckerei Mießen**      500,33
 **Bäckerei Schmitz**     1 189,50
 **Garage Mergelsberg**   3 242,18
 **Total (3 rows)**       **4 932,01**
======================== ==============
<BLANKLINE>

