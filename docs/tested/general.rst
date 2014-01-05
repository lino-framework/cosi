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
15 applications: about, contenttypes, system, users, countries, contacts, products, accounts, ledger, vat, sales, finan, lino_cosi, djangosite.
39 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           13        12
 accounts.Chart             4         1
 accounts.Group             7         6
 contacts.Company           27        19
 contacts.CompanyType       7         16
 contacts.Partner           23        88
 contacts.Person            29        69
 contacts.Role              4         0
 contacts.RoleType          4         5
 contenttypes.ContentType   4         68
 countries.Country          6         8
 countries.Place            8         75
 finan.BankStatement        11        3
 finan.BankStatementItem    11        21
 finan.JournalEntry         9         0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         11        3
 finan.PaymentOrderItem     10        18
 ledger.AccountInvoice      17        20
 ledger.InvoiceItem         9         32
 ledger.Journal             17        6
 ledger.Movement            9         113
 ledger.Voucher             7         45
 products.Product           12        8
 products.ProductCat        5         3
 sales.Invoice              25        19
 sales.InvoiceItem          15        31
 sales.InvoicingMode        8         0
 sales.PaymentTerm          7         0
 sales.SalesRule            4         0
 sales.ShippingMode         5         0
 system.HelpText            4         2
 system.SiteConfig          10        1
 system.TextFieldTemplate   6         2
 users.Authority            3         0
 users.Membership           3         0
 users.Team                 4         0
 users.User                 15        3
========================== ========= =======
<BLANKLINE>



User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Gruppen, Partner, Kursleiter, Teilnehmer
- Kurse : Kurse, Offene Einschreibungsanfragen, Auszustellende Teilnahmebescheinigungen
- Kalender : Kalender, Meine Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Buchungen
- Produkte : Produkte, Produktkategorien
- Verkauf : Verkaufsrechnungen (S), Zu fakturieren
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Financial : Bestbank (B), Cash (C), Miscellaneous Journal Entries (M)
- Büro : Meine Notizen, Mein E-Mail-Ausgang
- Berichte :
  - Buchhaltung : Tätigkeitsbericht
- Konfigurierung :
  - Büro : Meine Einfügetexte, Notizarten, Ereignisarten, Upload-Arten
  - System : Site-Parameter, Benutzer, Teams, Inhaltstypen, Hilfetexte
  - Kontakte : Länder, Orte, Gruppenarten, Funktionen
  - Kurse : Instructor Types, Participant Types, Themen, Kurs-Serien, Timetable Slots
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Termine, Gastrollen, Ereignisarten, Externe Kalender
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Fakturationsmodi, Lieferarten, Zahlungsbedingungen
- Explorer :
  - Büro : Einfügetexte, Notizen, Uploads, E-Mail-Ausgänge, Anhänge
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - Kurse : Einschreibungen, Einschreibungs-Zustände
  - Kalender : Aufgaben, Gäste, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses
  - Financial : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info

