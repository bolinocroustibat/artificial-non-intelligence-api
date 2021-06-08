# Artificial Non Intelligence - API

A deep learning generated web game to raise awareness about AI and trolls.
This repository is about the API.

For the frontend, check the [dedicated frontend repo](https://github.com/bolinocroustibat/artificial-non-intelligence-frontend).


## Main dependencies

- Python 3.8 or 3.9
- FastAPI
- PostgreSQL database (currently Heroku Postgre)
- Uvicorn web server


## Run the API locally

Create a virtual environment for the project, and install the Python dependencies packages with:
```sh
pip install -r requirements.txt
```

...or, if you use Poetry (which is much better and strongly advised):
```sh
poetry install
```

To run the API for local testing, launch the web server in your virtual environnement with:
```sh
uvicorn api.main:app --reload
```


## API endpoints

- `/redoc`: Documentation of the API
- `/get-random-comment`: Get a random comment (see `/redoc` for full documentation of this endpoint)
- `/verify-answer`: Verify the user's answer (see `/redoc` for full documentation of this endpoint)


## To deploy on Heroku

Add Heroku app as git origin, if necessary:
```sh
heroku git:remote -a non-intelligence-api
```

Deploy with:
```sh
git push heroku main
```


## Database

### Schema

The database consists of two tables:

- `comments`: stores the human-generated and ai-generated comments, along with their unique ID, a flag `real` to indicate if it's human or ai generated and a few minor other infos. This table is used for the API to serve the game content.
```sql
CREATE TABLE comments (
	id SERIAL,
	content TEXT NOT NULL,
	real INTEGER NOT NULL,
	aggressive INTEGER,
	difficulty INTEGER,
	created timestamp DEFAULT CURRENT_TIMESTAMP
);
```

- `answers`: stores the answers from users from the game. Each answer has a foreign key to the `comments` table, and the IP adress of the user, along with few minor other infos:
```sql
CREATE TABLE answers (
	id SERIAL,
	answer INT NOT NULL,
	ip VARCHAR,
	comment INTEGER NOT NULL,
	FOREIGN KEY (comment) REFERENCES comments (id)
);
```


### Remove duplicate from the comments table of the DB

The import script doesn't check in the DB if there's any duplicates.
To remove the duplicated comments content from the DB at any time, use the following SQL command:
```sql
DELETE FROM comments
WHERE id NOT in(
		SELECT
			min(id)
			FROM comments
		GROUP BY
			content);
```
(this should be added to the import script in the future)
