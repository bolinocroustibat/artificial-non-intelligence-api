# Artificial Non Intelligence

## Data

- As a SQLite database, located in /artificial-non-intelligence/data.
- As a CSV file, from Kaggle, located in /artificial-non-intelligence/data.


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


## API

TO DO



## Frontend

Located in `/frontend` for now.
Basic frontend with HTML, CSS and JavaScript, no dependencies.


## To deploy on Heroku

Add Heroku app as origin, if necessary:
`heroku git:remote -a artificial-non-intelligence`

Deploy with:
`git push heroku master`
