# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)


"""Adds models and tables for importing BankToCustomer SEPA statements
from a bank. This module was developed for Belgian banks.

Excerpts of the Febelfin Implementation guidelines `XML message for
statement.
<https://www.febelfin.be/sites/default/files/files/Standard-XML-Statement-v1-en_0.pdf>`_
(version 1.0):

  This document contains the Belgian guidelines for the application of
  the Belgian subset of the MX.CAMT.053 B2C Statement.

  This message is sent by the bank to an account holder or a third
  person mandated by him.  It is used for informing the account holder
  or the third person mandated of the account balance s and account
  transactions

  The principle has been adopted for double encoding, i.e. encoding
  proper to ISO Bank Transaction Code list (§ 5.2 – Double encoding)
  together with ‘proprietary’ Febelfin encoding.

  Each item of the BankToCustomer Cash Management Standards message is
  referring to the corresponding index of the item in the (ISO 20022)
  Message Definition Report for Bank-to-Customer Cash Management. This
  Report can be found on www.iso20022.org, under “Catalogue of UNIFI
  messages”, with “camt.053.001.02” as reference for the EoD
  reporting.

  Any gaps in the index numbering are due to the fact that some
  message elements of the MX.CAMT.053.001.02 message are not supported
  in the Belgian subset



.. autosummary::
   :toctree:

    models
    ui
    camt
    febelfin
    fixtures.demo


"""

from __future__ import unicode_literals

from lino.api import ad, _


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."
    verbose_name = _("SEPA import")

    needs_plugins = ['lino_cosi.lib.cosi']
    
    import_statements_path = None
    """A path wildcard pointing to xml files which need to get imported.

    As a system admin you can set this e.g. by specifying in your
    :xfile:`settings.py` (*before* instantiating your
    :setting:`SITE`)::

       ad.configure_plugin('b2c', import_statements_path="/var/sepa_incoming")

    End-users are supposed to download SEPA statement files to that
    directory and then to invoke the
    :class:`lino_cosi.lib.b2c.models.ImportStatements` action.

    """

    delete_imported_xml_files = False
    """This attribute define whether, Cosi have to delete the SEPA file
    after it get imported.

    """

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.accounts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('system.SiteConfig', 'import_b2c')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.sepa
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('b2c.Accounts')
        m.add_action('b2c.Statements')
        m.add_action('b2c.Transactions')
