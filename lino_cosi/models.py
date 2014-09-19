# -*- coding: UTF-8 -*-
# Copyright 2011-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The :xfile:`models.py` module for :ref:`cosi`.
"""

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


@dd.receiver(dd.pre_analyze)
def set_merge_actions(sender, **kw):
    partners = dd.modules.contacts
    for m in (partners.Person, partners.Organisation):
        m.define_action(merge_row=dd.MergeAction(m))

