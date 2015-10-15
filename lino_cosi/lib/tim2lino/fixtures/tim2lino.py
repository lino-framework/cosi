# -*- coding: UTF-8 -*-
# Copyright 2009-2015 Luc Saffre
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

"""Import legacy data from TIM (basic version).

Usage:

- :attr:`legacy_data_path <lino.core.site.Site.legacy_data_path>` must
  point to the TIM data path, e.g.::

      legacy_data_path = '~/vbshared2/drives/L/backup/data/privat'

- Add ``'tim2lino'`` to your
  :attr:`demo_fixtures <lino.core.site.Site.demo_fixtures>`.

- Run :manage:`initdb_demo`.

"""
from __future__ import unicode_literals

GET_THEM_ALL = True

import os
import datetime
from decimal import Decimal
# from lino.utils.quantities import Duration

from clint.textui import puts, progress
from dateutil import parser as dateparser

from django.conf import settings
from django.core.exceptions import ValidationError

from lino.utils import dbfreader
from lino.utils import dblogger
from lino.utils import dpy

from lino_cosi.lib.accounts.choicelists import AccountTypes

from lino.core.utils import obj2str
from lino.core.utils import is_valid_email

from lino_cosi.lib.ledger.choicelists import JournalGroups

from lino.api import dd, rt

Activity = dd.resolve_model('pcsw.Activity')
Country = dd.resolve_model('countries.Country')
Place = dd.resolve_model('countries.Place')
Person = dd.resolve_model("contacts.Person")
Company = dd.resolve_model("contacts.Company")
Account = dd.resolve_model('accounts.Account')
Group = dd.resolve_model('accounts.Group')
Journal = dd.resolve_model('ledger.Journal')
Movement = dd.resolve_model('ledger.Movement')
# potentially UnresolvedModel:
Household = dd.resolve_model('households.Household')
List = dd.resolve_model('lists.List')

if True:
    users = dd.resolve_app('users')
    tickets = dd.resolve_app('tickets')
    clocking = dd.resolve_app('clocking')
    households = dd.resolve_app('households')
    vat = dd.resolve_app('vat')
    sales = dd.resolve_app('sales')
    ledger = dd.resolve_app('ledger')
    accounts = dd.resolve_app('accounts')
    products = dd.resolve_app('products')
    contacts = dd.resolve_app('contacts')
    finan = dd.resolve_app('finan')
    sepa = dd.resolve_app('sepa')
    lists = dd.resolve_app('lists')


def dbfmemo(s):
    s = s.replace('\r\n', '\n')
    s = s.replace(u'\xec\n', '')
    # s = s.replace(u'\r\nì',' ')
    if u'ì' in s:
        raise Exception("20121121 %r" % s)
    return s.strip()

# def convert_username(name):
    # return name.lower()

from lino_cosi.lib.vat.choicelists import VatClasses


def tax2vat(idtax):
    idtax = idtax.strip()
    if idtax == 'D20':
        return VatClasses.normal
    elif idtax == 'D18':
        return VatClasses.normal
    elif idtax == '0':
        return VatClasses.exempt
    elif idtax == 'IS':
        return VatClasses.normal
    elif idtax == 'XS':
        return VatClasses.normal
    else:
        return VatClasses.normal
    raise Exception("Unknown VNl->IdTax %r" % idtax)


def pcmn2type(idgen):
    if idgen[0] == '6':
        return AccountTypes.expenses
    if idgen[0] == '7':
        return AccountTypes.incomes
    if idgen[0] == '4':
        return AccountTypes.liabilities
    return AccountTypes.assets


def tim2bool(x):
    if not x.strip():
        return False
    return True


def convert_gender(v):
    if v in ('W', 'F'):
        return 'F'
    if v == 'M':
        return 'M'
    return None


def mton(s):  # PriceField
    s = s.strip()
    if not s:
        return None
    if s != "GRATIS":
        # TIM accepted an (erroneous) amount '36535..23' as 36535
        # (omitting the part after the duplicated ".")
        i = s.find('..')
        if i != -1:
            s = s[:i]
        return Decimal(s)
    return Decimal()


