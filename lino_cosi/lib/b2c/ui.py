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
Tables for `lino_cosi.lib.b2c`.

"""

from __future__ import unicode_literals

from lino.api import dd, _
from lino_cosi.lib.sepa.roles import SepaUser


class Accounts(dd.Table):
    required_roles = dd.login_required(SepaUser)
    model = 'b2c.Account'
    detail_layout = """
    iban bic last_transaction owner_name account_name partners
    b2c.StatementsByAccount
    """
    column_names = "iban bic last_transaction partners owner_name account_name *"
    editable = False


class StatementDetail(dd.FormLayout):
    main = """
    top_left top_right
    b2c.TransactionsByStatement
    """

    top_left = """
    account account__owner_name
    account__account_name statement_number local_currency
    """

    top_right = """
    balance_start start_date
    balance_end end_date
    """


class Statements(dd.Table):
    required_roles = dd.login_required(SepaUser)
    model = 'b2c.Statement'
    column_names = ('account statement_number '
                    'balance_start start_date balance_end end_date '
                    'local_currency *')
    order_by = ["-start_date"]
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
    column_names = 'statement_number balance_start start_date balance_end end_date local_currency *'
    auto_fit_column_widths = True
    

class TransactionDetail(dd.FormLayout):
    main = """
    statement seqno booking_date value_date amount
    remote_account remote_bic eref txcd_text
    remote_owner
    addr_left addr_right
    message
    """
    addr_left = "remote_owner_address"
    addr_right = """
    remote_owner_city
    remote_owner_postalcode
    remote_owner_country_code
    """


class Transactions(dd.Table):
    required_roles = dd.login_required(SepaUser)
    model = 'b2c.Transaction'
    editable = False
    detail_layout = TransactionDetail()
    column_names = "statement seqno value_date amount remote_account remote_owner *"


class TransactionsByStatement(Transactions):
    required_roles = dd.login_required(SepaUser)
    master_key = 'statement'
    column_names = 'booking_date amount remote_html message_html *'
    auto_fit_column_widths = True


