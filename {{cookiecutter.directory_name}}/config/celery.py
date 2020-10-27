{%- if cookiecutter.celery == "Yes" -%}
import os

from celery import Celery
from django.conf import settings
from kombu import Exchange

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", broker=settings.CELERY_BROKER_URL)
app.config_from_object("config.settings", namespace="CELERY")

default_exchange = Exchange('boilerplate', type='direct')

app.conf.task_default_queue = 'boilerplate'
app.conf.task_default_exchange = 'boilerplate'
app.conf.task_default_routing_key = 'boilerplate'
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


{%- elif cookiecutter.celery == "No" -%}

{% endif %}