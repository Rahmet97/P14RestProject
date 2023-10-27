import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P14RestProject.settings')

app = Celery('P14RestProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
