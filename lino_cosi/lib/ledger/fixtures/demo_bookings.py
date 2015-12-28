# -*- coding: UTF-8 -*-
# Copyright 2012-2015 Luc Saffre
# This file is part of Lino Cosi.
#
# Lino Cosi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Lino Cosi is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with Lino Cosi.  If not, see
# <http://www.gnu.org/licenses/>.


"""
Creates fictive demo bookings:

- monthly purchases (causing costs)
- monthly sales

See also :mod:`lino_cosi.lib.finan.fixtures.demo_bookings`

"""

from __future__ import unicode_literals

import logging
logger = logging.getLogger(__name__)


import datetime
from dateutil.relativedelta import relativedelta as delta

from decimal import Decimal

from django.conf import settings
from lino.utils import Cycler
from lino.api import dd, rt

from lino_cosi.lib.vat.mixins import myround

vat = dd.resolve_app('vat')
sales = dd.resolve_app('sales')

partner_model = settings.SITE.partners_app_label + '.Partner'

current_group = None

# from lino.core.requests import BaseRequest
REQUEST = settings.SITE.login()  # BaseRequest()
MORE_THAN_A_MONTH = datetime.timedelta(days=40)


def objects():

    Journal = rt.modules.ledger.Journal
    Company = dd.resolve_model('contacts.Company')
    Person = dd.resolve_model('contacts.Person')
    Product = dd.resolve_model('products.Product')

    USERS = Cycler(settings.SITE.user_model.objects.all())

    if sales:

        # yield Product(name="Foo", sales_price='399.90')
        # yield Product(name="Bar", sales_price='599.90')
        # yield Product(name="Baz", sales_price='990.00')
        PRODUCTS = Cycler(Product.objects.order_by('id'))
        JOURNAL_S = Journal.objects.get(ref="SLS")
        CUSTOMERS = Cycler(Person.objects.filter(
            gender=dd.Genders.male).order_by('id'))
        assert Person.objects.count() > 0
        ITEMCOUNT = Cycler(1, 2, 3)
        QUANTITIES = Cycler(15, 10, 8, 4)
        # SALES_PER_MONTH = Cycler(2, 1, 3, 2, 0)
        SALES_PER_MONTH = Cycler(5, 4, 1, 8, 6)

    # purchases:
    PROVIDERS = Cycler(Company.objects.filter(
        sepa_accounts__iban__isnull=False).order_by('id'))

    JOURNAL_P = Journal.objects.get(ref="PRC")
    #~ assert JOURNAL_P.dc == accounts.CREDIT
    ACCOUNTS = Cycler(JOURNAL_P.get_allowed_accounts())
    AMOUNTS = Cycler([Decimal(x) for x in
                      "20 29.90 39.90 99.95 199.95 599.95 1599.99".split()])
    AMOUNT_DELTAS = Cycler([Decimal(x)
                           for x in "0 0.60 1.10 1.30 2.50".split()])
    DATE_DELTAS = Cycler((1, 2, 3, 4, 5, 6, 7))
    INFLATION_RATE = Decimal("0.02")

    """"purchase stories" : each story represents a provider who sends
    monthly invoices.

    """
    PURCHASE_STORIES = []
    for i in range(5):
        # provider, (account,amount)
        story = (PROVIDERS.pop(), [])
        story[1].append((ACCOUNTS.pop(), AMOUNTS.pop()))
        if i % 3:
            story[1].append((ACCOUNTS.pop(), AMOUNTS.pop()))
        PURCHASE_STORIES.append(story)

    START_YEAR = dd.plugins.ledger.start_year
    date = datetime.date(START_YEAR, 1, 1)
    end_date = settings.SITE.demo_date(-10)  # + delta(years=-2)
    # end_date = datetime.date(START_YEAR+1, 5, 1)
    # print(20151216, START_YEAR, settings.SITE.demo_date(), end_date - date)
    while date < end_date:

        if sales:
            partner = None
            for i in range(SALES_PER_MONTH.pop()):
                # Every fifth time there are two successive invoices
                # to the same partner.
                if partner is None or i % 5:
                    partner = CUSTOMERS.pop()
                #~ print __file__, date
                invoice = sales.VatProductInvoice(
                    journal=JOURNAL_S,
                    partner=partner,
                    user=USERS.pop(),
                    voucher_date=date + delta(days=5 + i),
                    entry_date=date + delta(days=5 + i + 1),
                )
                    # date=date + delta(days=10 + DATE_DELTAS.pop()))
                yield invoice
                for j in range(ITEMCOUNT.pop()):
                    item = sales.InvoiceItem(
                        voucher=invoice,
                        product=PRODUCTS.pop(),
                        qty=QUANTITIES.pop())
                    item.product_changed(REQUEST)
                    item.before_ui_save(REQUEST)
                    yield item
                invoice.register(REQUEST)
                invoice.save()

        for story in PURCHASE_STORIES:
            vd = date + delta(days=DATE_DELTAS.pop())
            invoice = vat.VatAccountInvoice(
                journal=JOURNAL_P, partner=story[0], user=USERS.pop(),
                voucher_date=vd,
                entry_date=vd + delta(days=1))
            yield invoice
            for account, amount in story[1]:
                amount += amount + \
                    (amount * INFLATION_RATE * (date.year - START_YEAR))
                item = vat.InvoiceItem(voucher=invoice,
                                       account=account,
                                       total_incl=myround(amount) +
                                       AMOUNT_DELTAS.pop())
                item.total_incl_changed(REQUEST)
                item.before_ui_save(REQUEST)
                #~ if item.total_incl:
                    #~ print "20121208 ok", item
                #~ else:
                    #~ if item.product.price:
                        #~ raise Exception("20121208")
                yield item
            invoice.register(REQUEST)
            invoice.save()

        date += delta(months=1)
