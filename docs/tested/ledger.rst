.. _cosi.tested.ledger:

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
>>> from lino.runtime import *
>>> from django.test.client import Client
>>> from django.utils import translation
>>> ses = rt.login("robin")
>>> translation.activate('en')


Basic truths of accounting
--------------------------

- A purchases invoice credits the partner.
- A sales invoice debits the partner.
- The payment of a purchases invoice debits  the partner.
- The payment of a sales invoice credits the partner.

>>> ses.show(ledger.Journals, column_names="ref name trade_type account dc")
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

The table of debtors is currently very long because demo_bookings
currently doesn't generate any BankStatements:

>>> ses.show(ledger.Debtors, column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
======================================= ===============
 Partner                                 Balance
--------------------------------------- ---------------
 **Arens Andreas**                       1 034,95
 **Arens Annette**                       424,97
 **Altenberg Hans**                      719,89
 **Bastiaensen Laurent**                 245,00
 **Collard Charlotte**                   4 569,70
 **Ausdemwald Alfons**                   149,99
 **Charlier Ulrike**                     999,95
 **Chantraine Marc**                     359,97
 **Dericum Daniel**                      289,92
 **Demeulenaere Dorothée**               70,00
 **Dobbelstein-Demeulenaere Dorothée**   245,00
 **Dobbelstein Dorothée**                4 569,70
 **Ernst Berta**                         999,95
 **Evertz Bernd**                        359,97
 **Evers Eberhart**                      289,92
 **Emonts Daniel**                       70,00
 **Engels Edgar**                        245,00
 **Faymonville Luc**                     4 569,70
 **Gernegroß Germaine**                  999,95
 **Groteclaes Gregory**                  359,97
 **Hilgers Hildegard**                   289,92
 **Hilgers Henri**                       70,00
 **Ingels Irene**                        245,00
 **Jansen Jérémy**                       4 569,70
 **Jacobs Jacqueline**                   999,95
 **Johnen Johann**                       359,97
 **Jonas Josef**                         289,92
 **Jousten Jan**                         70,00
 **Kaivers Karl**                        245,00
 **Lambertz Guido**                      4 569,70
 **Laschet Laura**                       999,95
 **Lazarus Line**                        359,97
 **Malmendier Marc**                     70,00
 **Leffin Josefine**                     289,92
 **Meessen Melissa**                     245,00
 **Emonts Erich**                        359,97
 **Mießen Michael**                      4 569,70
 **Meier Marie-Louise**                  999,95
 **Emonts-Gast Erna**                    70,00
 **Emontspool Erwin**                    289,92
 **Radermacher Alfons**                  245,00
 **Radermacher Berta**                   4 569,70
 **Radermacher Christian**               999,95
 **Radermacher Daniela**                 359,97
 **Radermacher Edgard**                  289,92
 **Radermacher Fritz**                   70,00
 **Donderweer BV**                       429,97
 **Van Achter NV**                       79,99
 **Hans Flott & Co**                     33,99
 **Bernd Brechts Bücherladen**           100,00
 **Reinhards Baumschule**                199,99
 **Moulin Rouge**                        229,96
 **Auto École Verte**                    113,97
 **Total (53 rows)**                     **49 259,45**
======================================= ===============
<BLANKLINE>


>>> ses.show(ledger.Creditors, column_names="partner balance")
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
========================= ================
 Partner                   Balance
------------------------- ----------------
 **Rumma & Ko OÜ**         957,41
 **Bäckerei Ausdemwald**   3 768,34
 **Bäckerei Mießen**       16 863,36
 **Bäckerei Schmitz**      33 831,60
 **Garage Mergelsberg**    91 364,04
 **Total (5 rows)**        **146 784,75**
========================= ================
<BLANKLINE>
