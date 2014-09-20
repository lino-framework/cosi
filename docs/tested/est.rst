.. _cosi.tested.est:

Estonia
=======

The Estonian version of :ref:`cosi` imports every place in Estonia
from :mod:`commondata.ee`.

.. include:: /include/tested.rst

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
============= ================== ============== ==========
 Designation   Designation (et)   Place Type     zip code
------------- ------------------ -------------- ----------
 Juuru                            Municipality
 Järvakandi                       Municipality
 Kaiu                             Municipality
 Kehtna                           Municipality
 Kohila                           Municipality
 Käru                             Municipality
 Märjamaa                         Municipality
 Raikküla                         Municipality
 Rapla                            Town
 Vigala                           Municipality
============= ================== ============== ==========
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
============= ================== =============== ==========
 Designation   Designation (et)   Place Type      zip code
------------- ------------------ --------------- ----------
 Atla                             Küla            79403
 Helda                            Küla            79417
 Härgla                           Küla            79404
 Hõreda                           Küla            79010
 Jaluse                           Küla            79410
 Juuru                            Small borough
 Järlepa                          Küla
 Kalda                            Küla            79418
 Lõiuse                           Küla            79405
 Mahtra                           Küla            79407
 Orguse                           Küla
 Pirgu                            Küla
 Sadala                           Küla            79419
 Vankse                           Küla            79406
============= ================== =============== ==========
<BLANKLINE>
