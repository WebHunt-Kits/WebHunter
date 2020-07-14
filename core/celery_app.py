from celery import Celery
from flask_mico.conf import settings

celery_app = Celery(settings.SERVICE_NAME,
                    broker=settings.CeleryConfig.BROKER_URL)
celery_app.config_from_object(settings.CeleryConfig)
