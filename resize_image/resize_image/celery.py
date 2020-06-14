import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resize_image.settings')

celery_app = Celery('resize_image')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()
