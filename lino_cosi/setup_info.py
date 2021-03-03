# -*- coding: UTF-8 -*-
# Copyright 2014-2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-cosi',
    version='20.12.0',
    install_requires=['lino-xl','django-iban', 'lxml'],
    # tests_require=['beautifulsoup4'],  # satisfied by lino deps
    test_suite='tests',
    description="A Lino application to make accounting simple",
    long_description=u"""

**Lino Così** is a
`Lino application <http://www.lino-framework.org/>`__
for accounting (`more <https://cosi.lino-framework.org/about.html>`__).

- The central project homepage is http://cosi.lino-framework.org

- You can try it yourself in `our demo sites
  <https://www.lino-framework.org/demos.html>`__

- We have some `end-user documentation in German
  <https://de.cosi.lino-framework.org/>`__

- Technical specs are at https://www.lino-framework.org/specs/cosi

- This is an integral part of the Lino framework, which is documented
  at https://www.lino-framework.org

- The changelog is at https://www.lino-framework.org/changes

- For introductions, commercial information and hosting solutions
  see https://www.saffre-rumma.net

- This is a sustainably free open-source project. Your contributions are
  welcome.  See https://community.lino-framework.org for details.

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="https://cosi.lino-framework.org",
    license='BSD-2-Clause',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 3
Development Status :: 5 - Production/Stable
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
