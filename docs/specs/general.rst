.. _cosi.specs.general:
.. _cosi.tested.general:

=======
General
=======

..  to test only this document:

    $ python setup.py test -s tests.DocsTests.test_general

    >>> import lino
    >>> lino.startup('lino_cosi.projects.apc.settings.doctests')
    >>> from lino.api.doctest import *

The database structure
======================

>>> from lino.utils.diag import analyzer
>>> print(analyzer.show_db_overview())
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
31 apps: lino_startup, staticfiles, about, jinja, bootstrap3, extjs, printing, system, contenttypes, gfks, users, office, countries, contacts, xl, products, cosi, accounts, ledger, sepa, uploads, outbox, excerpts, appypod, export_excel, tinymce, wkhtmltopdf, vat, finan, sales, invoicing.
46 models:
=========================== ============================== ========= =======
 Name                        Default table                  #fields   #rows
--------------------------- ------------------------------ --------- -------
 accounts.Account            accounts.Accounts              15        12
 accounts.Group              accounts.Groups                6         7
 contacts.Company            contacts.Companies             27        22
 contacts.CompanyType        contacts.CompanyTypes          7         14
 contacts.Partner            contacts.Partners              23        91
 contacts.Person             contacts.Persons               30        69
 contacts.Role               contacts.Roles                 4         0
 contacts.RoleType           contacts.RoleTypes             4         5
 contenttypes.ContentType    gfks.ContentTypes              3         47
 countries.Country           countries.Countries            6         8
 countries.Place             countries.Places               8         78
 excerpts.Excerpt            excerpts.Excerpts              11        0
 excerpts.ExcerptType        excerpts.ExcerptTypes          17        5
 finan.BankStatement         finan.BankStatements           16        14
 finan.BankStatementItem     finan.BankStatementItemTable   10        66
 finan.JournalEntry          finan.FinancialVouchers        14        0
 finan.JournalEntryItem      finan.JournalEntryItemTable    10        0
 finan.PaymentOrder          finan.PaymentOrders            15        14
 finan.PaymentOrderItem      finan.PaymentOrderItemTable    10        70
 gfks.HelpText               gfks.HelpTexts                 4         2
 invoicing.Item              invoicing.Items                9         0
 invoicing.Plan              invoicing.Plans                6         1
 ledger.AccountingPeriod     ledger.AccountingPeriods       7         15
 ledger.Journal              ledger.Journals                19        6
 ledger.MatchRule            ledger.MatchRules              3         10
 ledger.Movement             ledger.Movements               9         650
 ledger.PaymentTerm          ledger.PaymentTerms            8         7
 ledger.Voucher              ledger.Vouchers                9         175
 outbox.Attachment           outbox.Attachments             4         0
 outbox.Mail                 outbox.Mails                   8         0
 outbox.Recipient            outbox.Recipients              6         0
 products.Product            products.Products              13        9
 products.ProductCat         products.ProductCats           5         2
 sales.InvoiceItem           sales.InvoiceItems             15        144
 sales.PaperType             sales.PaperTypes               5         2
 sales.VatProductInvoice     sales.Invoices                 24        72
 sepa.Account                sepa.Accounts                  6         17
 system.SiteConfig           system.SiteConfigs             13        1
 tinymce.TextFieldTemplate   tinymce.TextFieldTemplates     5         2
 uploads.Upload              uploads.Uploads                9         0
 uploads.UploadType          uploads.UploadTypes            8         0
 users.Authority             users.Authorities              3         0
 users.User                  users.Users                    13        3
 vat.InvoiceItem             vat.InvoiceItemTable           9         120
 vat.VatAccountInvoice       vat.Invoices                   19        75
 vat.VatRule                 vat.VatRules                   9         11
=========================== ============================== ========= =======
<BLANKLINE>



The application menu
====================

Rolf is the local system administrator, he has a complete menu:

>>> ses = rt.login('rolf') 
>>> with dd.translation.override('de'):
...     ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Kontakte : Personen, Organisationen, Partner
- Produkte : Produkte, Produktkategorien
- Buchhaltung :
  - Verkauf : Verkaufsrechnungen (SLS)
  - Einkauf : Einkaufsrechnungen (PRC)
  - Finanzjournale : Zahlungsaufträge (PMO), Kasse (CSH), Bestbank (BNK), Diverse Buchungen (MSC)
  - Rechnungen erstellen
- Büro : Meine Uploads, Mein E-Mail-Ausgang, Meine Auszüge
- Berichte :
  - System : Broken GFKs
  - Buchhaltung : Situation, Tätigkeitsbericht, Schuldner, Gläubiger
- Konfigurierung :
  - System : Site-Parameter, Hilfetexte, Benutzer
  - Orte : Länder, Orte
  - Kontakte : Organisationsarten, Funktionen
  - Buchhaltung : Kontengruppen, Konten, Journale, Buchungsperioden, Zahlungsbedingungen
  - Büro : Upload-Arten, Auszugsarten, Meine Einfügetexte
  - MwSt. : MwSt-Regeln, Papierarten
- Explorer :
  - System : Datenbankmodelle, Vollmachten, Benutzerprofile
  - Kontakte : Kontaktpersonen
  - Buchhaltung : Befriedigungsregeln, Belege, Belegarten, Bewegungen, Geschäftsjahre, Handelsarten, Journalgruppen
  - SEPA : Bankkonten
  - Büro : Uploads, Upload-Bereiche, E-Mail-Ausgänge, Anhänge, Auszüge, Einfügetexte
  - MwSt. : MwSt.-Regimes, MwSt.-Klassen, Produktrechnungen, Produktrechnungszeilen, Fakturationspläne
  - Finanzjournale : Kontoauszüge, Diverse Buchungen, Zahlungsaufträge
- Site : Info


