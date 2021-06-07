import databases
import ormar
import sqlalchemy


database = databases.Database('sqlite:///data/db.sqlite3')
# app.state.database = database
metadata = sqlalchemy.MetaData()


class Comment(ormar.Model):
    """
    Real and fakes comments.
    """
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=3000, nullable=True)
    realness: bool = ormar.Boolean(nullable=True)
    difficulty: int = ormar.Integer(primary_key=False, nullable=True)
    class Meta:
        tablename = "comments" 
        metadata = metadata
        database = database

class Answer(ormar.Model):
    """
    Logged answers from game users.
    """
    id: int = ormar.Integer(primary_key=True)
    answer: str = ormar.Integer()
    ip: bool = ormar.String(max_length=32, nullable=True)
    comment: Comment = ormar.ForeignKey(Comment)
    class Meta:
        tablename = "answers" 
        metadata = metadata
        database = database
