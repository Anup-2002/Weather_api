from celery import Celery
from app.config import get_settings
settings = get_settings()
# Celery app 
celery_app = Celery(
    "weather_monitor",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["app.tasks"],
)

celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "fetch-weather-every-minute": {
        "task": "app.tasks.fetch_weather_for_all_cities",
        "schedule": settings.fetch_interval_seconds,
    }
}