# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino Cosi extension of :mod:`lino_xl.lib.contacts`

.. autosummary::
   :toctree:

    models
    fixtures.std
    fixtures.demo

"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):

    # extends_models = ['Partner', 'Person', 'Company']
    needs_plugins = ['lino_cosi.lib.cosi']
    
