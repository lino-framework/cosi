from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_cosi')
add_demo_database('lino_cosi.projects.std.settings.demo')
add_demo_database('lino_cosi.projects.ylle.settings.demo')
add_demo_database('lino_cosi.projects.apc.settings.demo')
add_demo_database('lino_cosi.projects.pierre.settings.demo')
# add_demo_database('lino_cosi.settings.start.demo')

env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

env.revision_control_system = 'git'
