.. include:: /../docs/shared/include/defs.rst

==========
Bankkonten
==========

.. contents::
   :depth: 1
   :local:


Kontoauszüge erfassen
=====================

Für jedes Bankkonto gibt es in Lino ein entsprechendes *Journal*. Für
jeden Kontoauszug der Bank gibst du einen Kontoauszug in Lino ein.
Achte dabei auf Übereinstimmung der Nummern sowie der alten und neuen
Salden. Jeder Kontoauszug wiederum enthält eine oder mehrere Zeilen,
je eine pro Transaktion.

Um einen neuen Kontoauszug zu erfassen, wähle zunächst im Hauptmenü
:menuselection:`Buchhaltung --> Finanzjournale` und dort das
gewünschte Journal. Lino zeigt dann eine Tabelle mit den bereits
erfassten Kontoauszügen. Hier kannst du sehen, wo du beim letzten Mal
aufgehört hast.

Doppelklick auf einem bestehenden Auszug zeigt dessen
Vollbild-Ansicht.

Klicke auf |insert| in der Werkzeugleiste, um einen neuen Kontoauszug
einzufügen.

Als Buchungsdatum gib das Datum des Kontoauszugs ein. Der *Alte Saldo*
sollte der gleiche sein wie der *Neue Saldo* des vorigen Kontoauszugs.

Dieses Fenster kannst du auch per Tastatur mit :kbd:`Ctrl+S`
bestätigen.

Anfangs zeigt Lino den noch leeren Kontoauszug.

Hier musst du auf |eject| klicken, um das untere Panel (*Inhalt*)
in einem eigenen Fenster zu öffnen.

Inhalt eines Kontoauszugs
=========================

Das Feld **Nr** füllt Lino automatisch aus. (Du kannst auf einer
bestehenden Nummer :kbd:`F2` drücken und sie ändern, um die
Reihenfolge der Zeilen zu beeinflussen).

Das Feld **Datum** kann leer bleiben, dann trägt Lino das Datum des
Kontoauszugs ein.

Im Feld **Partner** muss der *Kunde* oder *Lieferant* ausgewählt
werden, wenn es sich um die *Zahlung einer Rechnung* handelt.  Siehe
`Zahlung einer Rechnung erfassen`_.

Das Feld muss *leer* bleiben, wenn es sich um eine *allgemeine
Buchung* (Generalbuchung) handelt, die nicht beglichen werden
muss. Zum Beispiel interne Transfers von einem Bankkonto zum anderen,
Abbuchung von Zahlungsaufträgen, Bankunkosten, Zuschüsse, Subsidien,
Kreditrückzahlungen, Mieten.

Im Feld **Konto** muss das *Generalkonto* eingetragen werden. Dieses
Feld muss immer ausgefüllt sein. Wenn Du einen Partner ausgewählt
hast, dann sollte hier eines der Konten "Kunden" (4000) oder
"Lieferanten" (4400) stehen.

Das Feld **Match** dient zum Begleichen von Zahlungen auf
Partnerkonten.  Bei Zahlungen ohne Partnerkonto sollte es leer sein.
Siehe auch `Bereinigen von Partnerkonten`_.

Zahlung einer Rechnung erfassen
===============================

Wenn im Inhalt eines Bankkontoauszugs ein *Partner* ausgefüllt ist,
dann schaut Lino nach, ob offene Buchungen vorliegen und tut
folgendes.

- Wenn es **genau eine offene Buchung** gibt, füllt Lino in den
  Feldern *Match* und *Einnahme* bzw. *Ausgabe* die Zahlungsreferenz
  und den Betrag der Rechnung ein.
  
  Wenn Lino den Betrag ausgefüllt hast, kannst du diesen trotzdem noch
  abändern.  Zum Beispiel bei Teilzahlung oder Zahlungsdifferenz.

- Wenn es **mehrere offene Buchungen** gibt, trägt Lino im Feld
  *Match* den Text "x Vorschläge" ein. Das bedeutet, dass du auf das
  Wort *Vorschläge* klicken solltest.  Siehe `Buchungsvorschläge`_.
  Falls Du keinen Vorschlag findest, solltest du das Feld *Match* entweder  auf leer setzen 

- Wenn es **keine offene Buchung** gibt, setzt Lino das Feld *Match*  auf leer.
  Du musst dann im Feld *Konto* entweder *4000 Kunden* oder *4400 Lieferanten*
  eingeben und den Betrag in *Einnahme* bzw. *Ausgabe* selber ausfüllen.
  
Buchungsvorschläge
==================

Das Fenster **Buchungsvorschläge** öffnet sich, wenn du auf das Wort
*Vorschläge* klickst.  Hier zeigt Lino alle offenen Buchungen des
Partners.

Du kannst Zeile eine davon **auswählen**, indem du auf den Button mit
dem **Blitz** klickst.  (Ja, das ist nicht die intuitivste Methode...
wir arbeiten daran).

Lino füllt dann die betreffende Zeile des Kontoauszug so aus, dass sie
den ausgewählten Vorschlag begleicht.

Du kannst **mehrere Zeilen auf einmal** auswählen, indem du
:kbd:`[Shift]` oder `[Ctrl]` beim Klicken gedrückt hältst.  Mit
:kbd:`[Shift]` werden auch alle Zeilen zwischen der ersten und der
zweiten Zeile ausgeählt.

Wenn du mehrere Vorschläge auswählst, fügt Lino für jeden zusätzlichen
Vorschlag eine Zeile in den Kontoauszug ein.


Wenn die Rechnungsnummer bekannt ist
====================================

Wenn die Rechnungsnummer bekannt ist, kannst du diese im Feld
**Match** eintragen und Lino füllt dann Partner und Betrag ausgehend
von der Rechnung aus.


Bereinigen von Partnerkonten
============================

Buchungen in einem Partnerkonto müssen prinzipiell **beglichen**
werden, d.h. Debit und Kredit müssen einander ausgleichen.  Zum
Beispiel wenn ich einem Kunden eine Rechnung schicke, dann muss der
die auch bezahlen.

Solange eine Partnerbuchung nicht beglichen ist, gilt sie als
**offen**.

Zum Beispiel kann man in der **Historie eines Partners** man angeben,
ob man nur die offenen Buchungen sehen will, oder nur die beglichenen,
oder alle.  Die *Historie eines Partners* kannst du sehen, indem du
auf den Namen des Partners klickst. Lino öffnet dann das
Detail-Fenster dieses Partners. Dort musst du dann noch auf **offene
Buchungen** klicken.

Jede Buchung in ein Partnerkonto hat einen **Match**.  Das ist ein
kurzer Text, üblicherweise die Rechnungsnummer, der von Lino
automatisch gefüllt wird.

Man kann den *Match* manuell im Nachhinein ändern. Das kann sinnvoll
sein z.B. bei Teilzahlungen, Zahlungsdifferenzen oder wenn eine
Zahlung mehrere Rechnungen begleicht.

Man kann den Match nicht einfach mit :kbd:`F2` in der Historie ändern,
sondern man muss das betreffende Dokument entregisterern, den Match
dort ändern, und dann das Dokument wieder registrerern.  Das geht aber
relativ schnell, weil du ja von der Historie aus auf den Beleg klicken
kannst, um dessen Detailfenster zu öffnen.  Wenn du nach dem
Registrieren das Detailfenster schließt, kommst du in deine Historie
zurück.
