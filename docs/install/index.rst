.. _cosi.install:

====================
Installing Lino Così
====================

Install the project code
------------------------

- Install Lino (the framework) as documented in
  :ref:`lino.dev.install`

- Go to your :xfile:`repositories` directory and download also a copy
  of the *Lino Cosi* repository::

    $ cd ~/repositories
    $ git clone https://github.com/lsaffre/lino-cosi cosi
    
- Use pip to install this as editable package::

    $ pip install -e cosi

- Check whether everything worked well::

    $ cd ~/repositories/cosi
    $ inv initdb
    $ inv test


Create a local project
----------------------

- Create a local Lino project as explained in :ref:`lino.tutorial.hello`.

- Change your project's :xfile:`settings.py` file so that it looks as
  follows:

  .. literalinclude:: settings.py

  The first line is the Python way to specify your source file's
  encoding (:pep:`263`).  We need to specify this because of the
  non-ascii **ì** of "Lino Così" in line 3.


Run directly from repository
----------------------------

- You can avoid creating a local project and use directly one of the
  demo databases that come with Lino Così.  Basically you just do::

    $ cd ~/repositories/cosi
    $ cd lino_cosi/projects/apc
    $ python manage.py runserver
    
  Instead of ``std`` in the second line, you can choose "apc",
  "pierre" or "ylle". 
  :mod:`lino_cosi.projects`
    
- And to be honest, the above trick will probably work only if you
  have set up your :ref:`lino.djangosite_local`.

  
