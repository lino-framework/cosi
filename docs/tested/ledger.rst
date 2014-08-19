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
==================== =============================== ============ ================================ ========
 ref                  Designation                     Trade Type   Account                          dc
-------------------- ------------------------------- ------------ -------------------------------- --------
 S                    Sales invoices                  Sales                                         Credit
 P                    Purchase invoices               Purchases                                     Debit
 B                    Bestbank                                     (5500) Bestbank                  Debit
 PO                   Payment Orders                  Purchases    (5810) Payment Orders Bestbank   Debit
 C                    Cash                                         (5700) Cash                      Debit
 M                    Miscellaneous Journal Entries                                                 Debit
 V                    VAT declarations                             (4513) VAT to declare            Debit
 **Total (7 rows)**                                                                                 **6**
==================== =============================== ============ ================================ ========
<BLANKLINE>



>>> ses.show(ledger.Debtors,column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
=============================== ==============
 Partner                         Balance
------------------------------- --------------
 **Arens Andreas**               35,00
 **Arens Annette**               65,00
 **Bäckerei Ausdemwald**         85,19
 **Rumma & Ko OÜ**               158,59
 **Altenberg Hans**              429,97
 **Ausdemwald Alfons**           79,99
 **Radermacher Daniela**         359,97
 **Radermacher Edgard**          289,92
 **Radermacher Fritz**           70,00
 **Donderweer BV**               429,97
 **Van Achter NV**               79,99
 **Hans Flott & Co**             33,99
 **Bernd Brechts Bücherladen**   100,00
 **Reinhards Baumschule**        199,99
 **Moulin Rouge**                229,98
 **Auto École Verte**            113,98
 **Total (16 rows)**             **2 761,53**
=============================== ==============
<BLANKLINE>


>>> ses.show(ledger.Creditors,column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
======================== ==============
 Partner                  Balance
------------------------ --------------
 **Bäckerei Mießen**      500,32
 **Bäckerei Schmitz**     1 189,50
 **Garage Mergelsberg**   3 242,18
 **Total (3 rows)**       **4 932,00**
======================== ==============
<BLANKLINE>


