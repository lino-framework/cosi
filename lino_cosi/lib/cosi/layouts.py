# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The default :attr:`custom_layouts_module
<lino.core.site.Site.custom_layouts_module>` for Lino Cosi.

"""

from lino.api import rt

rt.actors.products.Products.column_names = "id name cat sales_price *"
rt.actors.products.Products.detail_layout = """
id cat sales_price vat_class delivery_unit
name
description
"""

rt.models.accounts.Accounts.column_names = "\
ref name purchases_allowed group *"

rt.models.countries.Places.detail_layout = """
name country
type parent zip_code id
PlacesByPlace contacts.PartnersByCity
"""
rt.models.accounts.Accounts.detail_layout = """
ref:10 name
group type id default_amount:10 vat_column
needs_partner clearable purchases_allowed
ledger.MovementsByAccount
"""

rt.models.system.SiteConfigs.detail_layout = """
site_company next_partner_id:10
default_build_method simulate_today
"""

