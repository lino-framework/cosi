from .demo import *
SITE.verbose_name = SITE.verbose_name + " (:memory:)"
# SITE = Site(globals())
DATABASES['default']['NAME'] = ':memory:'
