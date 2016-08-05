import datetime

from lino_cosi.projects.std.settings import *


class Site(DocsSite):
    project_name = 'cosi_std'

    title = "Lino Cosi demo"
    is_demo_site = True
    # ignore_dates_after = datetime.date(2019, 05, 22)
    the_demo_date = datetime.date(2015, 05, 12)
    languages = "en fr de"

    def setup_plugins(self):
        """
        Change the default value of certain plugin settings.

        """
        super(Site, self).setup_plugins()
        self.plugins.ledger.configure(start_year=2015)

SITE = Site(globals())
DEBUG = True
