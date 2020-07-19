from celery import Celery
from flask_mico.conf import settings

application = Celery(settings.SERVICE_NAME,
                     broker=settings.CeleryConfig.BROKER_URL)
application.config_from_object(settings.CeleryConfig)
