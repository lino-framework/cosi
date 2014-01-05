.. _cosi.tested.general:

General
=======

.. include:: /include/tested.rst

The following statements import a set of often-used global names::

>>> from __future__ import print_function
>>> import json
>>> from pprint import pprint
>>> from django.conf import settings
>>> from django.utils import translation
>>> from django.test.client import Client
>>> from lino import dd
>>> from lino.runtime import *

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify here that the demo database 
has 23 pupils and 7 teachers:

>>> contacts.Person.objects.count()
69
>>> contacts.Company.objects.count()
12


The test database
-----------------

Test whether :meth:`get_db_overview_rst 
<lino_site.Site.get_db_overview_rst>` returns the expected result:

>>> print(settings.SITE.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
15 applications: about, contenttypes, system, users, countries, contacts, products, accounts, ledger, vat, declarations, sales, finan, lino_cosi, djangosite.
39 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           13        12
 accounts.Chart             4         1
 accounts.Group             7         6
 contacts.Company           27        12
 contacts.CompanyType       7         16
 contacts.Partner           23        81
 contacts.Person            28        69
 contacts.Role              4         0
 contacts.RoleType          4         5
 contenttypes.ContentType   4         40
 countries.Country          6         8
 countries.Place            8         75
 declarations.Declaration   18        0
 finan.BankStatement        12        27
 finan.BankStatementItem    11        178
 finan.JournalEntry         10        0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         12        27
 finan.PaymentOrderItem     10        162
 ledger.AccountInvoice      18        140
 ledger.InvoiceItem         9         224
 ledger.Journal             17        7
 ledger.Movement            9         890
 ledger.Voucher             8         260
 products.Product           12        12
 products.ProductCat        5         2
 sales.Invoice              26        66
 sales.InvoiceItem          13        130
 sales.InvoicingMode        8         1
 sales.PaymentTerm          7         0
 sales.SalesRule            4         0
 sales.ShippingMode         5         0
 system.HelpText            4         2
 system.SiteConfig          10        1
 system.TextFieldTemplate   6         2
 users.Authority            3         0
 users.Membership           3         0
 users.Team                 4         0
 users.User                 13        3
========================== ========= =======
<BLANKLINE>



User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Gruppen, Partner
- Produkte : Produkte, Produktkategorien
- Verkauf : Verkaufsrechnungen (S)
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Financial : Bestbank (B), Cash (C), Miscellaneous Journal Entries (M), VAT declarations (V)
- Berichte :
  - Buchhaltung : Tätigkeitsbericht, Debtors, Creditors
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - System : Site-Parameter, Benutzer, Teams, Inhaltstypen, Hilfetexte
  - Kontakte : Länder, Orte, Gruppenarten, Funktionen
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Fakturationsmodi, Lieferarten, Zahlungsbedingungen
- Explorer :
  - Büro : Einfügetexte
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses, MWSt.-Erklärungen
  - Financial : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info

