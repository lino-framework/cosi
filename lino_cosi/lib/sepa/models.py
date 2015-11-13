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
from lino.utils.xmlgen.html import E
from lino.utils import join_elems

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
        if not pth:
            msg = "No import_statements_path configured."
            return ar.error(msg, alert=_("Error"))
        dd.logger.info("Importing XML files from %s...", pth)
        wc = os.path.join(pth, '*.[Xx][Mm][Ll]')
        count = 0
        for filename in glob.iglob(wc):
            self.import_file(ar, filename)
            count += 1
        msg = "{0} XML files have been imported.".format(count)
        dd.logger.info(msg)
        return ar.success(msg, alert=_("Success"))

    def import_file(self, ar, filename):
        """Import the named file, which must be a CAMT053 XML file."""
        Account = rt.modules.sepa.Account
        parser = CamtParser()
        data_file = open(filename, 'rb').read()
        num = 0
        failed_statements = {}
        # try:
        dd.logger.info("Parsing %s with camt.", filename)
        res = parser.parse(data_file)
        if res is None:
            raise Exception("res is None")
        for _statement in res:
            iban = _statement['account_number']
            movements_to_update = False
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
                # raise Exception(msg.format(iban))
                dd.logger.warning(msg.format(iban))
                continue
            if not Statement.objects.filter(
                    statement_number=_statement['name'], account=account).exists():
                s = Statement(account=account,
                              start_date=_statement['start_date'],
                              end_date=_statement['end_date'],
                              # date_done=time.strftime("%Y-%m-%d"),
                              statement_number=_statement['name'],
                              balance_end=_statement['balance_end'],
                              balance_start=_statement['balance_start'],
                              balance_end_real=_statement['balance_end_real'],
                              currency_code=_statement['currency_code'])
            else:
                s = Statement.objects.get(
                    statement_number=_statement['name'], account=account)
                # s.date = _statement['date'].strftime("%Y-%m-%d")
                # s.date_done = time.strftime("%Y-%m-%d")
                s.start_date = _statement['start_date']
                s.end_date = _statement['end_date']
                s.balance_end = _statement['balance_end']
                s.balance_start = _statement['balance_start']
                s.balance_end_real = _statement['balance_end_real']
                s.currency_code = _statement['currency_code']
                movements_to_update = True
            s.save()
            for _movement in _statement['transactions']:
                _ref = _movement.get('ref', '') or ''
                addr = '\n'.join(_movement.remote_owner_address)
                if not Movement.objects.filter(
                        unique_import_id=_movement['unique_import_id']).exists():
                    m = Movement(statement=s,
                                 unique_import_id=_movement['unique_import_id'],
                                 movement_date=_movement['date'],
                                 amount=_movement['amount'],
                                 partner_name=_movement.remote_owner,
                                 ref=_ref,
                                 remote_account=_movement.remote_account or '',
                                 remote_bic=_movement.remote_bank_bic or '',
                                 message=_movement._message or '',
                                 eref=_movement.eref or '',
                                 remote_owner=_movement.remote_owner or '',
                                 remote_owner_address=addr,
                                 remote_owner_city=_movement.remote_owner_city or '',
                                 remote_owner_postalcode=_movement.remote_owner_postalcode or '',
                                 remote_owner_country_code=_movement.remote_owner_country_code or '',
                                 transfer_type=_movement.transfer_type or '',
                                 execution_date=_movement.execution_date or '',
                                 value_date=_movement.value_date or '', )
                    m.save()
                elif movements_to_update:
                    m = Movement.objects.get(unique_import_id=_movement['unique_import_id'])
                    m.statement = s
                    m.movement_date = _movement['date']
                    m.amount = _movement['amount']
                    m.partner_name = _movement.remote_owner
                    m.ref = _ref
                    m.remote_account = _movement.remote_account or ''
                    m.remote_bic = _movement.remote_bank_bic or ''
                    m.message = _movement._message or ' '
                    m.eref = _movement.eref or ' '
                    m.remote_owner = _movement.remote_owner or ' '
                    m.remote_owner_address = addr
                    m.remote_owner_city = _movement.remote_owner_city or ' '
                    m.remote_owner_postalcode = _movement.remote_owner_postalcode or ' '
                    m.remote_owner_country_code = _movement.remote_owner_country_code or ' '
                    m.transfer_type = _movement.transfer_type or ' '
                    m.execution_date = _movement.execution_date or ' '
                    m.value_date = _movement.value_date or ' '
                    m.save()

            num += 1

        # except ValueError:
        #     dd.logger.info("Statement file was not a camt file.")

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
                msg_error = "Statement number {0} failed to be imported : {1}.".format(i + 1,
                                                                                       failed_statements[_statement])
                dd.logger.info(msg_error)
        # Deleting the imported file
        if dd.plugins.sepa.delete_imported_xml_files:
            os.remove(filename)
            msg = "The file {0} has been deleted.".format(filename)
            dd.logger.info(msg)
            ar.info(msg)


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
        return self.statement_number

    account = dd.ForeignKey('sepa.Account')
    start_date = models.DateField(_('Start date'), null=True)
    end_date = models.DateField(_('End date'), null=True)
    # date_done = models.DateTimeField(_('Import Date'), null=True)
    statement_number = models.CharField(
        _('Statement number'), null=False, max_length=128)
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
    movement_date = models.DateField(_('Movement date'), null=True, blank=True)
    amount = dd.PriceField(_('Amount'), null=True, blank=True)
    # partner = models.ForeignKey('contacts.Partner', related_name='sepa_movement', null=True)
    partner_name = models.CharField(_('Partner name'), max_length=35, blank=True)
    remote_account = IBANField(verbose_name=_("IBAN"), blank=True)
    remote_bic = BICField(verbose_name=_("BIC"), blank=True)
    ref = models.CharField(_('Ref'), null=False, max_length=35, blank=True)
    message = models.TextField(_('Message'), blank=True)
    eref = models.CharField(_('End to end reference'), max_length=128)
    remote_owner = models.CharField(_('Remote owner'), max_length=128, blank=True)
    remote_owner_address = models.CharField(_('Remote owner adress'), max_length=128, blank=True)
    remote_owner_city = models.CharField(_('Remote owner city'), max_length=32, blank=True)
    remote_owner_postalcode = models.CharField(_('Remote owner postal code'), max_length=10, blank=True)
    remote_owner_country_code = models.CharField(_('Remote owner country code'), max_length=4, blank=True)
    transfer_type = models.CharField(_('Transfer type'), max_length=32, blank=True)
    execution_date = models.DateField(_('Execution date'), null=True, blank=True)
    value_date = models.DateField(_('Value date'), null=True, blank=True)

    @dd.displayfield(_("Remote account"))
    def remote_html(self, ar):
        elems = []
        elems += [self.remote_account, " "]
        elems += ["(BIC:", self.remote_bic, ")"]
        elems.append(E.br())
        elems += [E.b(self.remote_owner), ", "]
        elems.append(E.br())
        elems += [self.remote_owner_address, ", "]
        elems += [self.remote_owner_postalcode, " "]
        elems += [self.remote_owner_city, " "]
        elems += [self.remote_owner_country_code]
        return E.div(*elems)

    @dd.displayfield(_("Message"))
    def message_html(self, ar):
        from django.utils.translation import ugettext as _
        elems = []
        # elems += [_("Date"), dd.fds(self.movement_date), " "]
        # elems += [_("Amount"), ' ', E.b(unicode(self.amount)), " "]
        # self.execution_date
        elems += self.message.splitlines()
        elems.append(E.br())
        elems += [_("ref:"), ': ', self.ref, ' ']
        elems += [_("eref:"), ': ', self.eref]
        elems.append(E.br())
        elems += [_("TT:"), ': ', E.b(self.transfer_type), ' ']
        elems += [_("Value date"), ': ', E.b(dd.fds(self.value_date)), " "]
        elems += [_("Execution date"), ': ',
                  E.b(dd.fds(self.execution_date)), " "]
        return E.div(*elems)

        
from .ui import *
