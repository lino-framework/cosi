from atelier.fablib import *
setup_from_project('lino_cosi','lino_cosi.settings.demo')

env.demo_databases.append('lino_cosi.settings.demo')
#~ env.django_databases.append('userdocs')
# env.tolerate_sphinx_warnings = True

#~ env.languages = 'en de fr'.split()
env.use_mercurial = False
