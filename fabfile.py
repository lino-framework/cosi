from atelier.fablib import *
setup_from_project('lino_cosi', 'lino_cosi.settings.demo')

env.demo_databases.append('lino_cosi.settings.est.demo')
env.demo_databases.append('lino_cosi.settings.be.demo')
env.demo_databases.append('lino_cosi.settings.start.demo')

env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

env.use_mercurial = False
