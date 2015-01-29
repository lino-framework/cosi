from atelier.fablib import *
setup_from_fabfile(globals(), 'lino_cosi')
add_demo_project('lino_cosi/projects/std')
add_demo_project('lino_cosi/projects/ylle')
add_demo_project('lino_cosi/projects/apc')
add_demo_project('lino_cosi/projects/pierre')

env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

env.revision_control_system = 'git'
