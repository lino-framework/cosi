.. _cosi.specs.general:
.. _cosi.tested.general:

=======
General
=======

..  to test only this document:

    $ python setup.py test -s tests.DocsTests.test_general

    >>> import lino
    >>> lino.startup('lino_cosi.projects.std.settings.doctests')
    >>> from lino.api.doctest import *

The database structure
======================

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
33 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, printing, system, contenttypes, gfks, users, office, xl, countries, cosi, contacts, products, accounts, weasyprint, ledger, sepa, excerpts, appypod, export_excel, tinymce, wkhtmltopdf, vat, finan, sales, invoicing, cal, courses, vatless.
60 models:
=========================== ============================== ========= =======
 Name                        Default table                  #fields   #rows
--------------------------- ------------------------------ --------- -------
 accounts.Account            accounts.Accounts              15        12
 accounts.Group              accounts.Groups                6         7
 cal.Calendar                cal.Calendars                  6         1
 cal.Event                   cal.OneEvent                   23        172
 cal.EventPolicy             cal.EventPolicies              19        6
 cal.EventType               cal.EventTypes                 17        2
 cal.Guest                   cal.Guests                     6         0
 cal.GuestRole               cal.GuestRoles                 4         0
 cal.Priority                cal.Priorities                 5         4
 cal.RecurrentEvent          cal.RecurrentEvents            21        15
 cal.RemoteCalendar          cal.RemoteCalendars            7         0
 cal.Room                    cal.Rooms                      4         0
 cal.Subscription            cal.Subscriptions              4         0
 cal.Task                    cal.Tasks                      17        0
 contacts.Company            contacts.Companies             27        22
 contacts.CompanyType        contacts.CompanyTypes          7         16
 contacts.Partner            contacts.Partners              23        91
 contacts.Person             contacts.Persons               30        69
 contacts.Role               contacts.Roles                 4         0
 contacts.RoleType           contacts.RoleTypes             4         5
 contenttypes.ContentType    gfks.ContentTypes              3         61
 countries.Country           countries.Countries            6         8
 countries.Place             countries.Places               8         78
 courses.Course              courses.Activities             29        0
 courses.Enrolment           courses.Enrolments             14        0
 courses.Line                courses.Lines                  21        0
 courses.Slot                courses.Slots                  5         0
 courses.Topic               courses.Topics                 4         0
 excerpts.Excerpt            excerpts.Excerpts              11        0
 excerpts.ExcerptType        excerpts.ExcerptTypes          17        6
 finan.BankStatement         finan.BankStatements           16        4
 finan.BankStatementItem     finan.BankStatementItemTable   10        22
 finan.JournalEntry          finan.FinancialVouchers        14        0
 finan.JournalEntryItem      finan.JournalEntryItemTable    10        0
 finan.PaymentOrder          finan.PaymentOrders            15        4
 finan.PaymentOrderItem      finan.PaymentOrderItemTable    10        20
 gfks.HelpText               gfks.HelpTexts                 4         2
 invoicing.Item              invoicing.Items                10        0
 invoicing.Plan              invoicing.Plans                6         1
 ledger.AccountingPeriod     ledger.AccountingPeriods       7         5
 ledger.Journal              ledger.Journals                19        7
 ledger.MatchRule            ledger.MatchRules              3         11
 ledger.Movement             ledger.Movements               10        212
 ledger.PaymentTerm          ledger.PaymentTerms            11        8
 ledger.Voucher              ledger.Vouchers                9         57
 products.Product            products.Products              13        9
 products.ProductCat         products.ProductCats           5         2
 sales.InvoiceItem           sales.InvoiceItems             15        48
 sales.PaperType             sales.PaperTypes               5         2
 sales.VatProductInvoice     sales.Invoices                 24        24
 sepa.Account                sepa.Accounts                  6         17
 system.SiteConfig           system.SiteConfigs             17        1
 tinymce.TextFieldTemplate   tinymce.TextFieldTemplates     5         2
 users.Authority             users.Authorities              3         0
 users.User                  users.Users                    16        3
 vat.InvoiceItem             vat.InvoiceItemTable           9         40
 vat.VatAccountInvoice       vat.Invoices                   19        25
 vat.VatRule                 vat.VatRules                   9         11
 vatless.AccountInvoice      vatless.Invoices               17        0
 vatless.InvoiceItem         vatless.InvoiceItems           6         0
=========================== ============================== ========= =======
<BLANKLINE>


The application menu
====================

Robin is the system administrator, he has a complete menu:

>>> ses = rt.login('robin') 
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Persons, Organizations, Partners
- Products : Products, Product Categories
- Accounting :
  - Sales : Sales invoices (SLS), Sales credit notes (SLC)
  - Purchases : Purchase invoices (PRC)
  - Financial : Payment Orders (PMO), Cash (CSH), Bestbank (BNK), Miscellaneous Journal Entries (MSC)
  - Create invoices
- Office : My Excerpts
- Calendar : My appointments, Overdue appointments, Unconfirmed appointments, My tasks, My guests, My presences, My overdue appointments
- Activities : Courses, -, Activity lines, Pending requested enrolments, Pending confirmed enrolments
- Reports :
  - Accounting : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
