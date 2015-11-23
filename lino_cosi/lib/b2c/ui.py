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
    iban bic last_movement partners
    b2c.StatementsByAccount
    """
    column_names = "iban bic last_movement partners *"
    editable = False


class StatementDetail(dd.FormLayout):
    main = """
    top_left top_right
    b2c.MovementsByStatement
    """

    top_left = """
    account:20 local_currency
    statement_number
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
    


class Movements(dd.Table):
    required_roles = dd.login_required(SepaUser)
    model = 'b2c.Movement'
    editable = False
    detail_layout = """
    statement:30 seqno booking_date:20 amount:20
    remote_account:20 remote_bic:10 eref:10
    remote_owner:20 remote_owner_address:20 remote_owner_city:20 remote_owner_postalcode:20
    remote_owner_country_code:20 transfer_type:20 value_date:20
    message
    """


class MovementsByStatement(Movements):
    required_roles = dd.login_required(SepaUser)
    master_key = 'statement'
    column_names = 'booking_date amount remote_html message_html *'
    auto_fit_column_widths = True


