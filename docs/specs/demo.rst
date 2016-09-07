.. _cosi.tested.demo:

=========================================
Tested code snippets on the demo database
=========================================

.. This document is part of the Lino Così test suite. To run only this
   test:

    $ python setup.py test -s tests.DocsTests.test_demo
    
    doctest init:

    >>> from lino import startup
    >>> startup('lino_cosi.projects.std.settings.doctests')
    >>> from lino.api.doctest import *
    >>> ses = rt.login('robin')

The demo database contains 69 persons and 22 companies.

>>> contacts.Person.objects.count()
69
>>> contacts.Company.objects.count()
22
>>> contacts.Partner.objects.count()
91


>>> print(' '.join(settings.SITE.demo_fixtures))
std few_countries euvatrates furniture minimal_ledger demo demo_bookings payments demo2



The test database
-----------------


>>> from lino.utils.diag import analyzer
>>> print analyzer.show_database_structure()
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
- accounts.Account : id, ref, seqno, name, sales_allowed, purchases_allowed, wages_allowed, clearings_allowed, group, type, needs_partner, clearable, default_amount, name_fr, name_de
- accounts.Group : id, name, ref, account_type, name_fr, name_de
- cal.Calendar : id, name, description, color, name_fr, name_de
- cal.Event : id, modified, created, build_time, build_method, user, assigned_to, owner_type, owner_id, start_date, start_time, end_date, end_time, summary, description, access_class, sequence, auto_type, event_type, transparent, room, priority, state
- cal.EventType : id, seqno, name, attach_to_email, email_template, description, is_appointment, all_rooms, locks_user, start_date, event_label, max_conflicting, event_label_fr, event_label_de, name_fr, name_de
- cal.Guest : id, event, partner, role, state, remark
- cal.GuestRole : id, name, name_fr, name_de
- cal.Priority : id, name, ref, name_fr, name_de
- cal.RecurrentEvent : id, name, user, start_date, start_time, end_date, end_time, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, event_type, description, name_fr, name_de
- cal.RemoteCalendar : id, seqno, type, url_template, username, password, readonly
- cal.Room : id, name, name_fr, name_de
- cal.Subscription : id, user, calendar, is_hidden
- cal.Task : id, modified, created, user, owner_type, owner_id, start_date, start_time, summary, description, access_class, sequence, auto_type, due_date, due_time, percent, state
- contacts.Company : id, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, payment_term, vat_regime, invoice_recipient, paper_type, partner_ptr, prefix, type, vat_id
- contacts.CompanyType : id, name, abbr, abbr_fr, abbr_de, name_fr, name_de
- contacts.Partner : id, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, payment_term, vat_regime, invoice_recipient, paper_type
- contacts.Person : id, country, city, zip_code, region, addr1, street_prefix, street, street_no, street_box, addr2, url, phone, gsm, fax, name, language, email, remarks, payment_term, vat_regime, invoice_recipient, paper_type, partner_ptr, title, first_name, middle_name, last_name, gender, birth_date
- contacts.Role : id, type, person, company
- contacts.RoleType : id, name, name_fr, name_de
- contenttypes.ContentType : id, app_label, model
- countries.Country : name, isocode, short_code, iso3, name_fr, name_de
- countries.Place : id, parent, name, country, zip_code, type, name_fr, name_de
- courses.Course : id, user, start_date, start_time, end_date, end_time, every_unit, every, monday, tuesday, wednesday, thursday, friday, saturday, sunday, max_events, room, max_date, line, teacher, slot, description, remark, state, max_places, name, enrolments_until, description_fr, description_de
- courses.Enrolment : id, start_date, end_date, user, printed_by, course_area, course, pupil, request_date, state, places, option, remark, confirmation_details
- courses.Line : id, ref, name, excerpt_title, course_area, topic, description, every_unit, every, event_type, fee, guest_role, options_cat, fees_cat, body_template, description_fr, description_de, name_fr, name_de, excerpt_title_fr, excerpt_title_de
- courses.Slot : id, seqno, start_time, end_time, name
- courses.Topic : id, name, name_fr, name_de
- excerpts.Excerpt : id, build_time, build_method, user, company, contact_person, contact_role, owner_type, owner_id, excerpt_type, language
- excerpts.ExcerptType : id, name, build_method, template, attach_to_email, email_template, certifying, remark, body_template, content_type, primary, backward_compat, print_recipient, print_directly, shortcut, name_fr, name_de
- finan.BankStatement : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, last_item_date, balance1, balance2
- finan.BankStatementItem : id, seqno, match, amount, dc, remark, account, partner, date, voucher
- finan.JournalEntry : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, last_item_date
- finan.JournalEntryItem : id, seqno, match, amount, dc, remark, account, partner, date, voucher
- finan.PaymentOrder : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, printed_by, item_account, item_remark, total, execution_date
- finan.PaymentOrderItem : id, seqno, match, bank_account, amount, dc, remark, account, partner, voucher
- gfks.HelpText : id, content_type, field, help_text
- invoicing.Item : id, plan, partner, first_date, last_date, amount, number_of_invoiceables, preview, selected, invoice
- invoicing.Plan : id, user, journal, today, max_date, partner
- ledger.AccountingPeriod : id, ref, start_date, end_date, state, year, remark
- ledger.Journal : id, ref, seqno, name, build_method, template, trade_type, voucher_type, journal_group, auto_check_clearings, force_sequence, account, printed_name, dc, yearly_numbering, printed_name_fr, printed_name_de, name_fr, name_de
- ledger.MatchRule : id, account, journal
- ledger.Movement : id, voucher, partner, seqno, account, amount, dc, match, cleared, value_date
- ledger.PaymentTerm : id, ref, name, days, months, end_of_month, printed_text, printed_text_fr, printed_text_de, name_fr, name_de
- ledger.Voucher : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state
- outbox.Attachment : id, owner_type, owner_id, mail
- outbox.Mail : id, user, owner_type, owner_id, date, subject, body, sent
- outbox.Recipient : id, mail, partner, type, address, name
- products.Product : id, name, description, cat, delivery_unit, vat_class, description_fr, description_de, name_fr, name_de, sales_account, sales_price, purchases_account
- products.ProductCat : id, name, description, name_fr, name_de
- sales.InvoiceItem : id, seqno, total_incl, total_base, total_vat, vat_class, unit_price, qty, product, description, discount, voucher, title, invoiceable_type, invoiceable_id
- sales.PaperType : id, name, template, name_fr, name_de
- sales.VatProductInvoice : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, partner, payment_term, match, total_incl, total_base, total_vat, vat_regime, your_ref, due_date, printed_by, language, subject, intro, paper_type
- sepa.Account : id, partner, iban, bic, remark, primary
- system.SiteConfig : id, default_build_method, simulate_today, site_company, next_partner_id, default_event_type, site_calendar, max_auto_events, clients_account, sales_vat_account, sales_account, suppliers_account, purchases_vat_account, purchases_account, wages_account, clearings_account
- tinymce.TextFieldTemplate : id, user, name, description, text
- uploads.Upload : id, file, mimetype, user, owner_type, owner_id, upload_area, type, description
- uploads.UploadType : id, name, upload_area, max_number, wanted, shortcut, name_fr, name_de
- users.Authority : id, user, authorized
- users.User : id, modified, created, username, password, profile, initials, first_name, last_name, email, remarks, language, partner, access_class, event_type
- vat.InvoiceItem : id, seqno, account, total_incl, total_base, total_vat, vat_class, voucher, title
- vat.VatAccountInvoice : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, partner, payment_term, match, total_incl, total_base, total_vat, vat_regime, your_ref, due_date
- vat.VatRule : id, seqno, start_date, end_date, country, vat_class, vat_regime, rate, can_edit
- vatless.AccountInvoice : id, user, journal, voucher_date, entry_date, accounting_period, number, narration, state, voucher_ptr, partner, payment_term, match, bank_account, your_ref, due_date, amount
- vatless.InvoiceItem : id, seqno, account, voucher, title, amount
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


