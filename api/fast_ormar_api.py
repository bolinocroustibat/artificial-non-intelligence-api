from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import databases
import sqlalchemy

import ormar

app = FastAPI()

database = databases.Database("sqlite:///test.db")
app.state.database = database


#If using middleware 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#If not using middleware: defining startup and shutdown events
@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

#Defining ORMAR models
class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)


class Item(ormar.Model):
    class Meta:
        tablename = "items"
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.String(max_length=100)
    category: Optional[Category] = ormar.ForeignKey(Category, nullable=True)



# Description: endpoint which take a random comment from the database (human-generated or AI-generated), 
# and send it back along with its ID in the database.
@app.get('/get-random-comment')

def get-random-comment():
        return {
        'id': 'database_id_of_the_comment', 
        'comment': 'text_content_of_the_comment'
        #'difficulty': 'difficulty_level_of_ai'
        } 
    
    
# Description: endpoint which receives the answer from the user from the frontend, compares to the 
# fake flag of the comment in the DB, and answers if it was a good or bad answer.
@app.get('verify-answer')

user_input = {
        'id': 'database_id_of_the_comment',
        'user_answer': 0 or 1
        }

def verify-answer(user_input):
    return {
        'id': 'database_id_of_the_comment',
        'user_answer': 0 or 1
        }

