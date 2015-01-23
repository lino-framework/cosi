.. _cosi.tested.bel_de:

Refusing permission to an anonymous request
===========================================

.. include:: /include/tested.rst

.. to test only this document:

  $ python setup.py test -s tests.DocsTests.test_bel_de

This document reproduces a unicode error which occurred when Lino
tried to say "As Anonymous you have no permission to run this action."
in German (where the internationlized text (u'Als Anonym haben Sie
nicht die Berechtigung, diese Aktion auszuf\xfchren.') contains
non-ascii characters.

The error was::

  UnicodeEncodeError at /api/sales/InvoicesByJournal
  'ascii' codec can't encode character u'\xfc' in position 64: ordinal not in range(128)

We cannot use the `doctests` settings because the situation happens
only with session-based authentication.


.. 

    >>> from __future__ import print_function
    >>> from __future__ import unicode_literals
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.projects.apc.settings.sestests'
    >>> import json
    >>> from bs4 import BeautifulSoup
    >>> from __future__ import print_function 
    >>> from __future__ import unicode_literals
    >>> from lino.runtime import *
    >>> from django.test.client import Client
    >>> from django.utils import translation


This document uses :mod:`lino_cosi.projects.apc`:

>>> print(settings.SETTINGS_MODULE)
lino_cosi.projects.apc.settings.sestests

>>> print(settings.SITE.default_user)
None
>>> print(settings.SITE.user_model)
<class 'lino.modlib.users.models.User'>
>>> print(settings.SITE.remote_user_header)
None
>>> print(settings.SITE.get_auth_method())
session
>>> print('\n'.join(settings.MIDDLEWARE_CLASSES))
django.middleware.common.CommonMiddleware
django.middleware.locale.LocaleMiddleware
django.contrib.sessions.middleware.SessionMiddleware
lino.core.auth.SessionUserMiddleware
lino.utils.ajax.AjaxExceptionResponse
>>> 'django.contrib.sessions' in settings.INSTALLED_APPS
True

Some client logs in and gets some data:

>>> client = Client()
>>> res = client.post('/auth', data=dict(username="rolf", password="1234"))
>>> res.status_code
200
>>> r = json.loads(res.content)
>>> print(r['message'])
Now logged in as u'rolf'
>>> r['success']
True

The user uses the main menu to open sales.InvoicesByJournal, which
will do the following AJAX call to get its data:

>>> url = '/api/sales/InvoicesByJournal'
>>> url += "?start=0&limit=25&fmt=json&rp=ext-comp-1135"
>>> url += "&pv=1&pv=&pv=&mt=24&mk=1"
>>> res = client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
>>> res.status_code
200
>>> r = json.loads(res.content)
>>> r.keys()
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> len(r['rows'])
21

Now imagine that the user gets a break and leaves her browser open,
the server meanwhile did a dump and a reload. So the sessions have
been removed:

>>> sessions.Session.objects.all().delete()

The user comes back and resizes her browser window, or some other
action which will trigger a refresh.  The same URL will now cause a
`PermissionDenied` exception:

>>> res = client.get(url)
>>> res.status_code
403
>>> soup = BeautifulSoup(res.content)
>>> # print(soup.body.prettify())
>>> divs = soup.body.find_all('div')
>>> len(divs)
6
>>> print(divs[3].get_text().strip())
Zugriff verweigert
You have no permission to see this resource.


The above URL is usually issued as an AJAX call.  When an exception
like the above occurs during an AJAX call, Lino's reponse has
different format which is defined by the :mod:`lino.utils.ajax`
middleware.

We must say this explicitly to Django's test client by
setting the extra HTTP header `HTTP_X_REQUESTED_WITH` to
'XMLHttpRequest'.

>>> res = client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
>>> res.status_code
403
>>> print(res.content)
... #doctest: +ELLIPSIS -NORMALIZE_WHITESPACE -REPORT_UDIFF
PermissionDenied
As Anonym you have no permission to run this action.
<BLANKLINE>
TRACEBACK:
...
<BLANKLINE>



