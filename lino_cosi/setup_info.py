# -*- coding: UTF-8 -*-
# Copyright 2014-2015 Luc Saffre
# License: BSD (see file COPYING for details)

SETUP_INFO = dict(
    name='lino-cosi',
    version='0.0.1',
    install_requires=['lino', 'django-iban', 'xlwt', 'lxml'],
    tests_require=['beautifulsoup4', 'commondata', 'commondata.ee', 'commondata.be'],
    test_suite='tests',
    description="A Lino application to make accounting simple",
    long_description="""\
A `Lino <http://www.lino-framework.org>`_ application to
make accounting simple.

""",
    author='Luc Saffre',
    author_email='luc.saffre@gmail.com',
    url="http://cosi.lino-framework.org",
    license='BSD License',
    classifiers="""\
Programming Language :: Python
Programming Language :: Python :: 2
Development Status :: 1 - Planning
Environment :: Web Environment
Framework :: Django
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Topic :: Office/Business :: Scheduling
""".splitlines())

SETUP_INFO.update(packages=[
    'lino_cosi',
    'lino_cosi.lib',
    'lino_cosi.lib.cosi',
    'lino_cosi.lib.accounts',
    'lino_cosi.lib.auto',
    'lino_cosi.lib.auto.sales',
    'lino_cosi.lib.declarations',
    'lino_cosi.lib.finan',
    'lino_cosi.lib.finan.fixtures',
    'lino_cosi.lib.ledger',
    'lino_cosi.lib.ledger.fixtures',
    'lino_cosi.lib.sales',
    'lino_cosi.lib.sales.fixtures',
    'lino_cosi.lib.sepa',
    'lino_cosi.lib.sepa.fixtures',
    'lino_cosi.lib.vat',
    'lino_cosi.lib.vat.fixtures',
    'lino_cosi.lib.vatless',
    'lino_cosi.projects',
    'lino_cosi.projects.apc',
    'lino_cosi.projects.apc.settings',
    'lino_cosi.projects.ylle',
    'lino_cosi.projects.ylle.settings',
    'lino_cosi.projects.pierre',
    'lino_cosi.projects.pierre.settings',
    'lino_cosi.projects.std',
    'lino_cosi.projects.std.settings',
    'lino_cosi.projects.std.tests',
])

SETUP_INFO.update(message_extractors={
    'lino_cosi': [
        ('**/cache/**', 'ignore', None),
        ('**.py', 'python', None),
        ('**.js', 'javascript', None),
        ('**/templates_jinja/**.html', 'jinja2', None),
    ],
})

SETUP_INFO.update(package_data=dict())


def add_package_data(package, *patterns):
    l = SETUP_INFO['package_data'].setdefault(package, [])
    l.extend(patterns)
    return l


# ~ add_package_data('lino_cosi',
# ~ 'config/patrols/Patrol/*.odt',
# ~ 'config/patrols/Overview/*.odt')

l = add_package_data('lino_cosi')
for lng in 'de fr'.split():
    l.append('locale/%s/LC_MESSAGES/*.mo' % lng)
