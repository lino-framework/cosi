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
Database models for `lino_cosi.lib.sepa`.

"""

from __future__ import unicode_literals
import logging
from pprint import pformat
import glob
import os
from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from lino.api import dd, _, rt
from lino.core.utils import ChangeWatcher
from .camt import CamtParser
from .fields import IBANField, BICField
from .utils import belgian_nban_to_iban_bic, iban2bic
import time

logger = logging.getLogger(__name__)


class ImportStatements(dd.Action):
    """Import the .xml files found in the directory specified at
    :attr:`import_statements_path
    <lino_cosi.lib.sepa.Plugin.import_statements_path>`.

    End-users invoke this via the menu command :menuselection:`SEPA
    --> Import SEPA`.

    When a file has been successfully imported, Lino deletes it.

    It might happen that an .xml file accidentally gets downloaded a
    second time. Lino does not create these statements again.

    """
    label = _("Import SEPA")
    http_method = 'POST'
    select_rows = False

    def get_view_permission(self, profile):
        """Make it invisible when :attr:`import_statements_path
        <lino_cosi.lib.sepa.Plugin.import_statements_path>` is empty.

        """
        if not dd.plugins.sepa.import_statements_path:
            return False
        return super(ImportStatements, self).get_view_permission(profile)

    def run_from_ui(self, ar):
        pth = dd.plugins.sepa.import_statements_path
        wc = os.path.join(pth, '*.xml')
        dd.logger.info("Importing SEPA statements from %s...", wc)
        count = 0
        if pth:
            for filename in glob.iglob(wc):
                self.import_file(ar, filename)
                count += 1
            msg = "{0} xml files would have been imported.".format(count)
            dd.logger.info(msg)
            return ar.success(msg, alert=_("Success"))
        msg = "No import_statements_path configured."
        return ar.error(msg, alert=_("Error"))

    def import_file(self, ar, filename):
        Account = rt.modules.sepa.Account

        # Parse a CAMT053 XML file.
        parser = CamtParser()
        data_file = open(filename, 'rb').read()
        num = 0
        failed_statements = {}
        try:
            dd.logger.info("Parsing %s with camt.", filename)
            res = parser.parse(data_file)
            if res is None:
                raise Exception("res is None")
            for _statement in res:
                iban = _statement['account_number']
                if iban is None:
                    # msg = "Statement without account number : {0}"
                    failed_statements[num] = "IBAN Not found"
                    continue
                    # raise Exception(msg.format(pformat(_statement)))
                try:
                    account = Account.objects.get(iban=iban)
                except Account.DoesNotExist:
                    account = Account(iban=iban)
                    account.full_clean()
                    account.save()
                except MultipleObjectsReturned:
                    msg = "Found more than one account with IBAN {0}"
                    dd.logger.warning(msg.format(iban))
                s = Statement(account=account,
                              date=_statement['date'].strftime("%Y-%m-%d"),
                              date_done=time.strftime("%Y-%m-%d"),
                              statement_number=_statement['name'],
                              balance_end=_statement['balance_end'],
                              balance_start=_statement['balance_start'],
                              balance_end_real=_statement['balance_end_real'],
                              currency_code=_statement['currency_code'])
                s.save()
                for _movement in _statement['transactions']:
                    # TODO :check if the movement is already imported.
                    if not Movement.objects.filter(
                            unique_import_id=_movement['unique_import_id']).exists():
                        _ref = _movement.get('ref', '') or ''
                        if _movement.remote_account:
                            try:
                                _bank_account = Account.objects.get(iban=_movement.remote_account)
                            except Account.DoesNotExist:
                                _bank_account = Account(iban=_movement.remote_account)
                                _bank_account.full_clean()
                                _bank_account.save()
                            m = Movement(statement=s,
                                         unique_import_id=_movement['unique_import_id'],
                                         movement_date=_movement['date'],
                                         amount=_movement['amount'],
                                         partner_name=_movement.remote_owner,
                                         ref=_ref,
                                         bank_account=_bank_account)
                            m.save()
                num += 1

        except ValueError:
            dd.logger.info("Statement file was not a camt file.")

        if len(failed_statements) == 0:
            msg = "Imported {0} statemenmts from file {1}.".format(num, filename)
            dd.logger.info(msg)
            ar.info(msg)
        else:
            count_statements_imported = num - len(failed_statements)
            msg = "Imported {0} statemenmts from file {1} with {2} statements failed.".format(count_statements_imported,
                                                                                              filename,
                                                                                              len(failed_statements))
            dd.logger.info(msg)
            for i, _statement in enumerate(failed_statements):
                msg_error = "Statement number {0} failed to be imported : {1}.".format(i + 1, failed_statements[_statement])
                dd.logger.info(msg_error)


dd.inject_action('system.SiteConfig', import_sepa=ImportStatements())


class Account(dd.Model):
    """A bank account related to a given :class:`Partner
    <lino.modlib.models.contacts.Partner>`.

    One partner can have more than one bank account.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Account')
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    partner = dd.ForeignKey(
        'contacts.Partner',
        related_name='sepa_accounts', null=True, blank=True)

    iban = IBANField(verbose_name=_("IBAN"))
    bic = BICField(verbose_name=_("BIC"), blank=True)

    remark = models.CharField(_("Remark"), max_length=200, blank=True)

    primary = models.BooleanField(
        _("Primary"),
        default=False,
        help_text=_(
            "Enabling this field will automatically disable any "
            "previous primary account and update "
            "the partner's IBAN and BIC"))

    allow_cascaded_delete = ['partner']

    def __unicode__(self):
        if self.remark:
            return "{0} ({1})".format(self.iban, self.remark)
        return self.iban

    def full_clean(self):
        if self.iban and not self.bic:
            if self.iban[0].isdigit():
                iban, bic = belgian_nban_to_iban_bic(self.iban)
                self.bic = bic
                self.iban = iban
            else:
                self.bic = iban2bic(self.iban) or ''
        super(Account, self).full_clean()

    def after_ui_save(self, ar, cw):
        super(Account, self).after_ui_save(ar, cw)
        if self.primary:
            mi = self.partner
            for o in mi.sepa_accounts.exclude(id=self.id):
                if o.primary:
                    o.primary = False
                    o.save()
                    ar.set_response(refresh_all=True)
            watcher = ChangeWatcher(mi)
            for k in PRIMARY_FIELDS:
                setattr(mi, k, getattr(self, k))
            mi.save()
            watcher.send_update(ar.request)


