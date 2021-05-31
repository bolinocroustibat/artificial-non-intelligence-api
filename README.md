# Artificial Non Intelligence

## Data

As a SQLite database, located in /artificial-non-intelligence/data.

## Comments crawlers

Located in /artificial-non-intelligence/data-crawler.

Python script to get comments from online website comments and put them in a SQlite database.

### Command to crawl comments

Launch the crawler with Python from typer command file:
```sh
python3 ./artificial-non-intelligence/data-crawler/crawl.py [website-crawler]
```

for example, for the crawler "Le Figaro":
```sh
python3 ./artificial-non-intelligence/data-crawler/crawl.py figaro
```
