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
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE -REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Produkte : Produkte, Produktkategorien
- Büro : Meine Auszüge, Mein E-Mail-Ausgang, Meine Uploads
- Verkauf : Verkaufsrechnungen (S)
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Finanzjournale : Bestbank (B), Kasse (C), Diverse Buchungen (M), MWSt-Erklärungen (V)
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - Büro : Meine Einfügetexte, Auszugsarten, Upload-Arten
  - System : Site-Parameter, Benutzer, Inhaltstypen, Hilfetexte
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Lieferarten
  - MWSt. : Zahlungsbedingungen
- Explorer :
  - Büro : Einfügetexte, Auszüge, E-Mail-Ausgänge, Anhänge, Uploads, Upload-Bereiche
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - SEPA : Konten
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses, MWSt.-Erklärungen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info
