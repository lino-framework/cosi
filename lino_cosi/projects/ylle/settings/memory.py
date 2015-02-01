from .demo import *


class Site(Site):
    # title = Site.title + " (:memory:)"
    pass

SITE = Site(globals())
DATABASES['default']['NAME'] = ':memory:'
