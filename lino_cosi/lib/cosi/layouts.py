# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
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

