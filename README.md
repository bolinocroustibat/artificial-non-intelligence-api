# Artificial Non Intelligence

## Data

- As a SQLite database, located in /artificial-non-intelligence/data.
- As a CSV file, from Kaggle, located in /artificial-non-intelligence/data.


## API

To launch the API locally:

`uvicorn api.main:app --reload`

To import a JSON file into the SQLite database:

`python api/import_json.py`


## To deploy on Heroku

Add Heroku app as origin, if necessary:
`heroku git:remote -a non-intelligence-api`

Deploy with:
`git push heroku main`


## Comments crawlers

Located in /artificial-non-intelligence/data-crawler.

Python script to get comments from online website comments and put them in a SQlite database.

Launch the crawler with Python from typer command file:
```sh
python3 ./artificial-non-intelligence/data-crawler/crawl.py [website-crawler]
```

for example, for the crawler "Le Figaro":
```sh
python3 ./artificial-non-intelligence/data-crawler/crawl.py figaro
```
