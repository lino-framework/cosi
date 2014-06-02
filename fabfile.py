from atelier.fablib import *
setup_from_project('lino_cosi', 'lino_cosi.settings.demo')

env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

env.use_mercurial = False
