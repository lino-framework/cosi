from .demo import *


class Site(Site):
    pass
    # title = Site.title + " (:memory:)"

SITE = Site(globals())
DATABASES['default']['NAME'] = ':memory:'
