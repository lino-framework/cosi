# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
.. autosummary::
   :toctree:

    lib
    migrate

"""

import os

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(
    docs="http://cosi.lino-framework.org",
    dedocs="http://de.cosi.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/cosi/blob/master/%s'
doc_trees = ['docs', 'dedocs']
