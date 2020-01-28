============================
An introduction to Lino Così
============================

Contacts
========

**Persons** is meant to record physical persons, while
**Organizations** is for companies, agencies, institutions and so on.

.. note::

    Note how persons and organizations are similar (e.g. they all have
    an `address` and a `phone number` field), but not quite.  Did you
    see some of the differences?

    (Answer: e.g. persons have a `Last name`, `First name` and `Sex`
    while organiszations have an `Organization type`.

Note that a person can have a given *role* in a given organization and
thus becomes a *contact person*.

The **Partners** table is what *persons* and *organizations* have in
common. As you can see, this table contains both your persons *and*
your organizations **together** in a same list.  It is the `union
<https://en.wikipedia.org/wiki/Union_%28set_theory%29>`_ of both
tables.

Why do we need such a union table of partners? There is an important
reason: an invoice (one of the important documents used in accounting)
must have a *recipient*, and that recipient can be a private person
for some invoices and an organization for some other invoices. And
(last but not least) in many accounting situations you are not
interested whether it's a person or an organizations, it is just some
business partner who owes you money.


Products
========

Lino Cosi has a simple product management.

You might write templates to produce a printable catalog or a website
from these product.


Sales
=====

sales, purchases and wages.


Accounting
==========

A **journal** is a collection of numbered documents called **vouchers**.


Kontakte verwalten
==================

Im Menü :menuselection:`Kontakte`
haben wir drei Befehle:
:menuselection:`Kontakte --> Personen`,
:menuselection:`Kontakte --> Organisationen`
und
:menuselection:`Kontakte --> Partner`.

In Lino Così müssen Empfänger von Verkaufsrechnungen und Absender
von Einkaufsrechnungen *zumindest* als "Partner" erfasst werden.
Ein Partner ist normalerweise entweder eine Organisation
(Firma, Institution,...) oder eine Person.
Theoretisch kann er auch beides zugleich sein:
Zum Beispiel kann ein befreundeter selbstständiger
Schreiner zugleich Person und Organisation (Einzelunternehmen) sein.

Ein Partner kann (noch theoretischer) auch weder Person noch Organisation
sein: zum Beispiel eine Verteilerliste.

Produkte verwalten
==================

Produkte sind alle Dinge, die Sie verkaufen wollen.
Also das können auch Dienstleistungen sein.
Ein Produkt hat eine Bezeichnung und einen Stückpreis.

Wenn Sie viele Produkte haben, können Sie diese
optional in Kategorien ordnen.
