import os
from celery import Celery

# Set default Django settings module for celery app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icdtagger.settings')

# Instantiate the celery app
app = Celery('icdtagger')

# Read config from Django settings, the CELERY namespace would make celery config keys have `CELERY`` prefix
app.config_from_object('django.conf:settings', namespace = 'CELERY')

# Discover and load tasks.py from all registered Django apps
app.autodiscover_tasks()