=================
Datenbankstruktur
=================

.. contents::
   :depth: 1
   :local:


Kontakte
========

Als **Partner** bezeichnet Lino eine physische oder juristische Person, mit der
wir potentiell kommunizieren können.  Physische Personen stehen unter
:menuselection:`Kontakte --> Personen` juristische Personen unter
:menuselection:`Kontakte --> Organisationen`.

Eure Anwendung kann neben den beiden Grundarten "Personen" und "Organisationen"
weitere Partnerarten definieren, die zum Beispiel Klienten, Angestellte, Firmen
Schulen, Haushalte, , ...

Während du in der Praxis eure Partner nach **Partnerart** anschaust, kannst du
:menuselection:`Explorer --> Kontakte --> Partner` eine Liste aller Partner
sehen, die euer Lino kennt. Dort werden also alle Partnerarten in einen Topf
geworfen.

Jede *Person* kann potentiell **Kontaktperson** für eine oder mehrere
Organisationen sein.  Und umgekehrt kann jede Organisation eine oder mehrere
Kontaktpersonen haben.

Wenn man eine Person als Kontaktperson einer Organisation definiert, kann man
ausserdem angeben, welche **Funktion** diese  Person in dieser Organisation
ausübt.

Jeder Partner kann potentiell eine Rechnung kriegen oder schicken oder sonstwie
in einer buchhalterischen Bewegung vorkommen.  In diesem Fall spricht man dann
auch vom **Geschäftspartner**.


Buchhaltung
===========

Ein **Beleg** ist ein Dokument, das eine buchhalterische Transaktion belegt. Es
gibt verschiedene Arten von Belegen.  Manche Belege werden durch euren Lino
erstellt, z.B. Verkaufsrechnungen, Zahlungsaufträge oder MWSt-Deklarationen.
Andere Belege werden euch durch einen Geschäftspartner zugestellt und ihr gebt
sie in Lino ein, z.B. Einkaufsrechnungen oder Bankkontoauszüge.

Ein **Journal** ist eine nummerierte Serie von Belegen der gleichen Art.  Eure
Journale kannst du sehen und konfigurieren unter :menuselection:`Konfigurierung
--> Buchhaltung --> Journale`.

Jedes Journal

