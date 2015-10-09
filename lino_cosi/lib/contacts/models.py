# Copyright 2013-2015 Luc Saffre
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


from lino.api import _
from lino.modlib.contacts.models import *

from lino_cosi.lib.vat.mixins import PartnerDetailMixin


class PartnerDetail(PartnerDetail, PartnerDetailMixin):
    
    main = "general ledger"

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
    

@dd.receiver(dd.post_analyze)
def my_details(sender, **kw):
    contacts = sender.modules.contacts
    contacts.Partners.set_detail_layout(PartnerDetail())
    contacts.Companies.set_detail_layout(CompanyDetail())
    contacts.Persons.set_detail_layout(PersonDetail())


