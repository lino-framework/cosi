from atelier.tasks import ns
ns.setup_from_tasks(
    globals(), "lino_cosi",
    languages="en de fr et nl es".split(),
    # tolerate_sphinx_warnings=True,
    blogref_url="http://luc.lino-framework.org",
    locale_dir='lino_cosi/lib/cosi/locale',
    revision_control_system='git',
    cleanable_files=['docs/api/lino_cosi.*'],
    demo_projects=['lino_cosi.projects.std.settings.demo'])


