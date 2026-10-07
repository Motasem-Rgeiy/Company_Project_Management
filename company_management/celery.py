import os
from celery import Celery

# Set default Django settings module for 'project'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_management.settings')

app = Celery('company_management')

# Load task config from Django settings using the 'CELERY' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks.py in all registered INSTALLED_APPS
app.autodiscover_tasks()