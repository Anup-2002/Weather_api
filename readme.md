
# Weather Monitoring Service

FastAPI service that stores configured cities and saves their current weather at a fixed interval using Celery and Redis.

## Tech Stack

- Python 3
- FastAPI
- Celery
- Redis
- SQLite
- Open-Meteo API
## Configuration

Create a `.env` file in the project root and add the following environment variables:

```env
DATABASE_URL=sqlite:///./weather.db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast
FETCH_INTERVAL_SECONDS=60
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Database connection URL (SQLite by default). |
| `REDIS_URL` | Redis server URL. |
| `CELERY_BROKER_URL` | Celery broker URL. |
| `CELERY_RESULT_BACKEND` | Celery result backend URL. |
| `OPEN_METEO_URL` | Open-Meteo API endpoint. |
| `FETCH_INTERVAL_SECONDS` | Interval (in seconds) for fetching weather data. |
## Project Setup

Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy the example environment file:

```bash
copy .env.example .env
```

The default database is SQLite and will be created automatically as `weather.db`.

## Redis Setup

Redis is required for Celery. If Redis is installed locally, make sure it is running on `localhost:6379`.

For Docker Desktop:

```bash
docker run --name weather-redis -p 6379:6379 redis:7
```

## Run FastAPI

```bash
uvicorn app.main:app --reload
```

Open the API docs:

```text
http://127.0.0.1:8000/docs
```

## Run Celery Worker

In a second terminal:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

On Windows, use:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info -P solo
```

## Run Scheduled Task

In a third terminal:

```bash
celery -A app.celery_app.celery_app beat --loglevel=info
```

The beat scheduler runs `fetch_weather_for_all_cities` every 60 seconds.

## API Testing

Import `postman_collection.json` into Postman.

### Add City

```http
POST /cities
```

Example body:

```json
{
  "city": "Mumbai",
  "latitude": 19.076,
  "longitude": 72.8777
}
```

### List Cities

```http
GET /cities
```

### Weather History

```http
GET /cities/Mumbai/history
```

After the scheduled task runs, this endpoint returns the saved weather records for the selected city.
