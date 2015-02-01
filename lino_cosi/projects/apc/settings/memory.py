from .demo import *


class Site(Site):
    verbose_name = Site.verbose_name + " (:memory:)"

SITE = Site(globals())
DATABASES['default']['NAME'] = ':memory:'
