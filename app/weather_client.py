from typing import Any
import requests
from app.config import get_settings
def fetch_current_weather(latitude: float, longitude: float) -> dict[str, Any]:
    settings = get_settings()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",
    }

    response = requests.get(settings.open_meteo_url, params=params, timeout=15)
    response.raise_for_status()

    data = response.json()
    current_weather = data.get("current_weather")
    if not current_weather:
        raise ValueError("Current weather data was not returned by Open-Meteo")
    # return current data
    return current_weather
