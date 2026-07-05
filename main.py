from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import create_tables, get_db
from app.models import MonitoredCity, WeatherHistory
from app.schemas import CityCreate, CityOut, WeatherHistoryOut


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    create_tables()
    yield


app = FastAPI(
    title="Weather Monitoring Service",
    lifespan=lifespan
)


@app.post("/cities", response_model=CityOut, status_code=status.HTTP_201_CREATED)
def add_city(city_data: CityCreate, db: Session = Depends(get_db)):
    city_name = city_data.city.strip()

    if city_name == "":
        raise HTTPException(
            status_code=400,
            detail="City name cannot be empty"
        )

    city = MonitoredCity(
        city=city_name,
        latitude=city_data.latitude,
        longitude=city_data.longitude
    )

    db.add(city)

    try:
        db.commit()
        db.refresh(city)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="City already exists"
        )

    return city

@app.get("/cities", response_model=list[CityOut])
def list_cities(db: Session =Depends(get_db)):
    cities = db.scalars(
        select(MonitoredCity).order_by(MonitoredCity.city)
    ).all()

    return cities


@app.get("/cities/{city}/history", response_model=list[WeatherHistoryOut])
def city_weather_history(city: str, db: Session = Depends(get_db)):
    history = db.scalars(
        select(WeatherHistory)
        .where(WeatherHistory.city == city)
        .order_by(WeatherHistory.fetched_at.desc())
    ).all()

    return history
@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather Monitoring Service"}