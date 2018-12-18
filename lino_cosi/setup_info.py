# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-cosi',
    # version='0.0.4',
    version='18.12.0',
    install_requires=['lino-xl','django-iban', 'lxml'],
    tests_require=['beautifulsoup4',],
    test_suite='tests',
    description="A Lino application to make accounting simple",
    long_description=u"""

**Lino Così** is a free desktop-like web accounting application.  It
is targeted to small and expanding enterprises or organisations who
want more than an off-the-shelf product.  With Lino Così you will
finally perceive it as a joy to

- manage your contacts, your catalog of products and your account
  chart
- record and print your sales invoices
- record your purchase invoices
- declare your VAT statement
- record your bank statements
- get your financial situation

Lino Così is **almost ready for use**.  Despite the fact that Lino
Così itself keeps things simple, its codebase is **used by more
sophisticated applications** like `Lino Welfare
<http://welfare.lino-framework.org>`__ or `Lino Voga
<http://voga.lino-framework.org>`__.

- For *introductions* and *commercial information* about Lino Così 
  please see `www.saffre-rumma.net
  <http://www.saffre-rumma.net/cosi/>`__.

- You can try it yourself in `our demo sites
  <http://www.lino-framework.org/demos.html>`__

- The central project homepage is http://cosi.lino-framework.org

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://cosi.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django :: 1.11
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: OS Independent
Topic :: Office/Business :: Financial :: Accounting
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_cosi',
    'lino_cosi.lib',
    'lino_cosi.lib.cosi',
    'lino_cosi.lib.b2c',
    'lino_cosi.lib.b2c.fixtures',
    'lino_cosi.lib.contacts',
    'lino_cosi.lib.contacts.fixtures',
    'lino_cosi.lib.contacts.management',
    'lino_cosi.lib.contacts.management.commands',
    'lino_cosi.lib.orders',
])

SETUP_INFO.update(message_extractors={
    'lino_cosi': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/templates_jinja/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(
    # package_data=dict(),
    zip_safe=False,
    include_package_data=True)


# def add_package_data(package, *patterns):
#     l = SETUP_INFO['package_data'].setdefault(package, [])
#     l.extend(patterns)
#     return l


# ~ add_package_data('lino_cosi',
# ~ 'config/patrols/Patrol/*.odt',
# ~ 'config/patrols/Overview/*.odt')

# l = add_package_data('lino_cosi.lib.cosi')
# for lng in 'de fr'.split():
#     l.append('lino_cosi/lib/cosi/locale/%s/LC_MESSAGES/*.mo' % lng)

# l = add_package_data('lino_xl.lib.sepa',
#                      'lino_xl.lib/sepa/config/iban/*')
                     # 'config/iban/*')
# print 20160820, SETUP_INFO['package_data']
# raw_input()
