import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('DJANGO_ENV', 'dev')  # Default to 'dev'

if env == 'prod':
    from .settings_prod import *
else:
    from .settings_dev import *