# Artificial Non Intelligence - API

<img src=/images/Cover_photo_Artifical_NonIntelligence.png>

A deep learning generated web game to raise awareness about AI and trolls.
This repository is about the API.

For the Data and Data Analysis, check the [dedicated Data repo](https://github.com/bolinocroustibat/artificial-non-intelligence-data).

For the frontend, check the [dedicated frontend repo](https://github.com/bolinocroustibat/artificial-non-intelligence-frontend).


## Requirements

- [Docker](https://www.docker.com/) and Docker Compose (for running the application)
- [uv](https://github.com/astral/uv) package manager (optional, only for development)


## Internal Dependencies

These dependencies are automatically handled by Docker:
- [Python 3.13](https://www.python.org/) ([Alpine](https://hub.docker.com/_/python) based)
- [FastAPI](https://fastapi.tiangolo.com/) with [Uvicorn](https://www.uvicorn.org/)/[Gunicorn](https://gunicorn.org/) workers
- [PostgreSQL 17](https://www.postgresql.org/)
- [uv](https://github.com/astral/uv) package manager


## Running with Docker (recommended)

1. Create a `.env` file in the root directory with the following variables:
```bash
ENVIRONMENT=local
APP_PORT=8000
DB_PORT=5432
POSTGRES_DB=artificial-non-intelligence
SENTRY_DSN=https://abc123@abc123.ingest.sentry.io/abc123
ORIGINS=http://localhost:8888,https://artificial-non-intelligence.netlify.app
```

2. Build and start the containers:
```bash
docker compose up --build
```

The API will be available at `http://localhost:8000` (or whichever port you specified in `APP_PORT`).

### Container Registry

The project uses GitHub Container Registry (GHCR) to store Docker images. The images are automatically built and pushed on each tag release. You can find the container images at:

```
ghcr.io/bolinocroustibat/artificial-non-intelligence-api
```

Available tags:
- `latest`: Latest stable release
- `x.y.z`: Specific version releases


## Run locally (without Docker)

1. Create a `.env` file as described above

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
uv sync

# Or using pip
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Start the development server:
```bash
uvicorn api.main:app --reload
```


## API endpoints

- `/docs`: Documentation of the API in Swagger format
- `/redoc`: Documentation of the API in Redoc format
- `/sessions`: POST a new session id (see `/docs` for full documentation of this endpoint)
- `/questions`: GET a random question (see `/docs` for full documentation of this endpoint)
- `/answers`: POST - post the user's answer (see `/docs` for full documentation of this endpoint)


## Exporting dependencies

To export dependencies from uv.lock to requirements.txt:
```bash
uv export --no-dev --format requirements-txt > requirements.txt
```
