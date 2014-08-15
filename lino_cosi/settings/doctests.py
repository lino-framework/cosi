from ..settings import *
SITE = Site(globals(), no_local=True,
            remote_user_header='REMOTE_USER',
            hidden_languages='de fr')
#~ hidden_languages is for tested docs
DEBUG = True
