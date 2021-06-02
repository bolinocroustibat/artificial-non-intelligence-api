import databases
import ormar
import sqlalchemy


database = databases.Database('sqlite:///data/db.sqlite3')
# app.state.database = database
metadata = sqlalchemy.MetaData()


class Comment(ormar.Model):
    """
    The only table in our database.
    """
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=3000)
    realness: bool = ormar.Boolean()
    difficulty: int = ormar.Integer(primary_key=False, nullable=True)
    class Meta:
        tablename = "comments" 
        metadata = metadata
        database = database
