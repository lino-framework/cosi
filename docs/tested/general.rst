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
>>> from lino.api import dd, rt
>>> from lino.api.shell import *

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
- Verkauf : Verkaufsrechnungen (SLS)
- Einkauf : Einkaufsrechnungen (PRC)
- Finanzjournale : Bestbank (BNK), Zahlungsaufträge (PMO), Kasse (CSH), Diverse Buchungen (MSG), MWSt.-Erklärungen (VAT)
- Berichte :
  - System : Broken GFKs
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - System : Hilfetexte, Site-Parameter, Benutzer
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Büro : Upload-Arten, Auszugsarten
  - Verkauf : Lieferarten
  - MWSt. : Zahlungsbedingungen, MWSt-Regeln
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - SEPA : Konten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses, MWSt.-Erklärungen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge, Groupers
- Site : Info
