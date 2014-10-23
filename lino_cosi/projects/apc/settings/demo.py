from ..settings import *


class Site(Site):
    title = Site.title + ' demo'
    is_demo_site = True

SITE = Site(globals())
