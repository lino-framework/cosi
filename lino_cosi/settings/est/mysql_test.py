from .demo import *


class Site(Site):
    title = Site.title + " (:memory:)"

SITE = Site(globals())
DATABASES['default']['NAME'] = ':memory:'
