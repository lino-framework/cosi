.. _cosi.tested.bel_de:

Lino Così in Eupen
==================

The APC version of :ref:`cosi` is for East Belgium.

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_bel_de


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


The following reproduces a unicode error which occurred when Lino
tried to say "As Anonymous you have no permission to run this action."
in German (where the internationlized text (u'Als Anonym haben Sie
nicht die Berechtigung, diese Aktion auszuf\xfchren.') contains
non-ascii characters.

The error was::

  UnicodeEncodeError at /api/sales/InvoicesByJournal
  'ascii' codec can't encode character u'\xfc' in position 64: ordinal not in range(128)

>>> url = '/api/sales/InvoicesByJournal'
>>> url += "?start=0&limit=25&fmt=json&rp=ext-comp-1135&pv=1&pv=&pv=&mt=24&mk=1"

We cannot use the `doctests` settings because the situation happens
only with session-based authentication.

>>> client = Client()

Some client logged in and gets some data:

>>> res = client.post('/auth', data=dict(username="rolf", password="1234"))
>>> res.status_code
200
>>> r = json.loads(res.content)
>>> print(r['message'])
Now logged in as u'rolf'
>>> r['success']
True

>>> res = client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
>>> res.status_code
200
>>> r = json.loads(res.content)
>>> r.keys()
[u'count', u'rows', u'success', u'no_data_text', u'title', u'param_values']
>>> len(r['rows'])
21

Now imagine that the server meanwhile did a dump and a reload. So the
sessions have been removed:

>>> sessions.Session.objects.all().delete()

The same URL will now cause a `PermissionDenied` exception:

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



