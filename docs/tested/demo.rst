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
>>> ses = rt.login('rolf')

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
<lino_site.Site.get_db_overview_rst>` returns the expected result:

>>> print(dd.get_db_overview_rst()) 
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
23 apps: about, bootstrap3, lino, contenttypes, system, users, countries, contacts, products, accounts, sepa, excerpts, outbox, uploads, appypod, export_excel, ledger, sales, vat, declarations, finan, lino_cosi, djangosite.
43 models:
========================== ========= =======
 Name                       #fields   #rows
-------------------------- --------- -------
 accounts.Account           14        12
 accounts.Chart             4         1
 accounts.Group             7         7
 contacts.Company           26        20
 contacts.CompanyType       7         16
 contacts.Partner           22        89
 contacts.Person            29        69
 contacts.Role              4         0
 contacts.RoleType          4         5
 contenttypes.ContentType   4         44
 countries.Country          6         8
 countries.Place            8         78
 declarations.Declaration   18        0
 excerpts.Excerpt           11        0
 excerpts.ExcerptType       17        1
 finan.BankStatement        12        27
 finan.BankStatementItem    11        124
 finan.JournalEntry         10        0
 finan.JournalEntryItem     11        0
 finan.PaymentOrder         12        27
 finan.PaymentOrderItem     10        135
 ledger.AccountInvoice      19        140
 ledger.InvoiceItem         9         224
 ledger.Journal             17        7
 ledger.Movement            9         1015
 ledger.Voucher             8         260
 outbox.Attachment          4         0
 outbox.Mail                8         0
 outbox.Recipient           6         0
 products.Product           12        12
 products.ProductCat        5         2
 sales.Invoice              25        66
 sales.InvoiceItem          13        130
 sales.ShippingMode         5         0
 sepa.Account               6         13
 system.HelpText            4         2
 system.SiteConfig          12        1
 system.TextFieldTemplate   5         2
 uploads.Upload             9         0
 uploads.UploadType         7         0
 users.Authority            3         0
 users.User                 13        3
 vat.PaymentTerm            7         0
========================== ========= =======
<BLANKLINE>


Person #115 is not a Partner
----------------------------

Person #115 (u'Altenberg Hans') is not a Partner (master_key 
is <django.db.models.fields.related.ForeignKey: partner>)

>>> url = '/bs3/contacts/Person/115'
>>> res = client.get(url,REMOTE_USER='robin')
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
:attr:`preview_limit <lino.site.Site.preview_limit>`
Site attribute to either `None` or some bigger value.

This parameter existed before but wasn't tested.
In your code this would simply look like this::

  class PlacesByCountry(Places):
      preview_limit = 30

Here we override it on the living object:

>>> countries.PlacesByCountry.preview_limit = 25

Same request returns now 26 data rows:

>>> res = client.get(url,REMOTE_USER='robin')
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


