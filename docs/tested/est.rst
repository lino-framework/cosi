.. _cosi.tested.est:

Estonia
=======

The Estonian version of :ref:`cosi` imports every place in Estonia
from :mod:`commondata.ee`.

.. include:: /include/tested.rst

.. to test only this document:
  $ python setup.py test -s tests.DocsTests.test_est


>>> from __future__ import print_function
>>> from __future__ import unicode_literals
>>> import os
>>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino_cosi.settings.est.demo'
>>> from __future__ import print_function 
>>> from __future__ import unicode_literals
>>> from lino.runtime import *
>>> from django.test.client import Client
>>> ses = rt.login("rando")
>>> dd.translation.activate('et')


The estonian `Wikipedia
<https://et.wikipedia.org/wiki/Rapla_maakond>`_ says:

    Rapla maakonnas on 10 omavalitsusüksust (valda):

    Juuru vald - Järvakandi vald - Kaiu vald - Kehtna vald - Kohila vald - Käru vald - Märjamaa vald - Raikküla vald - Rapla vald - Vigala vald
    
Lino and :mod:`commondata.ee` agree with this:

>>> raplamaa = countries.Place.objects.get(
...    name="Rapla", type=countries.PlaceTypes.county)
>>> ses.show("countries.PlacesByPlace", raplamaa)
============ ============== =========== ==========
 Nimetus      Nimetus (et)   Asumiliik   zip code
------------ -------------- ----------- ----------
 Juuru                       Vald
 Järvakandi                  Vald
 Kaiu                        Vald
 Kehtna                      Vald
 Kohila                      Vald
 Käru                        Vald
 Märjamaa                    Vald
 Raikküla                    Vald
 Rapla                       Linn
 Vigala                      Vald
============ ============== =========== ==========
<BLANKLINE>

Another test is the 
`municipality of Juuru
<https://et.wikipedia.org/wiki/Juuru_vald>`_ for which Wikipedia 
announces one small borough and 14 villages:

    Juuru vallas on üks alevik (Juuru, elanikke 597) ja 14 küla: Atla (91), Helda, Hõreda (80), Härgla (84), Jaluse (40), Järlepa (235), Kalda, Lõiuse (103), Mahtra (99), Maidla (124), Orguse (43), Pirgu (102), Sadala ja Vankse (30).

Lino and :mod:`commondata.ee` again agree with this:

>>> juuru = countries.Place.objects.get(name="Juuru", 
...    type=countries.PlaceTypes.municipality)
>>> ses.show("countries.PlacesByPlace", juuru)
========= ============== =========== ==========
 Nimetus   Nimetus (et)   Asumiliik   zip code
--------- -------------- ----------- ----------
 Atla                     Küla        79403
 Helda                    Küla        79417
 Härgla                   Küla        79404
 Hõreda                   Küla        79010
 Jaluse                   Küla        79410
 Juuru                    Alevik
 Järlepa                  Küla
 Kalda                    Küla        79418
 Lõiuse                   Küla        79405
 Mahtra                   Küla        79407
 Orguse                   Küla
 Pirgu                    Küla
 Sadala                   Küla        79419
 Vankse                   Küla        79406
========= ============== =========== ==========
<BLANKLINE>


Formatting postal addresses
---------------------------

>>> eesti = countries.Country.objects.get(isocode="EE")
>>> sindi = countries.Place.objects.get(name="Sindi")
>>> p = contacts.Person(first_name="Malle", last_name="Mets", 
...     street=u"Männi tn", street_no="5", street_box="-6", 
...     zip_code="86705", country=eesti, city=sindi)
>>> print(p.address)
Malle Mets
Männi tn 5-6
86705 Sindi
Estonia

Townships in Estonia get special handling: their name is replaced by
the town's name when a zip code is known:

>>> city = countries.Place.objects.get(name="Kesklinn")
>>> print(city)
Kesklinn
>>> print(city.type)
township
>>> p = contacts.Person(first_name="Kati", last_name="Kask", 
...     street="Tartu mnt", street_no="71", street_box="-5", 
...     zip_code="10115", country=eesti, city=city)
>>> print(p.address)
Kati Kask
Tartu mnt 71-5
10115 Tallinn
Estonia

For countryside addresses, 

>>> city = countries.Place.objects.get(name="Vana-Vigala")
>>> print(city.type)
village
>>> p = contacts.Person(first_name="Kati", last_name="Kask", 
...     street="Hirvepargi", street_no="123", 
...     zip_code="78003", country=eesti, city=city)
>>> print(p.address)
Kati Kask
Hirvepargi 123
Vana-Vigala küla
Vigala vald
78003 Rapla maakond
Estonia
