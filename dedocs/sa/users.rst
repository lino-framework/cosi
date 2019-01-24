.. doctest tera_de/sa/users.rst
.. include:: /../docs/shared/include/defs.rst
.. init

    >>> from lino import startup
    >>> startup('lino_book.projects.lydia.settings.doctests')
    >>> from lino.api.doctest import *
    >>> from django.db import models

==================
Benutzerverwaltung
==================

Um die Liste der Benutzer und ihrer Zugriffsrechte zu sehen und zu verwalten,
wähle im Menü :menuselection:`Konfigurierung --> System --> Benutzer`.

Um einen **neuen Benutzer** anzulegen, klicke in der Werkzeugleiste auf |insert|.

Der **Benutzername** ist der Name, mit dem der Benutzer sich anmeldet. Lino
stellt keine besonderen Bedingungen an den Benutzernamen.  Üblich sind
kleinbuchstaben und ein Punkt zum Trennen von Vor- und Nachname.  Für einen
Benutzer Max Mustermann zum Beispiel wären Benutzernamen denkbar:
``max.mustermann``, ``m.mustermann``, ``mm``, ``max``.

NB: Die existierenden Benutzernamen `xy@Eupen` sind aus TIM importiert, und wir
haben noch nicht definitiv beschlossen, was mit denen geschehen soll. Momentan
werden sie nicht benutzt.

Man kann den Benutzernamen eines bestehenden Benutzers ändern. Falls der
Benutzer gerade in Lino arbeitet, würde er wohl Fehlermeldungen kriegen und
sich neu anmelden müssen.

Man kann den Benutzernamen eines bestehenden Benutzers auf leer setzen und dann
kann dieser Benutzer sich nicht mehr anmelden.

Die **Benutzerart** entscheidet über die Zugriffsrechte des
Benutzers.  Wenn das Feld leer ist kann der Benutzer sich nicht
anmelden.

Das **ID** ist die interne Benutzernummer und das, was einen Benutzer
identifiziert.

Einen **Benutzer löschen** kann man nur, wenn es keine Datenobjekte in der
Datenbank gibt, die auf diese Benutzernummer verweisen.
  
Alle anderen Felder können die Benutzer auch selber ändern.
Siehe :doc:`/basics/settings`.

Der Systemverwalter kann bei jedem Benutzer auf den Button mit dem Asterisk (✱)
klicken und dessen Passwort ändern.



Bearbeitungssperren
===================

In manchen Tabellen darf man nicht einfach wild drauflos bearbeiten,
sondern man muss im Detail-Fenster zuerst auf „Bearbeiten“ klicken, um
die Datenfelder bearbeiten zu können. Das dient dazu, unbeabsichtigte
konkurrierende Änderungen zu vermeiden, d.h. dass zwei Benutzer
gleichzeitig den gleichen Datensatz verändern.

Durch Klick auf „Bearbeiten“ wird eine sogenannte Bearbeitungssperre
angefragt : die Datenfelder, die bisher schreibgeschützt waren, sind
jetzt bearbeitbar. Der Button „Bearbeiten“ hat sich nach „Abbrechen“
verändert. Wenn man auf Speichern klickt, wird diese Sperre
automatisch wieder aufgehoben. Falls man es sich anders überlegt und
seine Änderungen nicht speichern will, sollten man Abbrechen klicken.
Wenn man das unveränderte Formular verlässt, ohne auf Abrrechen zu
klicken, kann es passieren, dass die Sperre aktiv bleibt (weil es für
Lino nicht immer leicht ist rauszufinden, ob du nicht in Wirklichkeit
nur eine Tasse Kaffee trinken gegangen bist).
