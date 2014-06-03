.. _cosi.install:

Installing Lino Così
====================

- Install Lino (the framework) as documented in
  :ref:`lino.dev.install`

- Go to your `repositories` directory and 
  download also a copy of the Lino Cosi repository::

    cd ~/repositories
    git clone https://github.com/lsaffre/lino-cosi cosi
    
- Use pip to install this as editable package::

    pip install -e cosi

- Your project's :file:`settings.py` file should look as follows:

  .. literalinclude:: settings.py

  The first line is Python way to specify  encoding
  (:pep:`263`).
  That's needed because of the non-ascii **ì** of "Lino Così" 
  in line 3.

- Your project's :xfile:`manage.py` file should look as follows:

  .. literalinclude:: manage.py

