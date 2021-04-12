# -*- coding: utf-8 -*-

from lino.sphinxcontrib import configure ; configure(globals())

extensions += ['lino.sphinxcontrib.logo']

from atelier.sphinxconf import interproject
interproject.configure(globals(), 'atelier etgen')
intersphinx_mapping['book'] = (
    'http://www.lino-framework.org', None)

html_context.update(public_url='https://cosi.lino-framework.org')

project = "Lino Così website"
html_title = "Lino Così"
copyright = '2012-2021 Rumma & Ko Ltd'

# extlinks.update({
#     'djangoticket': (
#         'http://code.djangoproject.com/ticket/%s', 'Django ticket #'),
# })
# extlinks.update(
#     ticket=('https://jane.mylino.net/#/api/tickets/AllTickets/%s', '#'))


print(20210412, exclude_patterns)
