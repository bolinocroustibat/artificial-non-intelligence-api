from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import databases
import sqlalchemy
import numpy as np

import ormar

app = FastAPI()


database = databases.Database('../artificial-non-intelligence/data/db.sqlite3')
app.state.database = database

metadata = sqlalchemy.MetaData()

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

class Comments(ormar.Model):
    class Meta:
        tablename = "comments" 
        metadata = metadata
        database = database
        
    id: int = ormar.Integer(primary_key=True)
    content: str = ormar.String(max_length=1000)  #char length
    realness: bool = ormar.Boolean  #double check
    difficulty: int = ormar.Integer(primary_key=False)

# Description: endpoint which take a random comment from the database (human-generated or AI-generated), 
# and send it back along with its ID in the database.
@app.get('/get-random-comment')

def get_random_comment():
        
        num_records = Comments.objects.count()
        
        #np.random.seed(42)   ## optional to set
        id = np.randint(0, num_records)
        content = Comments.objects.get(id=id)
        realness = content.realness
        difficulty = content.difficulty

        return {
            'id': id, 
            'comment': content,
            'realness': realness,
            'difficulty': difficulty
            } 
     
# Description: endpoint which receives the answer from the user from the frontend, compares to the 
# fake flag of the comment in the DB, and answers if it was a good or bad answer.
@app.get('verify-answer')

def verify_answer(questionId, answer):
    
    content = Comments.objects.get(id=questionId)
    realness = content.realness
    
    if answer == realness:
        return {
            'id': questionId,
            'correct': 1 # correct answer  
            }
    else:
        return {
            'id': questionId,
            'correct': 0  # 0 = wrong answer
            }
    

