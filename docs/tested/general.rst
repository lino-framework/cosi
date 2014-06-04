.. _cosi.tested.general:

General
=======

.. include:: /include/tested.rst

The following statements import a set of often-used global names::

>>> import json
>>> from lino import dd
>>> from lino.runtime import *

User profiles
-------------

Rolf is the local system administrator, he has a complete menu:

>>> ses = settings.SITE.login('rolf') 
>>> with dd.translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Produkte : Produkte, Produktkategorien
- Verkauf : Verkaufsrechnungen (S)
- Einkauf : Einkaufsrechnungen (P), Zahlungsaufträge (PO)
- Financial : Bestbank (B), Kasse (C), Diverse Buchungen (M), MWSt-Erklärungen (V)
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - Büro : Meine Einfügetexte
  - System : Site-Parameter, Benutzer, Inhaltstypen, Hilfetexte
  - Kontakte : Organisationsarten, Funktionen
  - Orte : Länder, Orte
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale
  - Verkauf : Lieferarten
  - MWSt. : Zahlungsbedingungen
- Explorer :
  - Büro : Einfügetexte
  - System : Vollmachten, Benutzergruppen, Benutzer-Levels, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - SEPA : Konten
  - Buchhaltung : Rechnungen, Belege, VoucherTypes, Bewegungen, Geschäftsjahre
  - MWSt. : VatRegimes, TradeTypes, VatClasses, MWSt.-Erklärungen
  - Financial : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info

