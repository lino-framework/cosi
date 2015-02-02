from lino_cosi.projects.pierre.settings import *


class Site(Site):
    is_demo_site = True

SITE = Site(globals())
