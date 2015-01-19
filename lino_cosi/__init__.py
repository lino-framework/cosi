# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)
"""
.. autosummary::
   :toctree:

    models
    projects
    migrate

"""

import os

execfile(os.path.join(os.path.dirname(__file__), 'setup_info.py'))
__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://cosi.lino-framework.org")
srcref_url = 'https://github.com/lsaffre/lino-cosi/blob/master/%s'
