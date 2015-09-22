# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
.. autosummary::
   :toctree:

    lib
    projects
    migrate

"""

import os

fn = os.path.join(os.path.dirname(__file__), 'setup_info.py')
execfile(fn)
__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://cosi.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-cosi/blob/master/%s'
