# -*- coding: UTF-8 -*-
# Copyright 2017-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

from lino_xl.lib.products.models import *
from lino.mixins import Referrable
from lino.api import _


ProductTypes.clear()
add = ProductTypes.add_item
add('100', _("Products"), 'default', table_name="products.Products")
#add('200', _("Services"), 'services', table_name="products.Services")
# add('300', _("Other"), 'default')

class Product(Product, Referrable):

    class Meta(Product.Meta):
        app_label = 'products'
        abstract = dd.is_abstract_model(__name__, 'Product')

    ref_max_length = 6


class ProductDetail(dd.DetailLayout):

    main = "general #courses sales"
    
    general = dd.Panel("""
    name id 
    product_type cat sales_price tariff
    vat_class sales_account delivery_unit
    description
    """, _("General"))

    # courses = dd.Panel("""
    # courses.EnrolmentsByFee
    # courses.EnrolmentsByOption
    # """, _("Enrolments"))

    sales = dd.Panel("""
    sales.InvoiceItemsByProduct
    """, _("Sales"))


Products.column_names = "name tariff sales_price sales_account *"

#class Services(Products):
#    _product_type = ProductTypes.services
#    column_names = "name sales_account *"

