from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_cosi')
add_demo_project('lino_cosi.projects.std.settings.demo')
add_demo_project('lino_cosi.projects.ylle.settings.demo')
add_demo_project('lino_cosi.projects.apc.settings.demo')
add_demo_project('lino_cosi.projects.pierre.settings.demo')

env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

env.revision_control_system = 'git'

env.cleanable_files = ['docs/api/lino_cosi.*']

env.locale_dir = 'lino_cosi/lib/cosi/locale'
