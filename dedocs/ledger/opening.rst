.. include:: /../docs/shared/include/defs.rst

=================
Eröffnungsbuchung
=================

.. contents::
   :depth: 1
   :local:


Wenn die Buchhaltung nicht in Lino beginnt und früher mit einem anderen
Programm gemacht wurde, dann musst du Lino die Kontenstände der Bilanzkonten zu
Beginn deiner Arbeit mitteilen.

Das muss manuell geschehen (bisher hat noch niemand eine automatische
Importfunktion aus anderen Buchhaltungsprogrammen in Auftrag gegeben).

Du brauchst dazu die Saldenliste der Generalkonten am Ende des Geschäftsjahres
vor dem Beginn mit Lino. Diese wird vom Vorgängersystem erstellt. In so einer
Saldenliste sollten nur die Bilanzkonten einen Endsaldo haben, weil die
Resultatkonten ja nie von einem GJ ins nächste übertragen werden.

Alle Bilanzkonten, die dort einen Beginnsaldo haben, solltest du in deinem
Kontenplan erfassen.

Wähle :menuselection:`Buchhaltung --> Diverse Transaktionen`.

Klicke auf |insert|, um einen neuen Beleg zu starten.

- Gib als Buchungsdatum den ersten Tag des ersten Geschäftsjahres ein.
- Gib als Beschreibung "Eröffnung Generalkonten"

Bestätige das Fenster mit :kbd:`Ctrl+S` oder Klick auf "Erstellen".

Im Inhalt des Belegs gib eine Kopie der o.e. Saldenliste ein.

Registriere den Beleg, um sicherzustellen, dass die Bilanz ausgeglichen ist.

Falls in den Zentralisierungskonten für Verkauf, Einkauf, Gehälter, etc ein
Saldo steht, erstelle nun pro Handelsart einen weiteren Beleg mit der
Bezeichnung "Eröffnung Kunden", "Eröffnung Lieferanten", "Eröffnung
Angestellte" usw.

Um auch die Salden der einzelnen Partner