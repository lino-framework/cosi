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
        self.new_statements = 0
        self.updated_statements = 0
        self.failed_statements = 0
        self.imported_files = 0
        dd.logger.info("Importing XML files from %s...", pth)
        wc = os.path.join(pth, '*.[Xx][Mm][Ll]')
        for filename in glob.iglob(wc):
            self.import_file(ar, filename)
        msg = "{0} XML files with {1} new and {2} updated " \
              "statements have been imported."
        msg = msg.format(
            self.imported_files, self.new_statements, self.updated_statements)
        dd.logger.info(msg)
        return ar.success(msg, alert=_("Success"))

    def import_file(self, ar, filename):
        """Import the named file, which must be a CAMT053 XML file."""
        Account = rt.modules.sepa.Account
        parser = CamtParser()
        data_file = open(filename, 'rb').read()
        # imported_statements = 0
        # try:
        dd.logger.info("Parsing %s with camt.", filename)
        res = parser.parse(data_file)
        self.imported_files += 1
        failed_statements = 0
        if res is None:
            raise Exception("res is None")
        for stmt in res:
            iban = stmt['account_number']
            unique_id = stmt['name']
            movements_to_update = False
            if iban is None:
                dd.logger.warning("Statement without IBAN : %s", unique_id)
                failed_statements += 1
                continue
                # raise Exception(msg.format(pformat(stmt)))
            try:
                account = Account.objects.get(iban=iban)
            except Account.DoesNotExist:
                account = Account(iban=iban)
                account.full_clean()
                account.save()
            except MultipleObjectsReturned:
                dd.logger.warning(
                    "Found more than one account with IBAN %s", iban)
                failed_statements += 1
                continue
            if Statement.objects.filter(
                statement_number=stmt['name'], account=account).exists():
                s = Statement.objects.get(
                    statement_number=stmt['name'], account=account)
                # s.date = stmt['date'].strftime("%Y-%m-%d")
                # s.date_done = time.strftime("%Y-%m-%d")
                s.start_date = stmt['start_date']
                s.end_date = stmt['end_date']
                s.balance_end = stmt['balance_end']
                s.balance_start = stmt['balance_start']
                s.balance_end_real = stmt['balance_end_real']
                s.currency_code = stmt['currency_code']
                movements_to_update = True
                self.new_statements += 1
            else:
                s = Statement(account=account,
                              start_date=stmt['start_date'],
                              end_date=stmt['end_date'],
                              # date_done=time.strftime("%Y-%m-%d"),
                              statement_number=stmt['name'],
                              balance_end=stmt['balance_end'],
                              balance_start=stmt['balance_start'],
                              balance_end_real=stmt['balance_end_real'],
                              currency_code=stmt['currency_code'])
                self.updated_statements += 1

            s.save()
            for mvmt in stmt['transactions']:
                _ref = mvmt.get('ref', '')
                addr = '\n'.join(mvmt.remote_owner_address)
                mvmt_id = mvmt['unique_import_id']
                if not Movement.objects.filter(
                        unique_import_id=mvmt_id).exists():
                    m = Movement(statement=s,
                                 unique_import_id=mvmt_id,
                                 movement_date=mvmt['date'],
                                 amount=mvmt['amount'],
                                 partner_name=mvmt.remote_owner,
                                 ref=_ref,
                                 remote_account=mvmt.remote_account or '',
                                 remote_bic=mvmt.remote_bank_bic or '',
                                 message=mvmt._message or '',
                                 eref=mvmt.eref or '',
                                 remote_owner=mvmt.remote_owner or '',
                                 remote_owner_address=addr,
                                 remote_owner_city=mvmt.remote_owner_city or '',
                                 remote_owner_postalcode=mvmt.remote_owner_postalcode or '',
                                 remote_owner_country_code=mvmt.remote_owner_country_code or '',
                                 transfer_type=mvmt.transfer_type or '',
                                 execution_date=mvmt.execution_date or '',
                                 value_date=mvmt.value_date or '', )
                    m.save()
                elif movements_to_update:
                    m = Movement.objects.get(unique_import_id=mvmt_id)
                    m.statement = s
                    m.movement_date = mvmt['date']
                    m.amount = mvmt['amount']
                    m.partner_name = mvmt.remote_owner
                    m.ref = _ref
                    m.remote_account = mvmt.remote_account or ''
                    m.remote_bic = mvmt.remote_bank_bic or ''
                    m.message = mvmt._message or ' '
                    m.eref = mvmt.eref or ' '
                    m.remote_owner = mvmt.remote_owner or ' '
                    m.remote_owner_address = addr
                    m.remote_owner_city = mvmt.remote_owner_city or ' '
                    m.remote_owner_postalcode = mvmt.remote_owner_postalcode or ' '
                    m.remote_owner_country_code = mvmt.remote_owner_country_code or ' '
                    m.transfer_type = mvmt.transfer_type or ' '
                    m.execution_date = mvmt.execution_date or ' '
                    m.value_date = mvmt.value_date or ' '
                    m.save()
                else:
                    dd.logger.warning(
                        "Existing transaction in a new statement?! %s", mvmt_id)

        # except ValueError:
        #     dd.logger.info("Statement file was not a camt file.")

        # msg = "Imported {0} statements from file {1}.".format(
        #     self.new_statements, self.updated_statements, filename)
        # dd.logger.info(msg)
        # ar.info(msg)
        if failed_statements > 0:
            dd.logger.warning(
                "%d statements were NOT imported from %s",
                failed_statements, filename)
            self.failed_statements += failed_statements
        elif dd.plugins.sepa.delete_imported_xml_files:
            # Delete the imported file if there were no errors
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
