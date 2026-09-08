# W1-03 — docker-compose.yml: FastAPI + PostgreSQL + Redis

## Objective
Write a `docker-compose.yml` that spins up three services locally — a FastAPI backend, PostgreSQL, and Redis — as a foundation for Chrysoptera's backend infrastructure.

## Project structure
```
chrysoptera-stack/
├── docker-compose.yml
└── api/
    ├── main.py
    ├── requirements.txt
    └── Dockerfile
```

## The FastAPI app (api/main.py)
A minimal app with two endpoints, matching what Week 2's actual backend task will need:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/readings")
def readings():
    return [{"site_id": 1, "solar_output_kw": 4.2}, {"site_id": 2, "solar_output_kw": 3.8}]
```

## The Dockerfile (api/Dockerfile)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## The docker-compose.yml
```yaml
services:
  api:
    build: ./api
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: chrysoptera
      POSTGRES_PASSWORD: chrysoptera_dev
      POSTGRES_DB: chrysoptera_dev
    ports:
      - "5432:5432"

  redis:
    image: redis:7
    ports:
      - "6379:6379"
```

Three services, networked together automatically by Docker Compose:
- **api** — the custom FastAPI app, built from the local Dockerfile
- **db** — official PostgreSQL 16 image, pre-configured with a dev user/password/database
- **redis** — official Redis 7 image, for future caching/session needs

## Command used
```
docker compose up --build
```

## Troubleshooting encountered

**Problem — `requirements.txt` invalid requirement error:**
```
ERROR: Invalid requirement: 'fastapi uvicorn[standard]' (from line 1 of requirements.txt)
```
Both package names had ended up on the same line instead of separate lines (a line break didn't register while typing). **Fix:** retyped the file with `fastapi` and `uvicorn[standard]` on two distinct lines, confirmed with a fresh save, then rebuilt — install succeeded.

## Verification
All three containers started cleanly:
- `redis-1` — "Ready to accept connections tcp"
- `db-1` — "database system is ready to accept connections"
- `api-1` — "Uvicorn running on http://0.0.0.0:8000"

Confirmed from the browser:
- `http://localhost:8000/health` → `{"status":"ok"}`
- `http://localhost:8000/readings` → mock JSON array of solar site readings
- `http://localhost:8000/docs` → FastAPI's auto-generated interactive API documentation, listing both endpoints

Stack stopped cleanly afterward with `docker compose down`.

## Outcome
A fully working local backend stack — API + database + cache — defined entirely as code in a single `docker-compose.yml`, reproducible on any machine with Docker installed. This is the foundation Week 2's actual API development (database schema, real endpoints, authentication) will build on top of.

*(Screenshots of /health, /readings, and /docs kept alongside this document.)*
