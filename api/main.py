from datetime import datetime

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from pydantic import BaseModel
import random
from typing import Optional, Tuple
import uuid

DATABASE_URL = os.environ['DATABASE_URL']


app = FastAPI()

# For security (avoid another app to connect to this API)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins (debug, remove for production)
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://artificial-non-intelligence.herokuapp.com",
        "https://artificial-non-intelligence.herokuapp.com",
        "http://www.artificial-non-intelligence.me",
        "https://www.artificial-non-intelligence.me"
    ],  # Allows only the frontend origin, use that for production
    allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    allow_methods=["GET", "POST"],  # Allows only GET and POST method
    allow_headers=["*"],  # Allows all headers
)


@app.get('/questions')
async def get_new_question(aggressive: Optional[bool] = None) -> dict:
        """
        Endpoint which takes a random comment from the database (human-generated or AI-generated), and sends it back along with its ID in the database.
        """

        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        with connection:
            real: int = random.choice([0, 1])
            if type(aggressive) == bool:
                aggressive_int = 1 if aggressive else 0
                query: str = f"SELECT id, content FROM questions WHERE real={real} AND aggressive={aggressive_int} ORDER BY RANDOM() LIMIT 1;"

            else:
                query: str = f"SELECT id, content FROM questions WHERE real={real} ORDER BY RANDOM() LIMIT 1;"
            cursor = connection.cursor()
            cursor.execute(query)
            question: Tuple = cursor.fetchone()
            cursor.close()
        return {
            'id': question[0], 
            'question': question[1],
            }


@app.post('/sessions')
async def start_new_session(request: Request) -> dict:
    """
    Start a new game, create a session
    """
    session_uid: str = uuid.uuid4()
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    with connection:
        client_host = request.client.host
        query: str = f"INSERT INTO sessions (ip, uuid) VALUES ('{client_host}', '{session_uid}');"
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
    return {'sessionUid': session_uid}


class AnswerPayload(BaseModel):
    sessionUid: str
    questionId: int
    answer: int


@app.post('/answers')
async def post_answer(
    body: AnswerPayload,
    request: Request
    ) -> dict:
    """
    Endpoint which receives the answer from the user from the frontend, compares to the fake flag of the comment in the DB, and updates the score.
    """
    print(body)
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    with connection:

        try:
            # Get the session ID and current score
            query: str = f"SELECT id, score, lives FROM sessions WHERE uuid='{body.sessionUid}';"
            cursor = connection.cursor()
            cursor.execute(query)
            session: Tuple = cursor.fetchone()
            session_id: int = session[0]
            score: int = session[1]
            lives: int = session[2]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Session does not exist")

        try:
            # Get the question
            query: str = f"SELECT id, real FROM questions WHERE id={body.questionId};"
            cursor = connection.cursor()
            cursor.execute(query)
            question: Tuple = cursor.fetchone()
            question_id: int = question[0]
            real: int = question[1]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Question does not exist")

        try:
            # Add answer to the DB
            client_host = request.client.host
            query: str = f"INSERT INTO answers (answer, question_id, ip, session_id) VALUES ({body.answer}, {question_id}, '{client_host}', {session_id});"
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
        
        if body.answer == real:
            # Update the session with the score +1
            correct = 1
            score += 1
            query: str = f"UPDATE sessions SET score={score} WHERE id={session_id};"
            cursor = connection.cursor()
            cursor.execute(query)
        else:
            correct = 0
            lives = lives - 1
            if lives > 0:
                # Update the session with the lives -1
                query: str = f"UPDATE sessions SET lives={lives} WHERE id={session_id};"
                cursor = connection.cursor()
                cursor.execute(query)
            else:
                # End the session and get the top score
                ended = datetime.utcnow()
                query: str = f"UPDATE sessions SET lives=0, ended='{ended}' WHERE id={session_id};"
                cursor = connection.cursor()
                cursor.execute(query)
                query: str = f"SELECT MAX(score) FROM sessions;"
                cursor.execute(query)
                top_score: int = cursor.fetchone()[0]
                cursor.close()
                return {
                    'correct': correct,
                    'lives': 0,
                    'score': score,
                    'topScore': top_score,
                    }

        cursor.close()

    return {'correct': correct, 'lives': lives, 'score': score}