def qton(s):  # QuantityField
    return s.strip()
    # s = s.strip()
    # if s:
        # if ':' in s: return Duration(s)
        # if s.endswith('%'):
            # return Decimal(s[:-1]) / 100
        # return Decimal(s)
    # return None


def isolang(x):
    if x == 'K':
        return 'et'
    if x == 'E':
        return 'en'
    if x == 'D':
        return 'de'
    if x == 'F':
        return 'fr'
    # if x == 'N' : return 'nl'


def store_date(row, obj, rowattr, objattr):
    v = row[rowattr]
    if v:
        if isinstance(v, basestring):
            v = dateparser.parse(v)
        setattr(obj, objattr, v)


def year_num(iddoc):
    # TODO: handle data before A.D. 2000
    year = ledger.FiscalYears.from_int(2000 + int(iddoc[:2]))
    num = int(iddoc[2:])
    return (year, num)


def row2jnl(row):
    try:
        jnl = Journal.objects.get(ref=row.idjnl)
        year, num = year_num(row.iddoc)
        # cl = sales.Invoice
        return jnl, year, num
    except Journal.DoesNotExist:
        return None, None, None


def ticket_state(idpns):
    if idpns == ' ':
        return tickets.TicketStates.new
    if idpns == 'A':
        return tickets.TicketStates.waiting
    if idpns == 'C':
        return tickets.TicketStates.fixed
    if idpns == 'X':
        return tickets.TicketStates.cancelled
    return tickets.TicketStates.new
    # return None  # 20120829 tickets.TicketStates.blank_item

# def country2kw(row,kw):


def try_full_clean(i):
    while True:
        try:
            i.full_clean()
        except ValidationError as e:
            if not hasattr(e, 'message_dict'):
                raise
            for k in e.message_dict.keys():
                fld = i._meta.get_field(k)
                v = getattr(i, k)
                setattr(i, k, fld.default)
                dblogger.warning(
                    "%s : ignoring value %r for %s : %s",
                    obj2str(i), v, k, e)
        return


