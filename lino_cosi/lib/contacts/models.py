# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from lino.api import _, rt
from lino_xl.lib.accounts.utils import DEBIT
from lino_xl.lib.contacts.models import *

from lino_xl.lib.vat.mixins import PartnerDetailMixin

class Partner(Partner):
    """An version of :class:`lino_xl.lib.contacts.models.Partner` which
    adds accounting fucntionality.

    """
    class Meta(Partner.Meta):
        abstract = dd.is_abstract_model(__name__, 'Partner')

    @dd.virtualfield(dd.PriceField(_("Debit balance")))
    def debit_balance(self, ar):
        Movement = rt.models.ledger.Movement
        qs = Movement.objects.filter(partner=self, cleared=False)
        return Movement.get_balance(DEBIT, qs)


class Person(Person, Partner):
    """An version of :class:`lino_xl.lib.contacts.models.Person` which
    adds accounting functionality.

    """
    class Meta(Person.Meta):
        abstract = dd.is_abstract_model(__name__, 'Person')


class Company(Company, Partner):
    """An version of :class:`lino_xl.lib.contacts.models.Company` which
    adds accounting functionality.

    """
    class Meta(Company.Meta):
        abstract = dd.is_abstract_model(__name__, 'Company')


# class PartnerDetail(PartnerDetail):
class PartnerDetail(PartnerDetail, PartnerDetailMixin):
    
    main = "general ledger sepa.AccountsByPartner"

    general = dd.Panel("""
    address_box:60 contact_box:30 overview
    bottom_box
    """, label=_("General"))

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
    

# Partners.detail_layout = PartnerDetail()
# Companies.detail_layout = CompanyDetail()
# Persons.detail_layout = PersonDetail()

Partners.set_detail_layout(PartnerDetail())
Companies.set_detail_layout(CompanyDetail())
Persons.set_detail_layout(PersonDetail())


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.modules.contacts
#     contacts.Partners.set_detail_layout(contacts.PartnerDetail())
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())
#     contacts.Persons.set_detail_layout(contacts.PersonDetail())


