.. _cosi.tested.general:

General
=======

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_general

The following statements import a set of often-used global names::

>>> from __future__ import print_function
>>> from __future__ import unicode_literals
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.apc.settings.doctests'
>>> import json
>>> from lino import dd, rt
>>> from lino.runtime import *

User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('rolf') 
>>> with dd.translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Produkte : Produkte, Produktkategorien
- Büro : Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge
- Verkauf : Verkaufsrechnungen (S)
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Finanzjournale : Bestbank (B), Kasse (C), Diverse Buchungen (M), MWSt-Erklärungen (V)
- Berichte :
  - System : Broken GFKs
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - System : Hilfetexte, Site-Parameter, Benutzer
  - Büro : Meine Einfügetexte, Upload-Arten, Auszugsarten
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Lieferarten
  - MWSt. : Zahlungsbedingungen, MWSt-Regeln
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Büro : Einfügetexte, Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge
  - Kontakte : Kontaktpersonen
  - SEPA : Konten
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses, MWSt.-Erklärungen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge, Groupers
- Site : Info
