# -*- coding: UTF-8 -*-
# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-cosi',
    version='20.5.0',
    install_requires=['lino-xl','django-iban', 'lxml'],
    tests_require=['beautifulsoup4'],
    test_suite='tests',
    description="A Lino application to make accounting simple",
    long_description=u"""

**Lino Così** is a
`Lino application <http://www.lino-framework.org/>`__
for accounting (`more <http://cosi.lino-framework.org/about.html>`__).

- We have some `end-user documentation in German
  <http://de.cosi.lino-framework.org/>`__

- This repository is considered an integral part of the Lino framework, which is
  documented as a whole in the `Lino Book
  <http://www.lino-framework.org/about/overview.html>`__.

- Your feedback is welcome.  Our `community page
  <http://www.lino-framework.org/community>`__ explains how to contact us.

- Changes to this particular repository are listed at
  http://cosi.lino-framework.org/changes/

- You can try it yourself in `our demo sites
  <http://www.lino-framework.org/demos.html>`__

- The central project homepage is http://cosi.lino-framework.org

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://cosi.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Office/Business :: Financial :: Accounting
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_cosi',
    'lino_cosi.lib',
    'lino_cosi.lib.cosi',
    'lino_cosi.lib.contacts',
    'lino_cosi.lib.contacts.fixtures',
    'lino_cosi.lib.contacts.management',
    'lino_cosi.lib.contacts.management.commands',
    'lino_cosi.lib.products',
    'lino_cosi.lib.products.fixtures',
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
