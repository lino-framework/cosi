# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
.. autosummary::
   :toctree:

    lib
    migrate

"""

import os

fn = os.path.join(os.path.dirname(__file__), 'setup_info.py')
exec(compile(open(fn, "rb").read(), fn, 'exec'))
__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://cosi.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/cosi/blob/master/%s'
doc_trees = ['docs']