PRIMARY_FIELDS = dd.fields_list(Account, 'iban bic')


class Statement(dd.Model):
    """A bank statement.

    This data is automaticaly imported by :class:`ImportStatements`.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Statement')
        verbose_name = _("Statement")
        verbose_name_plural = _("Statements")

    def __unicode__(self):
        if self.account:
            if self.date:
                return "{0} ({1})".format(self.account, self.date)
            else:
                return self.account
        return ''

    account = dd.ForeignKey('sepa.Account')
    date = models.DateField(_('Date'), null=True)
    date_done = models.DateTimeField(_('Import Date'), null=True)
    statement_number = models.CharField(_('Statement number'), null=False, max_length=128)
    balance_start = dd.PriceField(_("Initial amount"), null=True)
    balance_end = dd.PriceField(_("Final amount"), null=True)
    balance_end_real = dd.PriceField(_("Real end balance"), null=True)
    currency_code = models.CharField(_('Currency'), max_length=3)

    # fields like statement_number, date, solde_initial, solde_final


class Movement(dd.Model):
    """A movement within a bank statement.

    This data is automaticaly imported by :class:`ImportStatements`.

    """

    class Meta:
        abstract = dd.is_abstract_model(__name__, 'Movement')
        verbose_name = _("Movement")
        verbose_name_plural = _("Movements")

    statement = dd.ForeignKey('sepa.Statement')
    unique_import_id = models.CharField(_('Unique import ID'), max_length=128)
    # movement_number = models.CharField(_("Ref of Mov"), null=False, max_length=32)
    movement_date = models.DateField(_('Movement date'), null=True)
    amount = dd.PriceField(_('Amount'), null=True)
    partner = models.ForeignKey('contacts.Partner', related_name='sepa_movement', null=True)
    partner_name = models.CharField(_('Partner name'), max_length=35)
    bank_account = dd.ForeignKey('sepa.Account', blank=True, null=True)
    ref = models.CharField(_('Ref'), null=False, max_length=35)


from .ui import *
