from atelier.tasks import *
env.setup_from_tasks(globals(), 'lino_cosi')
env.add_demo_project('lino_cosi.projects.std.settings.demo')
env.add_demo_project('lino_cosi.projects.ylle.settings.demo')
env.add_demo_project('lino_cosi.projects.apc.settings.demo')
env.add_demo_project('lino_cosi.projects.pierre.settings.demo')

# env.languages = "en de fr et nl es".split()

# env.tolerate_sphinx_warnings = True

# env.revision_control_system = 'git'

# env.cleanable_files = ['docs/api/lino_cosi.*']

# env.locale_dir = 'lino_cosi/lib/cosi/locale'
