.. _cosi.tested.general:

General
=======

..  to test only this document:

    $ python setup.py test -s tests.DocsTests.test_general

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
- Buchhaltung :
  - Verkauf : Verkaufsrechnungen (SLS)
  - Einkauf : Einkaufsrechnungen (PRC)
  - Finanzjournale : Bestbank (BNK), Zahlungsaufträge (PMO), Kasse (CSH), Diverse Buchungen (MSG), MwSt.-Erklärungen (VAT)
- Berichte :
  - System : Broken GFKs
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontenpläne, Kontengruppen, Konten, Journale, Zahlungsbedingungen
  - Büro : Upload-Arten, Auszugsarten
  - MwSt. : MwSt-Regeln
  - Verkauf : Lieferarten
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - SEPA : Konten, Statements, Bewegungen
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge
  - Buchhaltung : Befriedigungsregeln, Belege, Belegarten, Bewegungen, Geschäftsjahre, Handelsarten
  - MwSt. : MwSt.-Regimes, MwSt.-Klassen, MwSt.-Erklärungen
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge, Groupers
- Site : Info
