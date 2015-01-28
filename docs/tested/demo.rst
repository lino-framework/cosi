.. _cosi.tested.demo:

=========================================
Tested code snippets on the demo database
=========================================

.. This document is part of the Lino Così test suite. To run only this
   test:

  $ python setup.py test -s tests.DocsTests.test_demo


General stuff:

>>> import os
>>> import json
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.std.settings.doctests'
>>> from lino.runtime import *
>>> from django.test import Client
>>> client = Client()
>>> ses = rt.login('robin')

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify things in the demo database 
using the Django API:

>>> contacts.Person.objects.count()
69
>>> contacts.Company.objects.count()
20


The test database
-----------------

Test whether :meth:`get_db_overview_rst 
<ad.Site.get_db_overview_rst>` returns the expected result:

>>> print(dd.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
22 apps: about, bootstrap3, lino, contenttypes, system, users, countries, contacts, products, accounts, sepa, excerpts, outbox, uploads, appypod, export_excel, ledger, sales, vat, declarations, finan, lino_cosi.
44 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Chart             accounts.Charts                2         1
 accounts.Group             accounts.Groups                5         7
 contacts.Company           contacts.Companies             26        20
 contacts.CompanyType       contacts.CompanyTypes          3         16
 contacts.Partner           contacts.Partners              22        89
 contacts.Person            contacts.Persons               29        69
 contacts.Role              contacts.Roles                 4         0
 contacts.RoleType          contacts.RoleTypes             2         5
 contenttypes.ContentType   contenttypes.ContentTypes      4         45
 contenttypes.HelpText      contenttypes.HelpTexts         4         2
 countries.Country          countries.Countries            4         8
 countries.Place            countries.Places               6         78
 declarations.Declaration   declarations.Declarations      18        0
 excerpts.Excerpt           excerpts.ExcerptsByX           11        0
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        1
 finan.BankStatement        finan.BankStatements           12        0
 finan.BankStatementItem    finan.BankStatementItemTable   11        0
 finan.JournalEntry         finan.JournalEntries           10        0
 finan.JournalEntryItem     finan.JournalEntryItemTable    11        0
 finan.PaymentOrder         finan.PaymentOrders            12        0
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 ledger.AccountInvoice      ledger.Invoices                19        140
 ledger.InvoiceItem         ledger.InvoiceItemTable        9         224
 ledger.Journal             ledger.Journals                13        7
 ledger.Movement            ledger.Movements               9         702
 ledger.Voucher             ledger.Vouchers                8         206
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              8         12
 products.ProductCat        products.ProductCats           3         2
 sales.Invoice              sales.Invoices                 25        66
 sales.InvoiceItem          sales.InvoiceItemTable         13        130
 sales.ShippingMode         sales.ShippingModes            3         0
 sepa.Account               sepa.Accounts                  6         13
 system.SiteConfig          system.SiteConfigs             12        1
 system.TextFieldTemplate   system.TextFieldTemplates      5         2
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    13        1
 vat.PaymentTerm            vat.PaymentTerms               5         0
 vat.VatRule                vat.VatRules                   9         11
========================== ============================== ========= =======
<BLANKLINE>


Person #115 is not a Partner
----------------------------

Person #115 (u'Altenberg Hans') is not a Partner (master_key 
is <django.db.models.fields.related.ForeignKey: partner>)

>>> url = '/bs3/contacts/Person/115'
>>> res = client.get(url, REMOTE_USER='robin')
>>> print(res.status_code)
200


Slave tables with more than 15 rows
-----------------------------------

When you look at the detail window of Belgium in `Lino Così
<http://demo4.lino-framework.org/api/countries/Countries/BE?an=detail>`_
then you see a list of all places in Belgium.
This demo database contains exactly 48 entries:

>>> be = countries.Country.objects.get(isocode="BE")
>>> be.place_set.count()
48

>>> countries.PlacesByCountry.request(be).get_total_count()
48

>>> url = '/api/countries/PlacesByCountry?fmt=json&start=0&mt=10&mk=BE'
>>> res = client.get(url,REMOTE_USER='robin')
>>> print(res.status_code)
200
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
16

The 16 is because Lino has a hard-coded default value of  
returning only 15 rows when no limit has been specified
(there is one extra row for adding new records).

In versions after :blogref:`20130903` you can change that limit 
for a given table by overriding the 
:attr:`preview_limit <lino.core.tables.AbstractTable.preview_limit>`
parameter of your table definition.
Or you can change it globally for all your tables 
by setting the 
:attr:`preview_limit <ad.Site.preview_limit>`
Site attribute to either `None` or some bigger value.

This parameter existed before but wasn't tested.
In your code this would simply look like this::

  class PlacesByCountry(Places):
      preview_limit = 30

Here we override it on the living object:

>>> countries.PlacesByCountry.preview_limit = 25

Same request returns now 26 data rows:

>>> res = client.get(url, REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
26

To remove the limit altogether, you can say:

>>> countries.PlacesByCountry.preview_limit = None

and the same request now returns all 49 data rows (48 + the phantom
row):

>>> res = client.get(url,REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
49


