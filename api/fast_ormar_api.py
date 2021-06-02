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

#Create 1 class / table

class Comments(ormar.Model):
    class Meta:
        tablename = "real_comments" 
        metadata = metadata
        database = database
        
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=1000)  #char length
    realness: bool = ormar.Boolean  #double check
    #difficulty: int = ormar.Integer(primary_key=False)


# Description: endpoint which take a random comment from the database (human-generated or AI-generated), 
# and send it back along with its ID in the database.
@app.get('/get-random-comment')

def get-random-comment():
        ##code how to get random comment from database
        
    
        return {
        'id': 'database_id_of_the_comment', 
        'comment': 'text_content_of_the_comment'
        #'difficulty': 'difficulty_level_of_ai'
        } 
    
    
# Description: endpoint which receives the answer from the user from the frontend, compares to the 
# fake flag of the comment in the DB, and answers if it was a good or bad answer.
@app.get('verify-answer')



def verify-answer(id, user_answer):
    
    # code : request database with id and then compare realness compare with user answer
    # send back to frontend the correct/incorrect verification
    
    return {
        'id': 'database_id_of_the_comment',
        'user_answer': 0 or 1
        }

