from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random
import sqlite3
from typing import Optional, Tuple


app = FastAPI()

# For security (avoid another app to connect to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (debug, remove for production)
    # allow_origins=[
    #     "http://localhost",
    #     "http://127.0.0.1",
    #     "https://artificial-non-intelligence.herokuapp.com"
    # ], (allows only the frontend origin, use that for production)
    allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    allow_methods=["GET"],  # Allows only GET method
    allow_headers=["*"],  # Allows all headers
)


@app.get('/get-random-comment')
async def get_random_comment(aggressive: Optional[bool] = None) -> dict:
        """
        Endpoint which takes a random comment from the database (human-generated or AI-generated), and sends it back along with its ID in the database.
        """

        # Get a random record from DB with equal chances between real and AI
        connection = sqlite3.connect("data/db.sqlite3")
        with connection:

            real: int = random.choice([0, 1])

            if type(aggressive) == bool:
                aggressive_int = 1 if aggressive else 0
                query: str = f"SELECT id, content FROM comments WHERE real={real} AND aggressive={aggressive_int} ORDER BY RANDOM() LIMIT 1;"
    
            else:
                query: str = f"SELECT id, content FROM comments WHERE real={real} ORDER BY RANDOM() LIMIT 1;"

            cursor = connection.cursor()
            cursor.execute(query)
            comment: Tuple = cursor.fetchone()
            cursor.close()

        return {
            'id': comment[0], 
            'comment': comment[1],
            }


@app.get('/verify-answer')
async def verify_answer(
    questionId: int,
    answerId: int,
    request: Request
    ) -> dict:
    """
    Endpoint which receives the answer from the user from the frontend, compares to the fake flag of the comment in the DB, and answers if it was a good or bad answer.
    """

    connection = sqlite3.connect("data/db.sqlite3")
    with connection:
        query: str = f"SELECT id, real FROM comments WHERE id={questionId};"
        cursor = connection.cursor()
        cursor.execute(query)
        comment: Tuple = cursor.fetchone()
        try:
            client_host = request.client.host
            query: str = f'INSERT INTO answers (answer, comment, ip) VALUES ({answerId}, {comment[0]}, "{client_host}");'
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
        cursor.close()

    if answerId == comment[1]:
        return {
            'id': questionId,
            'correct': 1 # correct answer  
            }
    return {
        'id': questionId,
        'correct': 0  # 0 = wrong answer
        }
