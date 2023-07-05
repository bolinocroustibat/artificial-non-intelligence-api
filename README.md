<img src=/images/Cover_photo_Artifical_NonIntelligence.png>

# Artificial Non Intelligence - API

A deep learning generated web game to raise awareness about AI and trolls.
This repository is about the API.

For the Data and Data Analysis, check the [dedicated Data repo](https://github.com/bolinocroustibat/artificial-non-intelligence-data).

For the frontend, check the [dedicated frontend repo](https://github.com/bolinocroustibat/artificial-non-intelligence-frontend).


## Main dependencies

- Python 3.11
- [FastAPI](https://fastapi.tiangolo.com/)
- a PostgreSQL database
- Uvicorn web server


## Run the API locally

Create or update a `settings.py` file on the root with the following settings corresponding on your environement, for example:
```
import tomllib

with open("pyproject.toml", "rb") as f:
    pyproject: dict = tomllib.load(f)
APP_NAME: str = pyproject["project"]["name"]
DESCRIPTION: str = pyproject["project"]["description"]
VERSION: str = pyproject["project"]["version"]
ENVIRONMENT="local"
DATABASE_HOST="127.0.0.1"
DATABASE_USER="root"
DATABASE_PASSWORD="root"
DATABASE_PORT="5432"
DATABASE_DB="artificial-non-intelligence"
ORIGINS=[
    "http://localhost:8888",
    "https://artificial-non-intelligence.netlify.app",
]
SENTRY_DSN = "https://abc123@abc123.ingest.sentry.io/abc123"
```

Create a virtual environment for the project, and install the Python dependencies packages with:
```sh
pip install -r requirements.txt
```

...or, if you use [PDM](https://pdm.fming.dev/):
```sh
pdm install
```

To run the API for local testing, launch the web server in your virtual environnement with:
```sh
uvicorn api.main:app --reload
```
or
```sh
pdm run uvicorn api.main:app --reload
```


## API endpoints

- `/redoc`: Documentation of the API
- `/sessions`: POST a new session id (see `/redoc` for full documentation of this endpoint)
- `/questions`: GET a random question (see `/redoc` for full documentation of this endpoint)
- `/answers`: POST - post the user's answer (see `/redoc` for full documentation of this endpoint)
