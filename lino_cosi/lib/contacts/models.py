# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from lino.api import _
from lino_xl.lib.contacts.models import *


class PartnerDetail(PartnerDetail):
    
    main = "general ledger sepa.AccountsByPartner"

    general = dd.Panel("""
    address_box:60 contact_box:30 overview
    bottom_box
    """, label=_("General"))

    ledger = dd.Panel("""
    payment_term purchase_account
    vat.VouchersByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)
    
    address_box = dd.Panel("""
    name_box
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """, label=_("Address"))

    contact_box = dd.Panel("""
    info_box
    email:40
    url
    phone
    gsm fax
    """, label=_("Contact"))

    bottom_box = """
    remarks
    """

    name_box = "name"
    info_box = "id language"


class PersonDetail(PartnerDetail, PersonDetail):
    
    name_box = "last_name first_name:15 gender title:10"
    info_box = "id:5 language:10"
    bottom_box = "remarks contacts.RolesByPerson"


class CompanyDetail(PartnerDetail, CompanyDetail):
    bottom_box = """
    remarks contacts.RolesByCompany
    """

    name_box = "prefix:10 name type:30"
    

