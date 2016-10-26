# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
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

Import legacy data from TIM (including households, ...).
An extension of :mod:`tim2lino <lino_cosi.lib.tim2lino.fitxtures.tim2lino>`.


"""
from __future__ import unicode_literals
import datetime


from lino.utils import mti
from lino.api import dd, rt

from .timloader1 import TimLoader

Person = dd.resolve_model("contacts.Person")
Company = dd.resolve_model("contacts.Company")
RoleType = dd.resolve_model("contacts.RoleType")
Role = dd.resolve_model("contacts.Role")
Household = dd.resolve_model('households.Household')
Product = dd.resolve_model('products.Product')
List = dd.resolve_model('lists.List')
Member = dd.resolve_model('lists.Member')
households_Member = dd.resolve_model('households.Member')
Account = dd.resolve_model('accounts.Account')

clocking = dd.resolve_app('clocking')

User = rt.models.users.User
UserTypes = rt.models.users.UserTypes
Partner = rt.models.contacts.Partner


def create(model, **kwargs):
    obj = model(**kwargs)
    obj.full_clean()
    obj.save()
    return obj

class TimLoader(TimLoader):

    # archived_tables = set('GEN ART VEN VNL JNL FIN FNL'.split())
    # archive_name = 'rumma'
    # has_projects = False
    # languages = 'de fr'
    
    def par_pk(self, pk):
        if pk.startswith('E'):
            return 1000000 + int(pk[1:])
        elif pk.startswith('S'):
            return 2000000 + int(pk[1:])
        try:
            return int(pk)
        except ValueError:
            return None

    def par_class(self, data):
        prt = data.idprt
        if prt == 'L':  # Lieferant
            return Company
        elif prt == 'K':  # Krankenkasse
            return Company
        elif prt == 'S':  # Sonstige
            return Company
        elif prt == 'W':  # Netzwerkpartner
            return Company
        elif prt == 'R':  # Ärzte
            return Person
        elif prt == 'Z':  # Zahler
            return Company
        elif prt == 'P':  # Personen
            return Person
        elif prt == 'G':  # Lebensgruppen
            return Household
        elif prt == 'T':  # Therapeutische Gruppen
            return List
        #~ dblogger.warning("Unhandled PAR->IdPrt %r",prt)

    def load_par(self, row):
        for obj in super(TimLoader, self).load_par(row):
            if row.idpar.startswith('E'):
                obj.team = self.eupen
            elif row.idpar.startswith('S'):
                obj.team = self.stvith
            # if isinstance(obj, Partner):
            #     obj.isikukood = row['regkood'].strip()
            #     obj.created = row['datcrea']
            #     obj.modified = datetime.datetime.now()
            yield obj

    # def load_pls(self, row, **kw):
    #     kw.update(ref=row.idpls.strip())
    #     kw.update(name=row.name)
    #     return List(**kw)

    def get_user(self, idusr=None):
        try:
            return User.objects.get(username=idusr)
        except User.DoesNotExist:
            return None

    def load_usr(self, row, **kw):
        kw.update(username=row.userid.strip())
        kw.update(first_name=row.name.strip())
        abtlg = row.abtlg.strip()
        if abtlg == 'E':
            kw.update(team=self.eupen)
        elif abtlg == 'S':
            kw.update(team=self.stvith)
        kw.update(profile=UserTypes.admin)
        return User(**kw)

    def load_mbr(self, row, **kw):

        p1 = self.get_customer(row.idpar)
        if p1 is None:
            dd.logger.debug(
                "Failed to load MBR %s : "
                "No idpar", row)
            return
        p2 = self.get_customer(row.idpar2)

        if p2 is not None:
            contact_role = self.contact_roles.get(row.idpls.strip())
            if contact_role is not None:
                kw = dict()
                p = mti.get_child(p1, Company)
                if p is None:
                    dd.logger.debug(
                        "Failed to load MBR %s : "
                        "idpar is not a company", row)
                    return
                kw.update(company=p)
                p = mti.get_child(p2, Person)
                if p is None:
                    dd.logger.debug(
                        "Failed to load MBR %s : "
                        "idpar2 is not a person", row)
                    return
                kw.update(person=p)
                kw.update(type=contact_role)
                return Role(**kw)

            role = self.household_roles.get(row.idpls.strip())
            if role is not None:
                household = mti.get_child(p1, Household)
                if household is None:
                    dd.logger.debug(
                        "Failed to load MBR %s : "
                        "idpar is not a household", row)
                    return
                person = mti.get_child(p2, Person)
                if person is None:
                    dd.logger.debug(
                        "Failed to load MBR %s : idpar2 is not a person", row)
                    return
                return households_Member(
                    household=household,
                    person=person,
                    role=role)
            dd.logger.debug(
                "Failed to load MBR %s : idpar2 is not empty", row)
            return

        try:
            lst = List.objects.get(ref=row.idpls.strip())
        except List.DoesNotExist:
            dd.logger.debug(
                "Failed to load MBR %s : unknown idpls", row)
            return
        kw.update(list=lst)
        kw.update(remark=row.remarq)
        kw.update(partner=p1)
        return Member(**kw)

    def load_dls(self, row, **kw):
        if not row.iddls.strip():
            return
        # if not row.idpin.strip():
        #     return
        pk = row.iddls.strip()
        idusr = row.idusr.strip()
        if pk.startswith('E'):
            team = self.eupen
            pk = int(pk[1:])
        elif pk.startswith('S'):
            team = self.stvith
            pk = int(pk[1:]) + 1000000
        u = self.get_user(idusr)
        if u is None:
            dd.logger.warning(
                "Cannot import session %s because there is no user %s",
                pk, idusr)
            return
        
        if u.team != team:
            u1 = u
            idusr += '@' + str(team.pk)
            try:
                u = User.objects.get(username=idusr)
            except User.DoesNotExist:
                u = create(
                    User, username=idusr, first_name=u1.first_name, team=team,
                    profile=u1.profile)
            
        kw.update(user=u)
        kw.update(id=pk)
        # if row.idprj.strip():
        #     kw.update(project_id=int(row.idprj))
            # kw.update(partner_id=PRJPAR.get(int(row.idprj),None))
        if row.idpar.strip():
            idpar = self.par_pk(row.idpar.strip())
            try:
                ticket = Partner.objects.get(id=idpar)
                kw.update(ticket=ticket)
            except Partner.DoesNotExist:
                dd.logger.warning(
                    "Cannot import session %s because there is no partner %d",
                    pk, idpar)
                return
                
        kw.update(summary=row.nb.strip())
        kw.update(start_date=row.date)

        def set_time(kw, fldname, v):
            v = v.strip()
            if not v:
                return
            if v == '24:00':
                v = '0:00'
            kw[fldname] = v

        set_time(kw, 'start_time', row.von)
        set_time(kw, 'end_time', row.bis)
        # set_time(kw, 'break_time', row.pause)
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
        # if row.memo.strip():
        #     kw = dict(owner=obj)
        #     kw.update(body=self.dbfmemo(row.memo))
        #     kw.update(user=obj.user)
        #     kw.update(date=obj.start_date)
        #     yield rt.modules.notes.Note(**kw)

    def objects(self):

        Team = rt.modules.teams.Team
        self.eupen = create(Team, name="Eupen")
        yield self.eupen
        self.stvith = create(Team, name="St. Vith")
        yield self.stvith
        
        yield self.load_dbf('USR')
        
        MemberRoles = rt.modules.households.MemberRoles

        self.household_roles = {
            'VATER': MemberRoles.head,
            'MUTTER': MemberRoles.spouse,
            'KIND': MemberRoles.child,
            'K': MemberRoles.child,
        }

        self.contact_roles = cr = {}
        cr.update(DIR=RoleType.objects.get(pk=2))
        cr.update(A=RoleType.objects.get(pk=3))
        cr.update(SYSADM=RoleType.objects.get(pk=4))

        obj = RoleType(name="TIM user")
        yield obj
        cr.update(TIM=obj)
        obj = RoleType(name="Lino user")
        yield obj
        cr.update(LINO=obj)
        obj = RoleType(name="Board member")
        yield obj
        cr.update(VMKN=obj)
        obj = RoleType(name="Member")
        yield obj
        cr.update(M=obj)

        # self.PROD_617010 = Product(
        #     name="Edasimüük remondikulud",
        #     id=40)
        # yield self.PROD_617010

        # self.sales_gen2art['617010'] = self.PROD_617010

        yield super(TimLoader, self).objects()

        # yield self.load_dbf('PLS')
        # yield self.load_dbf('MBR')

        # if False:  # and GET_THEM_ALL:
        #     yield self.load_dbf('PIN')
        yield self.load_dbf('DLS')

