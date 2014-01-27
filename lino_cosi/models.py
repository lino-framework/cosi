# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# This file is part of the Lino project.
# Lino is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
The :xfile:`models.py` module for :ref:`cosi`.
"""

import os
import cgi
import datetime

from django.db import models
#~ from django.db.models import Q
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


#~ from lino import mixins
from lino import dd


def site_setup(site):
    site.modules.system.SiteConfigs.set_detail_layout(
        """
        site_company next_partner_id:10
        default_build_method
        clients_account   sales_account     sales_vat_account
        suppliers_account purchases_account purchases_vat_account
        """)

    site.modules.accounts.Accounts.set_detail_layout(
        """
        ref:10 name id:5
        seqno chart group type clearable
        ledger.MovementsByAccount
        """)


# @dd.when_prepared('contacts.Person', 'contacts.Company')
# def hide_region(model):
#     model.hide_elements('region')


@dd.receiver(dd.pre_analyze)
def set_merge_actions(sender, **kw):
    partners = dd.modules.contacts
    for m in (partners.Person, partners.Organisation):
        m.define_action(merge_row=dd.MergeAction(m))