class TimLoader(object):

    LEN_IDGEN = 6

    archived_tables = set()
    archive_name = None
    codepage = 'cp850'
    # codepage = 'cp437'
    # etat_registered = "C"¹
    etat_registered = "¹"

    sales_gen2art = dict()
    """A dict which maps a `GEN->IdGen` to a product instance or id.
    
    """

    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.VENDICT = dict()
        self.FINDICT = dict()
        self.GROUPS = dict()
        self.languages = dd.resolve_languages(
            dd.plugins.tim2lino.languages)
        self.must_register = []
        self.must_match = []

    def get_user(self, idusr=None):
        return self.ROOT

    def par_class(self, row):
        # wer eine nationalregisternummer hat ist eine Person, selbst wenn er
        # auch eine MwSt-Nummer hat.
        if True:  # must convert them manually
            return Company
        prt = row.idprt
        if prt == 'O':
            return Company
        elif prt == 'L':
            return List
        elif prt == 'P':
            return Person
        elif prt == 'F':
            return Household
        # dblogger.warning("Unhandled PAR->IdPrt %r",prt)

    def dc2lino(self, dc):
        if dc == "D":
            return accounts.DEBIT
        elif dc == "C":
            return accounts.CREDIT
        raise Exception("Invalid D/C value %r" % dc)

    def get_customer(self, pk):
        pk = pk.strip()
        if not pk:
            return None
        pk = self.par_pk(pk)
        try:
            return contacts.Partner.objects.get(pk=pk)
        except contacts.Partner.DoesNotExist:
            return None

    def par_pk(self, pk):
        if pk.startswith('T'):
            return 3000 + int(pk[1:]) - 256
        else:
            return int(pk)

    def store(self, kw, **d):
        for k, v in d.items():
            if v is not None:
                if isinstance(v, basestring):
                    v = self.decode_string(v).strip()
            # if v:
                kw[k] = v

    def short2iso(self, s):
        if s == 'B':
            return 'BE'
        if s == 'D':
            return 'DE'
        if s == 'F':
            return 'FR'
        if s == 'L':
            return 'LU'
        if s == 'E':
            return 'ES'
        if s == 'H':
            return 'HU'
        if s == 'I':
            return 'IT'
        if s == 'USA':
            return 'US'
        if s == 'A':
            return 'AT'
        if s == 'AUS':
            return 'AU'
        if s == 'BEN':
            return 'BJ'
        if s == 'ANG':
            return 'AO'
        if s == 'TUN':
            return 'TN'
        if s == 'EST':
            return 'EE'
        if s == 'SLO':
            return 'SK'
        if s == 'S':
            return 'SE'
        if s == 'D-':
            return 'DE'
        if s == 'COL':
            return 'CO'
        if s == 'CAM':
            return 'CM'
        if s == 'SF':
            return 'FI'
        if s == 'VIE':
            return ''
        if s == 'BRA':
            return 'BR'
        return s
        # if s == 'AU': return 'AU'
        # if s == 'NL': return 'NL'
        # raise Exception("Unknown short country code %r" % s)

    def load_dbf(self, tableName, row2obj=None):
        if row2obj is None:
            row2obj = getattr(self, 'load_' + tableName[-3:].lower())
        fn = self.dbpath
        if self.archive_name is not None:
            if tableName in self.archived_tables:
                fn = os.path.join(fn, self.archive_name)
        fn = os.path.join(fn, tableName)
        fn += dd.plugins.tim2lino.dbf_table_ext
        if dd.plugins.tim2lino.use_dbf_py:
            dblogger.info("Loading %s...", fn)
            import dbf  # http://pypi.python.org/pypi/dbf/
            # table = dbf.Table(fn)
            table = dbf.Table(fn, codepage=self.codepage)
            # table.use_deleted = False
            table.open()
            # print table.structure()
            dblogger.info("Loading %d records from %s (%s)...",
                          len(table), fn, table.codepage)
            for record in table:
                if not dbf.is_deleted(record):
                    try:
                        yield row2obj(record)
                    except Exception as e:
                        dblogger.warning(
                            "Failed to load record %s from %s : %s",
                            record, tableName, e)

                    # i = row2obj(record)
                    # if i is not None:
                    #     yield settings.TIM2LINO_LOCAL(tableName, i)
            table.close()
        else:
            f = dbfreader.DBFFile(fn, codepage="cp850")
            dblogger.info("Loading %d records from %s...", len(f), fn)
            f.open()
            for dbfrow in f:
                try:
                    i = row2obj(dbfrow)
                    if i is not None:
                        yield settings.TIM2LINO_LOCAL(tableName, i)
                except Exception as e:
                    dblogger.warning("Failed to load record %s : %s",
                                     dbfrow, e)
            f.close()

        self.after_load(tableName)

    def load_gen2group(self, row, **kw):
        idgen = row.idgen.strip()
        if not idgen:
            return
        if len(idgen) < self.LEN_IDGEN:
            # dclsel = row.dclsel.strip()
            # kw.update(chart=accounts.Chart.objects.get(pk=1))
            kw.update(chart=self.CHART)
            kw.update(ref=idgen)
            kw.update(account_type=pcmn2type(idgen))
            self.babel2kw('libell', 'name', row, kw)
            # def names2kw(kw,*names):
                # names = [n.strip() for n in names]
                # kw.update(name=names[0])
            # names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            """TIM accepts empty GEN->Libell fields. In that 
            case we take the ref as name.
            """
            kw.setdefault('name', idgen)
            ag = accounts.Group(**kw)
            self.GROUPS[idgen] = ag
            yield ag

    def load_gen2account(self, row, **kw):
        idgen = row.idgen.strip()
        if not idgen:
            return
        if len(idgen) == self.LEN_IDGEN:
            ag = None
            for length in range(len(idgen), 0, -1):
                # print idgen[:length]
                ag = self.GROUPS.get(idgen[:length])
                if ag is not None:
                    break
            # dclsel = row.dclsel.strip()
            # kw.update(chart=accounts.Chart.objects.get(pk=1))
            kw.update(ref=idgen)
            kw.update(group=ag)
            kw.update(chart=self.CHART)
            kw.update(type=pcmn2type(idgen))
            self.babel2kw('libell', 'name', row, kw)
            # def names2kw(kw,*names):
                # names = [n.strip() for n in names]
                # kw.update(name=names[0])
            # names2kw(kw,row.libell1,row.libell2,row.libell3,row.libell4)
            obj = accounts.Account(**kw)
            # if idgen == "612410":
                # raise Exception(20131116)
            # dblogger.info("20131116 %s",dd.obj2str(obj))
            # dblogger.info("20131116 ACCOUNT %s ",obj)
            yield obj

    def load_jnl(self, row, **kw):
        vcl = None
        kw.update(ref=row.idjnl, name=row.libell)
        kw.update(chart=self.CHART)
        kw.update(dc=self.dc2lino(row.dc))
        if row.alias == 'VEN':
            if row.idctr == 'V':
                kw.update(trade_type=vat.TradeTypes.sales)
                kw.update(journal_group=JournalGroups.sales)
                vcl = sales.VatProductInvoice
            elif row.idctr == 'E':
                kw.update(trade_type=vat.TradeTypes.purchases)
                vcl = vat.VatAccountInvoice
                kw.update(journal_group=JournalGroups.purchases)
            else:
                raise Exception("Invalid JNL->IdCtr '{0}'".format(row.idctr))
        elif row.alias == 'FIN':
            idgen = row.idgen.strip()
            kw.update(journal_group=JournalGroups.financial)
            if idgen:
                kw.update(account=self.CHART.get_account_by_ref(idgen))
                if idgen.startswith('58'):
                    kw.update(trade_type=vat.TradeTypes.purchases)
                    vcl = finan.PaymentOrder
                elif idgen.startswith('5'):
                    vcl = finan.BankStatement
            else:
                vcl = finan.JournalEntry
        if vcl is None:
            raise Exception("Journal not recognized: %s" % row.idjnl)

        return vcl.create_journal(**kw)

    def load_fin(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            raise Exception("No journal for FIN record %s" % row)
        kw.update(year=year)
        kw.update(number=number)
        # kw.update(id=pk)
        kw.update(date=row.date)
        kw.update(user=self.get_user())
        kw.update(balance1=mton(row.mont1))
        kw.update(balance2=mton(row.mont2))
        doc = jnl.create_voucher(**kw)
        self.FINDICT[(jnl, year, number)] = doc
        # print row.etat
        if row.etat == self.etat_registered:
            self.must_register.append(doc)
        return doc

    def load_fnl(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            raise Exception("No journal for FNL record %s" % row)
        doc = self.FINDICT.get((jnl, year, number))
        if doc is None:
            raise Exception("FNL %r without document" %
                            list(jnl, year, number))
        try:
            kw.update(seqno=int(row.line.strip()))
        except ValueError:
            pass  # some lines contain "***"
        if row.date:
            kw.update(date=row.date)
        try:
            if row.idctr == ('V'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(
                    account=vat.TradeTypes.sales.get_partner_account())
            elif row.idctr == ('E'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(
                    account=vat.TradeTypes.purchases.get_partner_account())
            elif row.idctr == ('G'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(
                    account=vat.TradeTypes.wages.get_partner_account())
            elif row.idctr == ('S'):
                kw.update(partner_id=self.par_pk(row.idcpt.strip()))
                kw.update(
                    account=vat.TradeTypes.clearings.get_partner_account())
            else:
                a = accounts.Account.objects.get(ref=row.idcpt.strip())
                kw.update(account=a)
            kw.update(amount=mton(row.mont))
            kw.update(dc=self.dc2lino(row.dc))
        except Exception as e:
            dblogger.warning(
                "Failed to load FNL line %s from %s : %s", row, kw, e)
            raise
        try:
            item = doc.add_voucher_item(**kw)
            match = row.match.strip()
            if match:
                self.must_match.append((doc, item, match))
            return item
        except Exception as e:
            dblogger.warning(
                "Failed to load FNL line %s from %s : %s", row, kw, e)

    def load_ven(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            return
        kw.update(year=year)
        kw.update(number=number)
        # kw.update(id=pk)
        partner = self.get_customer(row.idpar)
        if partner is None:
            raise Exception("No partner id {0} in {1}".format(row.idpar, row))
        else:
            kw.update(partner=partner)
        if jnl.trade_type.name == 'sales':
            # kw.update(imode=self.DIM)
            if row.idprj.strip():
                kw.update(project_id=int(row.idprj.strip()))
            kw.update(discount=mton(row.remise))
        elif jnl.trade_type.name == 'purchases':
            pass
            # kw.update(partner=contacts.Partner.objects.get(
            #     pk=self.par_pk(row.idpar)))
            # partner=contacts.Partner.objects.get(pk=self.par_pk(row.idpar))
        else:
            raise Exception("Unknown TradeType %r" % jnl.trade_type)
        kw.update(date=row.date)
        kw.update(user=self.get_user(row.auteur))
        kw.update(total_excl=mton(row.montr))
        kw.update(total_vat=mton(row.montt))
        doc = jnl.create_voucher(**kw)
        # doc.partner = partner
        # doc.full_clean()
        # doc.save()
        self.VENDICT[(jnl, year, number)] = doc
        if row.etat == self.etat_registered:
            self.must_register.append(doc)
        match = row.match.strip()
        if match:
            self.must_match.append((doc, doc, match))
        return doc

    def load_vnl(self, row, **kw):
        jnl, year, number = row2jnl(row)
        if jnl is None:
            return
        doc = self.VENDICT.get((jnl, year, number))
        if doc is None:
            raise Exception("VNL {0} without document".format(
                [jnl, year, number]))
        # dblogger.info("20131116 %s %s",row.idjnl,row.iddoc)
        # doc = jnl.get_document(year,number)
        # try:
            # doc = jnl.get_document(year,number)
        # except Exception,e:
            # dblogger.warning(str(e))
            # return
        # kw.update(document=doc)
        kw.update(seqno=int(row.line.strip()))
        idart = row.idart.strip()
        if isinstance(doc, sales.VatProductInvoice):
            if row.code in ('A', 'F'):
                kw.update(product=products.Product.get_by_ref(idart))
            elif row.code == 'G':
                a = self.vnlg2product(row)
                if a is not None:
                    kw.update(product=a)
            kw.update(unit_price=mton(row.prixu))
            kw.update(qty=qton(row.qte))
        elif isinstance(doc, vat.VatAccountInvoice):
            if row.code == 'G':
                kw.update(account=idart)
        kw.update(title=row.desig.strip())
        kw.update(vat_class=tax2vat(row.idtax))
        mb = mton(row.cmont)
        mv = mton(row.montt)
        kw.update(total_base=mb)
        kw.update(total_vat=mv)
        if mb is not None and mv is not None:
            kw.update(total_incl=mb+mv)
        # kw.update(qty=row.idtax.strip())
        # kw.update(qty=row.montt.strip())
        # kw.update(qty=row.attrib.strip())
        # kw.update(date=row.date)
        try:
            return doc.add_voucher_item(**kw)
        except Exception as e:
            dblogger.warning("Failed to load VNL line %s from %s : %s",
                             row, kw, e)

    def vnlg2product(self, row):
        a = row.idart.strip()
        return self.sales_gen2art.get(a)

    # Countries already exist after initial_data, but their short_code is
    # needed as lookup field for Places.
    def load_nat(self, row):
        if not row['isocode'].strip():
            return
        try:
            country = Country.objects.get(
                isocode=row['isocode'].strip())
        except Country.DoesNotExist:
            country = Country(isocode=row['isocode'].strip())
            country.name = row['name'].strip()
        if row['idnat'].strip():
            country.short_code = row['idnat'].strip()
        return country

    def load_plz(self, row):
        pk = row.pays.strip()
        if not pk:
            return
        name = row.nom.strip() or row.cp.strip()
        if not name:
            return

        if False:  # severe
            country = Country.objects.get(isocode=self.short2iso(pk))
            # country = Country.objects.get(short_code=pk)
        else:
            try:
                country = Country.objects.get(isocode=self.short2iso(pk))
                # country = Country.objects.get(short_code=pk)
            except Country.DoesNotExist:
                dblogger.warning(
                    "Ignored PLZ %s (with invalid country %s)", row, pk)
                return
        zip_code = row['cp'].strip()
        if Place.objects.filter(zip_code=zip_code, country=country).exists():
            dblogger.warning(
                "Ignored PLZ %s (duplicate zip code %s-%s)",
                row, country.isocode, zip_code)
            return

        kw = dict(
            zip_code=zip_code,
            name=name,
            country=country,
        )
        return Place(**kw)

    def load_par(self, row):
        kw = {}
        # kw.update(
        #     street2kw(join_words(
        #         row['RUE'],
        #         row['RUENUM'],
        #         row['RUEBTE'])))

        self.store(kw, id=self.par_pk(row.idpar))

        email = row.email.strip()
        if email and is_valid_email(email):
            self.store(kw, email=email)

        self.store(kw, prefix=row.allo)
        self.store(kw, created=row.get('datcrea', None))

        cl = self.par_class(row)
        if cl is Company:
            cl = Company
            self.store(
                kw,
                vat_id=row['notva'].strip(),
                prefix=row['allo'].strip(),
                name=row.firme,
            )
        elif cl is Person:
            # kw.update(**name2kw(self.decode_string(row.firme)))
            self.store(
                kw,
                first_name=row['vorname'].strip(),
                last_name=row.firme,
                # birth_date=row['gebdat'],
                title=row['allo'].strip(),
            )
            sex = row.get('sex', None)
            self.store(
                kw, gender=convert_gender(sex))
        elif cl is Household:
            self.store(
                kw,
                name=row.firme.strip() + ' ' + row.vorname.strip(),
            )
        elif cl is List:
            self.store(
                kw,
                name=row.firme,
            )
        else:
            dblogger.warning(
                "Ignored PAR record %s (IdPrt %r)" % (
                    row.idpar, row.idprt))
            return
        if cl is not List:
            language = isolang(row['langue'])
            self.store(
                kw,
                language=language,
                remarks=dbfmemo(row.get('memo', '')),
            )

            isocode = self.short2iso(row.pays.strip())
            if isocode:
                try:
                    country = Country.objects.get(
                        isocode=isocode)
                except Country.DoesNotExist:
                    country = Country(isocode=isocode,
                                      name=isocode)
                    country.save()
                kw.update(country=country)

            zip_code = row['cp'].strip()
            if zip_code:
                kw.update(zip_code=zip_code)
                try:
                    city = Place.objects.get(
                        country=country,
                        zip_code__exact=zip_code,
                    )
                    kw.update(city=city)
                except Place.DoesNotExist as e:
                    city = Place(zip_code=zip_code,
                                 name=zip_code,
                                 country=country)
                    city.save()
                    kw.update(city=city)
                    # dblogger.warning("%s-%s : %s",row['PAYS'],row['CP'],e)
                except Place.MultipleObjectsReturned as e:
                    dblogger.warning("%s-%s : %s",
                                     row['pays'],
                                     row['cp'],
                                     e)
            self.store(
                kw,
                phone=row['tel'].strip(),
                fax=row['fax'].strip(),
                street=row['rue'].strip(),
                street_no=row['ruenum'],
                street_box=row['ruebte'].strip(),
            )

            # kw.update(street2kw(join_words(row['RUE'],
            # row['RUENUM'],row['RUEBTE'])))

        try:
            obj = cl(**kw)
        except Exception as e:
            dblogger.warning("Failed to instantiate %s from %s",
                             cl, kw)
            raise
        yield obj

        def compte2iban(s, **kw):
            a = s.split(':')
            if len(a) == 1:
                kw.update(iban=s)
            elif len(a) == 2:
                kw.update(bic=a[0])
                kw.update(iban=a[1])
            else:
                kw.update(iban=s)
            return kw
        
        compte1 = row['compte1'].strip()
        if compte1:
            obj.full_clean()
            obj.save()
            kw = compte2iban(compte1, partner=obj, primary=True)
            if kw['iban']:
                obj = sepa.Account(**kw)
                try:
                    obj.full_clean()
                    yield obj
                except ValidationError:
                    dblogger.warning(
                        "Ignored invalid PAR->Compte1 %r", compte1)

    def load_prj(self, row, **kw):
        pk = int(row.idprj.strip())
        kw.update(id=pk)
        if row.parent.strip():
            kw.update(parent_id=int(row.parent))
        kw.update(name=row.name1.strip())
        # if row.idpar.strip():
        #     kw.update(partner_id=self.par_pk(row.idpar.strip()))

        kw.update(ref=row.seq.strip())
        # kw.update(user=self.get_user(None))
        desc = dbfmemo(row.abstract).strip() + '\n\n' + dbfmemo(row.body)
        # kw.update(summary=dbfmemo(row.abstract))
        kw.update(description=desc)
        return tickets.Project(**kw)

    def load_pin(self, row, **kw):
        pk = int(row.idpin)
        kw.update(id=pk)
        if row.idprj.strip():
            kw.update(project_id=int(row.idprj))
            # kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        kw.update(summary=row.short.strip())
        kw.update(description=dbfmemo(row.memo))
        kw.update(state=ticket_state(row.idpns))
        kw.update(closed=row.closed)
        kw.update(created=row['date'])
        kw.update(modified=datetime.datetime.now())
        kw.update(reporter=self.get_user(row.idusr))
        return tickets.Ticket(**kw)
        # if row.idpar.strip():
        #     kw = dict(project=obj)
        #     kw.update(partner_id=self.par_pk(row.idpar))
        #     yield tickets.Sponsorship(**kw)

    def load_dls(self, row, **kw):
        if not row.iddls.strip():
            return
        if not row.idpin.strip():
            return
        try:
            ticket = tickets.Ticket.objects.get(pk=int(row.idpin))
        except tickets.Ticket.DoesNotExist:
            return
        pk = int(row.iddls)
        kw.update(id=pk)
        kw.update(ticket=ticket)
        # if row.idprj.strip():
        #     kw.update(project_id=int(row.idprj))
            # kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        # if row.idpar.strip():
        #     kw.update(partner_id=self.par_pk(row.idpar))
        kw.update(summary=row.nb.strip())
        kw.update(start_date=row.date)
        kw.update(user=self.get_user(row.idusr))

        def set_time(kw, fldname, v):
            v = v.strip()
            if not v:
                return
            if v == '24:00':
                v = '0:00'
            kw[fldname] = v

        set_time(kw, 'start_time', row.von)
        set_time(kw, 'end_time', row.bis)
        set_time(kw, 'break_time', row.pause)
        # kw.update(start_time=row.von.strip())
        # kw.update(end_time=row.bis.strip())
        # kw.update(break_time=row.pause.strip())
        # kw.update(is_private=tim2bool(row.isprivat))
        obj = clocking.Session(**kw)
        # if row.idpar.strip():
            # partner_id = self.par_pk(row.idpar)
            # if obj.project and obj.project.partner \
                # and obj.project.partner.id == partner_id:
                # pass
            # elif obj.ticket and obj.ticket.partner \
                # and obj.ticket.partner.id == partner_id:
                # pass
            # else:
                # ~ dblogger.warning("Lost DLS->IdPar of DLS#%d" % pk)
        yield obj
        if row.memo.strip():
            kw = dict(owner=obj)
            kw.update(body=dbfmemo(row.memo))
            kw.update(user=obj.user)
            kw.update(date=obj.start_date)
            yield rt.modules.notes.Note(**kw)

    def load_art(self, row, **kw):
        # try:
        #     pk = int(row.idart)
        # except ValueError as e:
        #     dblogger.warning("Ignored %s: %s", row, e)
        #     # return
        idart = row.idart.strip()
        if not idart:
            dblogger.warning("Ignored %s: ART->IdArt is empty", row)
            return
        kw.update(ref=idart)
        # if pk == 0:
        #     pk = 1000  # mysql doesn't accept value 0
        # kw.update(id=pk)
        self.babel2kw('name', 'name', row, kw)
        # dblogger.info("20140823 product %s", kw)
        kw.setdefault('name', idart)
        return products.Product(**kw)

    def decode_string(self, v):
        return v
        # return v.decode(self.codepage)

    def babel2kw(self, tim_fld, lino_fld, row, kw):
        if dd.plugins.tim2lino.use_dbf_py:
            import dbf
            ex = dbf.FieldMissingError
        else:
            ex = Exception
        for i, lng in enumerate(self.languages):
            try:
                v = getattr(row, tim_fld + str(i + 1), '').strip()
                if v:
                    v = self.decode_string(v)
                    kw[lino_fld + lng.suffix] = v
                    if lino_fld not in kw:
                        kw[lino_fld] = v
            except ex as e:
                pass
                dblogger.info("Ignoring %s", e)

    def after_load(self, tableName):
        for tableName2, func in dd.plugins.tim2lino.load_listeners:
            if tableName2 == tableName:
                func(self)

    def after_gen_load(self):
        sc = dict()
        for k, v in dd.plugins.tim2lino.siteconfig_accounts.items():
            sc[k] = self.CHART.get_account_by_ref(v)
        settings.SITE.site_config.update(**sc)
        # func = dd.plugins.tim2lino.setup_tim2lino
        # if func:
        #     func(self)

    def objects(tim):

        self = tim

        self.ROOT = users.User(username='luc', profile='900')
        self.ROOT.set_password("1234")
        yield self.ROOT

        # settings.SITE.loading_from_dump = True

        self.CHART = accounts.AccountCharts.default
        yield self.CHART

        if False:
            self.DIM = sales.InvoicingMode(name='Default')
            yield self.DIM

        # yield sales.Invoice.create_journal('sales',
        #    chart=self.CHART,name="Verkaufsrechnungen",ref="VKR")
        # yield ledger.AccountInvoice.create_journal('purchases',
        #    chart=self.CHART,name="Einkaufsrechnungen",ref="EKR")
        # from lino.modlib.users import models as users
        # ROOT = users.User.objects.get(username='root')
        # DIM = sales.InvoicingMode.objects.get(name='Default')
        yield tim.load_dbf('GEN', self.load_gen2group)
        yield tim.load_dbf('GEN', self.load_gen2account)

        yield dpy.FlushDeferredObjects

        self.after_gen_load()

        yield tim.load_dbf('ART')
        yield tim.load_dbf('JNL')

        yield dpy.FlushDeferredObjects

        # yield tim.load_dbf('NAT')
        yield tim.load_dbf('PLZ')
        yield tim.load_dbf('PAR')

        # from lino_cosi.lib.vat.fixtures import euvatrates
        # yield euvatrates.objects()

        settings.SITE.loading_from_dump = True
        yield tim.load_dbf('PRJ')
        yield dpy.FlushDeferredObjects
        settings.SITE.loading_from_dump = False

        """
        We need a FlushDeferredObjects here because most Project
        objects don't get saved at the first attempt
        """

        if GET_THEM_ALL:

            yield tim.load_dbf('VEN')
            yield tim.load_dbf('VNL')

            yield tim.load_dbf('FIN')
            yield tim.load_dbf('FNL')

            ses = rt.login(self.ROOT.username)

            dblogger.info("Register %d vouchers", len(self.must_register))
            failures = 0
            for doc in progress.bar(self.must_register):
                # puts("Registering {0}".format(doc))
                try:
                    doc.register(ses)
                except Exception as e:
                    dblogger.warning("Failed to register %s : %s ", doc, e)
                    failures += 1
                    if failures > 100:
                        dblogger.warning("Abandoned after 100 failures.")
                        break

            # Given a string `ms` of type 'VKR940095', locate the corresponding
            # movement.
            dblogger.info("Resolving %d matches", len(self.must_match))
            for (voucher, matching, ms) in self.must_match:
                if matching.pk is None:
                    dblogger.warning("Ignored match %s in %s (pk is None)" % (
                        ms, matching))
                    continue
                idjnl, iddoc = ms[:3], ms[3:]
                try:
                    year, num = year_num(iddoc)
                except ValueError as e:
                    dblogger.warning("Ignored match %s in %s (%s)" % (
                        ms, matching, e))
                try:
                    jnl = Journal.objects.get(ref=idjnl)
                except Journal.DoesNotExist:
                    dblogger.warning("Ignored match %s in %s (invalid JNL)" % (
                        ms, matching))
                    continue
                qs = Movement.objects.filter(
                    voucher__journal=jnl, voucher__number=num,
                    voucher__year=year, partner__isnull=False)
                if qs.count() == 0:
                    dblogger.warning("Ignored match %s in %s (no movement)" % (
                        ms, matching))
                    continue
                matching.match = qs[0]
                matching.save()
                voucher.deregister(ses)
                voucher.register(ses)
                

def objects():
    # settings.SITE.startup()
    tim = TimLoader(settings.SITE.legacy_data_path)
    for obj in tim.objects():
        yield obj
