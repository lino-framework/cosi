.. include:: /../docs/shared/include/defs.rst

==================
Einkaufsrechnungen
==================

.. contents::
   :depth: 1
   :local:


Einkaufsrechnungen erfassen
===========================

Um eine neue Einkaufsrechnungen (EKR) zu erfassen, wähle im Hauptmenü
:menuselection:`Buchhaltung --> Einkauf --> Einkaufsrechnungen` und klicke dann
auf |insert| oder betätige die Taste :kbd:`Einfügen`.

Lino zeigt dann ein Dialogfenster mit den Feldern :guilabel:`Partner`,
:guilabel:`Buchungsdatum` und :guilabel:`Total inkl. MwSt.` (Details dazu siehe weiter unten).

Bestätige das Fenster mit :kbd:`Strg+S` oder klicke auf :guilabel:`Erstellen`.
Wenn du auf |close| klickst oder :kbd:`Escape` drückst, wird nichts in der
Datenbank verändert und das Fenster wieder geschlossen.

Wenn du bestätigt hast, erstellt Lino die Rechnung und zeigt sie dir im
Detail-Fenster an, wo du alle weitere Angaben eingibst.

Das Detail-Fenster einer Einkaufsrechnung
=========================================

Dieses Fenster zeigt dir alle Angaben zu einer bestimmten Rechnung an. Alles,
was du hier tust, bezieht sich auf diese eine Rechnung.  Von hier aus kannst du
diese Rechnung ändern, registrieren, ausdrucken, löschen...


Der **Partner** einer EKR ist der Lieferant, der euch die Rechnung geschickt
hat. Das ist üblicherweise eine Firma oder Organisation, kann aber potentiell
auch eine Einzelperson oder eine andere Partnerart sein.

Das **Buchungsdatum** ist fast immer das gleiche wie das Rechnungsdatum.
Ausnahme: Wenn eine Rechnung in einem anderen Kalenderjahr gebucht wird, dann
muss als Buchungsdatum der 01.01. oder 31.12. des Jahres genommen werden, in
dem sie verbucht werden soll.

In **Total inkl. MWSt.** gib den Gesamtbetrag der Rechnung ein. Lino wird
diesen Betrag ggf. im folgenden Bildschirm verteilen.




Hier hat Lino den Gesamtbetrag so gut es ging aufgeteilt. Im Idealfall
kannst du hier auf "Registriert" klicken, um die Rechnung zu
registrieren. Und dann wieder auf um die nächste Rechnung einzugeben.

Alternativ kannst du Konto, Analysekonto, MWSt-Klasse und Beträge
manuell für diese eine Rechnung ändern.

Lino schaut beim Partner nach, welches Konto Einkauf dieser Partner
hat. Falls das Feld dort leer ist, nimmt Lino das Gemeinkonto
„Wareneinkäufe“. Das MWSt-Regime der Rechnung nimmt Lino ebenfalls vom
Partner. Beide Felder kannst du in den Partnerstammdaten nachschauen
gehen, indem du auf die Lupe (|search|) hinterm Feld „Partner“
klickst. Dort kannst du diese beiden Felder dann für alle zukünftigen
Rechnungen festlegen.

