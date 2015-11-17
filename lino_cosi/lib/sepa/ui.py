# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
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
Tables for `lino_cosi.lib.sepa`.

"""

from __future__ import unicode_literals

from lino.api import dd, _
from .roles import SepaUser, SepaStaff
from lino.modlib.contacts.roles import ContactsUser


class Accounts(dd.Table):
    required_roles = dd.login_required(SepaStaff)
    model = 'sepa.Account'
    detail_layout = """
    partner:30 iban:40 bic:20 remark:15
    sepa.StatementsByAccount
    """
    insert_layout = """
    partner
    iban bic
    """


class AccountsByPartner(Accounts):
    """Show the bank account(s) defined for a given partner. To be
    included to a detail window on partner.

    """
    required_roles = dd.login_required((ContactsUser, SepaUser))
    master_key = 'partner'
    column_names = 'iban bic remark primary *'
    order_by = ['iban']
    stay_in_grid = True
    auto_fit_column_widths = True
    insert_layout = """
    iban bic
    remark
    """


class StatementDetail(dd.FormLayout):
    main = """
    top_left top_right
    sepa.MovementsByStatement
    """

    top_left = """
    account:20 account__partner:30
    statement_number sequence_number currency_code
    """

    top_right = """
    balance_start start_date
    balance_end end_date
    """


class Statements(dd.Table):
    required_roles = dd.login_required(SepaStaff)
    model = 'sepa.Statement'
    column_names = ('account account__partner sequence_number statement_number:20 '
                    'balance_start start_date balance_end end_date '
                    'currency_code *')
    order_by = ["start_date"]
    detail_layout = StatementDetail()
    auto_fit_column_widths = True
    editable = False

    # insert_layout = dd.FormLayout("""
    # account date
    # statement_number
    # balance_start balance_end
    # """, window_size=(60, 'auto'))


class StatementsByAccount(Statements):
    required_roles = dd.login_required(SepaUser)
    master_key = 'account'
    column_names = 'sequence_number balance_start start_date balance_end end_date currency_code *'
    auto_fit_column_widths = True


class Movements(dd.Table):
    required_roles = dd.login_required(SepaStaff)
    model = 'sepa.Movement'
    editable = False
    detail_layout = """
    statement:30 unique_import_id:30 movement_date:20 amount:20
    remote_account:20 remote_bic:10 ref:20 eref:10
    remote_owner:20 remote_owner_address:20 remote_owner_city:20 remote_owner_postalcode:20
    remote_owner_country_code:20 transfer_type:20 execution_date:20 value_date:20
    message
    """


class MovementsByStatement(Movements):
    required_roles = dd.login_required(SepaUser)
    master_key = 'statement'
    column_names = 'movement_date amount remote_html message_html *'
    auto_fit_column_widths = True


class OrphanedAccounts(Accounts):
    required_roles = dd.login_required(SepaStaff)
    model = 'sepa.Account'
    order_by = ["id"]
    label = _("Orphaned bank accounts")
    insert_layout = """
    partner
    iban bic
    """

    @classmethod
    def get_queryset(self, ar):
        return self.model.objects.filter(partner=None)
