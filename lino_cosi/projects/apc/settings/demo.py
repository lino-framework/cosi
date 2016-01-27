import datetime

from lino_cosi.projects.apc.settings import *


class Site(Site):
    project_name = 'cosi_be_de'
    is_demo_site = True
    # ignore_dates_after = datetime.date(2019, 05, 22)
    the_demo_date = datetime.date(2015, 03, 12)

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.ledger.configure(start_year=2014)
        # print "20151217 a", hash(self.plugins.ledger)


SITE = Site(globals())

# SITE.plugins.ledger.configure(start_year=2014)
# print "20151217 b", hash(SITE.plugins.ledger)
