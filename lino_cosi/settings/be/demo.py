from lino_cosi.settings.be import *


class Site(Site):
    title = Site.title + ' demo'
    is_demo_site = True

SITE = Site(globals())


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
