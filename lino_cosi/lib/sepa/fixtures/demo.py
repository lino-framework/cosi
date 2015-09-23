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
Adds some commonly known partners and their bank accounts.

These are real data randomly collected from Internet.

"""

from __future__ import unicode_literals
import glob
import os
import time

from lino.utils.instantiator import Instantiator
from lino.api import rt
from lino_cosi.lib.sepa.camt import CamtParser
from lino_cosi.lib.sepa.models import Movement, Statement

Company = Instantiator('contacts.Company', 'name url').build
Account = Instantiator('sepa.Account', 'partner bic iban remark').build


class Adder(object):
    def __init__(self):
        self.current_partner = None
        self.primary = False
        # make the first account of every company primary

    def add_company(self, name, url, **kw):
        obj = Company(name=name, url=url, **kw)
        self.current_partner = obj
        self.primary = True
        return obj

    def add_account(self, bic, iban, remark=''):
        iban = iban.replace(' ', '')
        acc = Account(
            self.current_partner, bic, iban, remark, primary=self.primary)
        self.primary = False
        return acc


def objects():
    adder = Adder()
    C = adder.add_company
    A = adder.add_account

    yield C('AS Express Post', 'http://www.expresspost.ee/',
            country="EE")
    yield A('HABAEE2X', 'EE872200221012067904')

    yield C('AS Matsalu Veevärk', 'http://www.matsaluvv.ee',
            country="EE")
    yield A('HABAEE2X', 'EE732200221045112758')

    yield C('Eesti Energia AS', "http://www.energia.ee",
            country="EE")
    yield A('HABAEE2X', 'EE232200001180005555', "Eraklilendile")
    yield A('HABAEE2X', 'EE322200221112223334', "Ärikliendile")
    yield A('EEUHEE2X', 'EE081010002059413005')
    yield A('FOREEE2X', 'EE70 3300 3320 9900 0006')
    yield A('NDEAEE2X', 'EE43 17000 1700 0115 797')

    yield C('IIZI kindlustusmaakler AS', "http://www.iizi.ee",
            country="EE")
    yield A('HABAEE2X', 'EE382200221013987931')

    yield C('Maksu- ja tolliamet', "http://www.emta.ee",
            country="EE")
    yield A('HABAEE2X', 'EE522200221013264447')

    tallinn = rt.modules.countries.Place.objects.get(name="Tallinn")
    yield C('Ragn-Sells AS', "http://www.ragnsells.ee", country="EE",
            street="Suur-Sõjamäe", street_no=50, street_box="a",
            zip_code="11415",
            city=tallinn)
    yield A('HABAEE2X', 'EE202200221001178338')
    yield A('', 'EE781010220002715011 ')
    yield A('', 'EE321700017000231134')

    yield C('Electrabel Customer Solutions',
            "https://www.electrabel.be",
            country="BE",
            zip_code="1000",
            # city="Bruxelles",
            vat_id='BE 0476 306 127',
            street="Boulevard Simón Bolívar",
            street_no=34)
    # 1000 Bruxelles
    yield A('BPOTBEB1', 'BE46 0003 2544 8336')
    yield A('BPOTBEB1', 'BE81 0003 2587 3924')

    yield C('Ethias s.a.', "http://www.ethias.be",
            vat_id="BE 0404.484.654",
            street="Rue des Croisiers",
            street_no=24,
            country="BE",
            zip_code="4000")
    yield A('ETHIBEBB', 'BE79827081803833')

    yield C("Niederau Eupen AG", "http://www.niederau.be",
            vat_id="BE 0419.897.855",
            street="Herbesthaler Straße",
            street_no=134,
            country="BE",
            zip_code="4700")
    yield A('BBRUBEBB', 'BE98 3480 3103 3293')

    yield C("Leffin Electronics", "",
            email="info@leffin-electronics.be",
            vat_id="BE0650.238.114",
            street="Schilsweg",
            street_no=80,
            country="BE",
            zip_code="4700")
    yield A('GEBABEBB', 'BE38 2480 1735 7572')

    wc = os.path.join(os.path.dirname(__file__), 'data', 'COD_20150907_O25MMF107I.xml')
    filename = glob.glob(wc)[0]
    Account = rt.modules.sepa.Account
    Partner = rt.modules.contacts.Partner
    parser = CamtParser()
    data_file = open(filename, 'rb').read()
    try:
        res = parser.parse(data_file)
        if res is not None:
            for _statement in res:
                if _statement.get('account_number', None) is not None:
                    # TODO : How to query an account by iban field ?
                    account = Account.objects.get(id=1)
                    if account:
                        s = Statement(account=account,
                                      date=_statement['date'].strftime("%Y-%m-%d"),
                                      date_done=time.strftime("%Y-%m-%d"),
                                      statement_number=_statement['name'],
                                      balance_end=_statement['balance_end'],
                                      balance_start=_statement['balance_start'],
                                      balance_end_real=_statement['balance_end_real'],
                                      currency_code=_statement['currency_code'])
                        yield s
                        for _movement in _statement['transactions']:
                            partner = None
                            if _movement.get('partner_name', None) is not None:
                                if Partner.objects.filter(name=_movement['partner_name']).exists():
                                    partner = Partner.objects.get(name=_movement['partner_name'])
                                else:
                                    partner = Partner.objects.order_by('name')[0]
                            # TODO :check if the movement is already imported.
                            if not Movement.objects.filter(unique_import_id=_movement['unique_import_id']).exists():
                                yield Movement(statement=s,
                                               unique_import_id=_movement['unique_import_id'],
                                               movement_date=_movement['date'],
                                               amount=_movement['amount'],
                                               partner=partner,
                                               partner_name=_movement['partner_name'],
                                               ref=_movement.get('ref', '') or ' ',
                                               bank_account=account)
    except ValueError:
        print("Import Error")
