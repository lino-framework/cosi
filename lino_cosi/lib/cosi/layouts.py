# -*- coding: UTF-8 -*-
# Copyright 2017 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Cosi.

"""

from lino.api import rt

rt.models.products.Products.column_names = "id name cat sales_price *"
rt.models.products.Products.detail_layout = """
id cat sales_price vat_class delivery_unit
name
description
"""

rt.models.ledger.Accounts.column_names = "\
ref name purchases_allowed sheet_item *"

rt.models.countries.Places.detail_layout = """
name country
type parent zip_code id
PlacesByPlace contacts.PartnersByCity
"""
rt.models.ledger.Accounts.detail_layout = """
ref:10 name
sheet_item id default_amount:10 vat_column
needs_partner clearable purchases_allowed
ledger.MovementsByAccount
"""

rt.models.system.SiteConfigs.detail_layout = """
site_company next_partner_id:10
default_build_method simulate_today
"""

