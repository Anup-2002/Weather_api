from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
# pydantic models validation
class CityCreate(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class CityOut(BaseModel):
    id: int
    city: str
    latitude: float
    longitude: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WeatherHistoryOut(BaseModel):
    id: int
    city: str
    temperature: float
    wind_speed: float
    weather_code: int
    fetched_at: datetime

    model_config = ConfigDict(from_attributes=True)
