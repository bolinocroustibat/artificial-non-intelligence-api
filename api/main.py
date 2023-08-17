import random
import uuid
from datetime import datetime
from typing import Optional, Tuple

import psycopg
import sentry_sdk
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from settings import (
    APP_NAME,
    DATABASE_DB,
    DATABASE_HOST,
    DATABASE_PASSWORD,
    DATABASE_PORT,
    DATABASE_USER,
    DESCRIPTION,
    ENVIRONMENT,
    ORIGINS,
    SENTRY_DSN,
    VERSION,
)

# Initialize Sentry error logging
if ENVIRONMENT in ["production", "staging"]:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        release=f"{APP_NAME}@{VERSION}",
        traces_sample_rate=1.0,
        # Experimental profiling
        _experiments={
            "profiles_sample_rate": 1.0,
        },
    )


app = FastAPI(title=APP_NAME, description=DESCRIPTION, version=VERSION)

# For security (avoid another app to connect to this API)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins (debug, remove for production)
    allow_origins=ORIGINS,  # Allows only the frontend origin, use that for production
    allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    allow_methods=["GET", "POST"],  # Allows only GET and POST methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/sessions")
async def start_new_session(request: Request) -> dict:
    """
    Start a new game, create a session
    """
    session_uid: str = uuid.uuid4()
    connection = psycopg.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_DB,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )
    with connection:
        client_host = request.client.host
        query: str = f"INSERT INTO sessions (ip, uuid) VALUES ('{client_host}', '{session_uid}');"  # noqa E501
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
    return {"sessionUid": session_uid}


@app.get("/questions")
async def get_new_question(aggressive: Optional[bool] = None) -> dict:
    """
    Endpoint which takes a random comment from the database (human-generated or AI-generated), and sends it back along with its ID in the database.
    """

    connection = psycopg.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_DB,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )
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
        "id": question[0],
        "question": question[1],
    }


class AnswerPayload(BaseModel):
    sessionUid: str
    questionId: int
    answer: int


@app.post("/answers")
async def post_answer(body: AnswerPayload, request: Request) -> dict:
    """
    Endpoint which receives the answer from the user from the frontend, compares to the fake flag of the comment in the DB updates the score and the lives and end the game if lost
    """
    connection = psycopg.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_DB,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
    )
    with connection:
        try:
            # Get the session ID and current score
            query: str = (
                f"SELECT id, score, lives FROM sessions WHERE uuid='{body.sessionUid}';"
            )
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
                    "correct": correct,
                    "lives": 0,
                    "score": score,
                    "topScore": top_score,
                }

        cursor.close()

    return {"correct": correct, "lives": lives, "score": score}
