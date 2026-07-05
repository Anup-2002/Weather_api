from sqlalchemy import select

from app.celery_app import celery_app
from app.database import SessionLocal, create_tables
from app.models import MonitoredCity, WeatherHistory
from app.weather_client import fetch_current_weather

# Fetch data for all cities in database
@celery_app.task(name="app.tasks.fetch_weather_for_all_cities")
def fetch_weather_for_all_cities() -> dict[str, int]:
    create_tables()
    db = SessionLocal()
    saved_count = 0
    failed_count = 0
    try:
        cities = db.scalars(select(MonitoredCity).order_by(MonitoredCity.city)).all()

        for city in cities:
            try:
                current_weather = fetch_current_weather(city.latitude, city.longitude)
                history = WeatherHistory(
                    city=city.city,
                    temperature=float(current_weather["temperature"]),
                    wind_speed=float(current_weather["windspeed"]),
                    weather_code=int(current_weather["weathercode"]),
                )
                db.add(history)
                saved_count += 1
            except Exception:
                failed_count += 1
        db.commit()
        return {"saved": saved_count, "failed": failed_count}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
