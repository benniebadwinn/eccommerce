from __future__ import absolute_import, unicode_literals
from celery import Celery
from django.conf import settings
import os
from django.conf import settings



app.autodiscover_tasks()

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moontag_project.settings')

# create a Celery instance and configure it using the settings from Django
celery_app = Celery('moontag_project')

app = Celery('moontag_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



app = Celery('moontag_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

# celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery Beat Configuration
app.conf.beat_schedule = {
    'update-product-prices': {
        'task': 'your_app.tasks.update_product_prices',
        'schedule': 3600,  # Run every 1 hour (adjust as needed)
    },
}





