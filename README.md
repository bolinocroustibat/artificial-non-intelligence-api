# Artificial Non Intelligence - API

A deep learning generated web game to raise awareness about AI and trolls.
This repository is about the API.

For the Data and Data Analysis, check the [dedicated Data repo](https://github.com/bolinocroustibat/artificial-non-intelligence-data).

For the frontend, check the [dedicated frontend repo](https://github.com/bolinocroustibat/artificial-non-intelligence-frontend).


## Main dependencies

- Python 3.9
- [FastAPI](https://fastapi.tiangolo.com/)
- MySQL database (there were a previous version using PostgreSQL to be hosted by Heroku, but it's deprecated. Still available on [heroku branch](https://github.com/bolinocroustibat/artificial-non-intelligence-api/tree/heroku))
- Uvicorn web server


## Run the API locally

Create or update a settings.py file on the root with the following settings (example):
```
DATABASE_HOST="127.0.0.1"
DATABASE_USER="root"
DATABASE_PASSWORD="root"
DATABASE_PORT="8889"
DATABASE_DB="artificial-non-intelligence"
```

Create a virtual environment for the project, and install the Python dependencies packages with:
```sh
pip install -r requirements.txt
```

...or, if you use [Poetry](https://python-poetry.org/) (which is much better and strongly advised):
```sh
poetry install
```

To run the API for local testing, launch the web server in your virtual environnement with:
```sh
uvicorn api.main:app --reload
```


## API endpoints

- `/redoc`: Documentation of the API
- `/comments`: GET a random comment (see `/redoc` for full documentation of this endpoint)
- `/answers`: GET - verify the user's answer (see `/redoc` for full documentation of this endpoint)
- `/scores`: GET - send score (see `/redoc` for full documentation of this endpoint)
