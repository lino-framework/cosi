from lino_cosi.settings import *
ad.configure_plugin('contacts', hide_region=True)
SITE = Site(globals(), title="Lino Cosi demo", is_demo_site=True)


# the following line should not be active in a checked-in version
#~ DATABASES['default']['NAME'] = ':memory:'
