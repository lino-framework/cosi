.. _cosi.install:

Installing Lino Così
====================

- Install Lino (the framework) as documented in
  :ref:`lino.dev.install`

- Go to your :xfile:`repositories` directory and download also a copy
  of the *Lino Cosi* repository::

    $ cd ~/repositories
    $ git clone https://github.com/lsaffre/lino-cosi cosi
    
- Use pip to install this as editable package::

    $ pip install -e cosi

- Run a recommended check to see whether everything worked well::

    $ pip install commondata commondata.ee commondata.be
    $ cd ~/repositories/cosi
    $ fab initdb
    $ fab test

- Create a local Lino project as explained in :ref:`lino.tutorial.hello`.

- Change your project's :xfile:`settings.py` file so that it looks as
  follows:

  .. literalinclude:: settings.py

  The first line is the Python way to specify your source file's
  encoding (:pep:`263`).  We need to specify this because of the
  non-ascii **ì** of "Lino Così" in line 3.

