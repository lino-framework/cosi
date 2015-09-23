.. _cosi.tested.demo:

=========================================
Tested code snippets on the demo database
=========================================

.. This document is part of the Lino Così test suite. To run only this
   test:

    $ python setup.py test -s tests.DocsTests.test_demo
    
    doctest init:

    >>> import os
    >>> import json
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.std.settings.doctests'
    >>> from lino.api.doctest import *
    >>> ses = rt.login('robin')

We can now refer to every installed app via it's `app_label`.
For example here is how we can verify things in the demo database 
using the Django API:

>>> contacts.Person.objects.count()
69
>>> contacts.Company.objects.count()
22


The test database
-----------------

Test whether :meth:`get_db_overview_rst 
<ad.Site.get_db_overview_rst>` returns the expected result:

>>> print(dd.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
28 apps: staticfiles, about, bootstrap3, lino_startup, appypod, printing, system, contenttypes, gfks, users, countries, contacts, products, accounts, sepa, uploads, outbox, excerpts, export_excel, ledger, vat, declarations, finan, sales, cosi, cal, courses, vatless.
66 models:
========================== ============================== ========= =======
 Name                       Default table                  #fields   #rows
-------------------------- ------------------------------ --------- -------
 accounts.Account           accounts.Accounts              12        12
 accounts.Group             accounts.Groups                5         7
 cal.Calendar               cal.Calendars                  4         1
 cal.Event                  cal.OneEvent                   23        68
 cal.EventType              cal.EventTypes                 12        2
 cal.Guest                  cal.Guests                     6         0
 cal.GuestRole              cal.GuestRoles                 2         0
 cal.Priority               cal.Priorities                 3         4
 cal.RecurrentEvent         cal.RecurrentEvents            19        9
 cal.RemoteCalendar         cal.RemoteCalendars            7         0
 cal.Room                   cal.Rooms                      2         0
 cal.Subscription           cal.Subscriptions              4         0
 cal.Task                   cal.Tasks                      17        0
 contacts.Company           contacts.Companies             26        22
 contacts.CompanyType       contacts.CompanyTypes          3         16
 contacts.Partner           contacts.Partners              22        91
 contacts.Person            contacts.Persons               29        69
 contacts.Role              contacts.Roles                 4         0
 contacts.RoleType          contacts.RoleTypes             2         5
 contenttypes.ContentType   gfks.ContentTypes              4         67
 countries.Country          countries.Countries            4         8
 countries.Place            countries.Places               6         78
 courses.Course             courses.Courses                28        0
 courses.Enrolment          courses.Enrolments             14        0
 courses.Line               courses.Lines                  15        0
 courses.Slot               courses.Slots                  5         0
 courses.Topic              courses.Topics                 2         0
 declarations.Declaration   declarations.Declarations      18        0
 excerpts.Excerpt           excerpts.Excerpts              11        0
 excerpts.ExcerptType       excerpts.ExcerptTypes          15        2
 finan.BankStatement        finan.BankStatements           12        15
 finan.BankStatementItem    finan.BankStatementItemTable   10        99
 finan.Grouper              finan.Groupers                 11        0
 finan.GrouperItem          finan.GrouperItemTable         9         0
 finan.JournalEntry         finan.FinancialVouchers        10        0
 finan.JournalEntryItem     finan.JournalEntryItemTable    10        0
 finan.PaymentOrder         finan.PaymentOrders            12        15
 finan.PaymentOrderItem     finan.PaymentOrderItemTable    10        0
 gfks.HelpText              gfks.HelpTexts                 4         2
 ledger.Journal             ledger.Journals                14        7
 ledger.MatchRule           ledger.MatchRules              3         10
 ledger.Movement            ledger.Movements               9         495
 ledger.PaymentTerm         ledger.PaymentTerms            5         0
 ledger.Voucher             ledger.Vouchers                9         136
 outbox.Attachment          outbox.Attachments             4         0
 outbox.Mail                outbox.Mails                   8         0
 outbox.Recipient           outbox.Recipients              6         0
 products.Product           products.Products              9         12
 products.ProductCat        products.ProductCats           3         2
 sales.InvoiceItem          sales.InvoiceItemTable         15        51
 sales.InvoicingMode        sales.InvoicingModes           6         0
 sales.ShippingMode         sales.ShippingModes            3         0
 sales.VatProductInvoice    sales.Invoices                 27        26
 sepa.Account               sepa.Accounts                  6         17
 sepa.Movement              sepa.Movements                 9         0
 sepa.Statement             sepa.Statements                9         0
 system.SiteConfig          system.SiteConfigs             15        1
 uploads.Upload             uploads.Uploads                9         0
 uploads.UploadType         uploads.UploadTypes            6         0
 users.Authority            users.Authorities              3         0
 users.User                 users.Users                    15        1
 vat.InvoiceItem            vat.InvoiceItemTable           9         128
 vat.VatAccountInvoice      vat.Invoices                   21        80
 vat.VatRule                vat.VatRules                   9         11
 vatless.AccountInvoice     vatless.Invoices               18        0
 vatless.InvoiceItem        vatless.InvoiceItems           6         0
========================== ============================== ========= =======
<BLANKLINE>


Person #115 is not a Partner
----------------------------

Person #115 (u'Altenberg Hans') is not a Partner (master_key 
is <django.db.models.fields.related.ForeignKey: partner>)

>>> url = '/bs3/contacts/Person/115'
>>> res = test_client.get(url, REMOTE_USER='robin')
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
>>> res = test_client.get(url,REMOTE_USER='robin')
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

>>> res = test_client.get(url, REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
26

To remove the limit altogether, you can say:

>>> countries.PlacesByCountry.preview_limit = None

and the same request now returns all 49 data rows (48 + the phantom
row):

>>> res = test_client.get(url,REMOTE_USER='robin')
>>> result = json.loads(res.content)
>>> print(len(result['rows']))
49