- Configure :
  - System : Site Parameters, Help Texts, Users
  - Places : Countries, Places
  - Contacts : Organization types, Functions
  - Accounting : Account Groups, Accounts, Journals, Accounting periods, Payment Terms
  - Office : Excerpt Types, My Text Field Templates
  - VAT : VAT rules, Paper types
  - Calendar : Calendars, Rooms, Priorities, Recurrent event rules, Guest Roles, Calendar Event Types, Event Policies, Remote Calendars
  - Activities : Topics, Timetable Slots
- Explorer :
  - System : content types, Authorities, User types
  - Contacts : Contact Persons
  - Accounting : Match rules, Vouchers, Voucher types, Movements, Fiscal Years, Trade types, Journal groups, Invoices
  - SEPA : Bank accounts
  - Office : Excerpts, Text Field Templates
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items, Invoicing plans
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - Calendar : Calendar entries, Tasks, Presences, Subscriptions, Event states, Guest states, Task states
  - Activities : Activities, Enrolments, Enrolment states
- Site : About

Romain gets the same menu in French:
  
>>> rt.login('romain').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Contacts : Personnes, Organizations, Partenaires
- Products : Products, Product Categories
- Comptabilité :
  - Sales : Factures vente (SLS), Sales credit notes (SLC)
  - Purchases : Factures achat (PRC)
  - Financial : Payment Orders (PMO), Caisse (CSH), Bestbank (BNK), Opérations diverses (MSC)
  - Create invoices
- Bureau : Mes Extraits
- Calendrier : Mes rendez-vous, Rendez-vous dépassés, Rendez-vous à confirmer, Mes tâches, Mes visiteurs, Mes présences, Mes rendez-vous dépassés
- Activities : Cours, -, Activity lines, Demandes d’inscription en attente, Demandes d’inscription confirmées
- Rapports :
  - Comptabilité : Situation, Activity Report, Debtors, Creditors
  - VAT : Due invoices
- Configuration :
  - Système : Paramètres du Site, Textes d'aide, Utilisateurs
  - Endroits : Pays, Endroits
  - Contacts : Types d'organisation, Fonctions
  - Comptabilité : Groupes de comptes, Comptes, Journals, Périodes comptables, Délais de paiement
  - Bureau : Types d'extrait, Mes Text Field Templates
  - VAT : VAT rules, Types de papier
  - Calendrier : Calendriers, Locaux, Priorités, Règles d'évènements récurrents, Rôles de participants, Types d'entrée calendrier, Event Policies, Remote Calendars
  - Activities : Topics, Timetable Slots
- Explorateur :
  - Système : types de contenu, Procurations, Types d'utilisateur
  - Contacts : Personnes de contact
  - Comptabilité : Match rules, Vouchers, Voucher types, Mouvements, Années comptables, Trade types, Journal groups, Invoices
  - SEPA : Comptes en banque
  - Bureau : Extraits, Text Field Templates
  - VAT : VAT regimes, VAT Classes, Product invoices, Product invoice items, Invoicing plans
  - Financial : Bank Statements, Journal Entries, Payment Orders
  - Calendrier : Entrées calendrier, Tâches, Présences, Abonnements, Event states, Guest states, Task states
  - Activities : Activities, Inscriptions, États d'inscription
- Site : à propos

Rolf gets the same menu in German:
  
>>> rt.login('rolf').show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Produkte : Produkte, Produktkategorien
- Buchhaltung :
  - Verkauf : Verkaufsrechnungen (SLS), Gutschriften Verkauf (SLC)
  - Einkauf : Einkaufsrechnungen (PRC)
  - Finanzjournale : Zahlungsaufträge (PMO), Kasse (CSH), Bestbank (BNK), Diverse Buchungen (MSC)
  - Rechnungen erstellen
- Büro : Meine Auszüge
- Kalender : Meine Termine, Überfällige Termine, Unbestätigte Termine, Meine Aufgaben, Meine Gäste, Meine Anwesenheiten, Meine überfälligen Termine
- Aktivitäten : Kurse, -, Aktivitätenreihen, Offene Einschreibungsanfragen, Auszustellende Teilnahmebescheinigungen
- Berichte :
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
  - MwSt. : Offene Rechnungen
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontengruppen, Konten, Journale, Buchungsperioden, Zahlungsbedingungen
  - Büro : Auszugsarten, Meine Einfügetexte
  - MwSt. : MwSt-Regeln, Papierarten
  - Kalender : Kalenderliste, Räume, Prioritäten, Periodische Terminregeln, Gastrollen, Kalendereintragsarten, Terminregeln, Externe Kalender
  - Aktivitäten : Themen, Timetable Slots
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerarten
  - Kontakte : Kontaktpersonen
  - Buchhaltung : Ausgleichungsregeln, Belege, Belegarten, Bewegungen, Geschäftsjahre, Handelsarten, Journalgruppen, Rechnungen
  - SEPA : Bankkonten
  - Büro : Auszüge, Einfügetexte
  - MwSt. : MwSt.-Regimes, MwSt.-Klassen, Produktrechnungen, Produktrechnungszeilen, Fakturationspläne
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
  - Kalender : Kalendereinträge, Aufgaben, Anwesenheiten, Abonnements, Termin-Zustände, Gast-Zustände, Aufgaben-Zustände
  - Aktivitäten : Aktivitäten, Einschreibungen, Einschreibungs-Zustände
- Site : Info
