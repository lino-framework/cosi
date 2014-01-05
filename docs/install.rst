.. _cosi.install:

Installing Lino-Cosi
=======================

Development server
------------------

If you need only a development server, 
just install Lino (the framework) as documented 
in :ref:`lino.dev.install`, then:

- Go to your `hgwork` directory and 
  download also a copy of the Lino-Cosi repository::

    cd ~/hgwork
    git clone https://github.com/lsaffre/lino-cosi
    
- Use pip to install this as editable package::

    pip install -e cosi

- In your project's `settings.py`, make sure that you inherit from 
  the right `settings` module::
    
    from lino_cosi.settings import *


