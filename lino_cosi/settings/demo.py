from lino_cosi.settings import *
SITE = Site(globals(), title="Lino-Cosi demo", is_demo_site=True)
# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
