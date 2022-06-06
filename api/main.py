from datetime import datetime

import asyncio
import aiomysql
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from typing import Optional, Tuple
import uuid

from settings import DATABASE_DB,DATABASE_HOST, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_USER

loop = asyncio.get_event_loop()

app = FastAPI()

# For security (avoid another app to connect to this API)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # Allows all origins (debug, remove for production)
    allow_origins=[
        "http://localhost:8888",
        "http://artificial-non-intelligence.netlify.app",
        "https://artificial-non-intelligence.netlify.app/",
        "http://artificial-non-intelligence.herokuapp.com",
        "https://artificial-non-intelligence.herokuapp.com",
        "http://www.artificial-non-intelligence.me",
        "https://www.artificial-non-intelligence.me",
    ],  # Allows only the frontend origin, use that for production
    allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    allow_methods=["GET", "POST"],  # Allows only GET and POST methods
    allow_headers=["*"],  # Allows all headers
)


async def get_db_connection():
    return await aiomysql.connect(
        host=DATABASE_HOST,
        port=int(DATABASE_PORT),
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        db=DATABASE_DB,
        loop=loop,
    )

@app.post("/sessions")
async def start_new_session(request: Request) -> dict:
    """
    Start a new game, create a session
    """
    session_uid: str = uuid.uuid4()
    conn = await get_db_connection()
    client_host = request.client.host
    async with conn.cursor() as cursor:
        await cursor.execute(
            f"INSERT INTO sessions (ip, uuid) VALUES ('{client_host}', '{session_uid}');"
        )
        await conn.commit()
        # print(cursor.description)
    conn.close()
    return {"sessionUid": session_uid}


@app.get("/questions")
async def get_new_question(aggressive: Optional[bool] = None) -> dict:
    """
    Endpoint which takes a random comment from the database (human-generated or AI-generated), and sends it back along with its ID in the database.
    """
    conn = await get_db_connection()
    real: int = random.choice([0, 1])
    if type(aggressive) == bool:
        aggressive_int = 1 if aggressive else 0
        query: str = f"SELECT id, content FROM questions WHERE `real`={real} AND `aggressive`={aggressive_int} ORDER BY RAND() LIMIT 1;"

    else:
        query: str = f"SELECT id, content FROM questions WHERE `real`={real} ORDER BY RAND() LIMIT 1;"
    async with conn.cursor() as cursor:
        await cursor.execute(query)
        # print(cursor.description)
        question: Tuple = await cursor.fetchone()
    conn.close()
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
    # print(body)

    conn = await get_db_connection()
    
    async with conn.cursor() as cursor:
        try:
            # Get the session ID and current score
            query: str = (
                f"SELECT id, score, lives FROM sessions WHERE `uuid`='{body.sessionUid}';"
            )
            await cursor.execute(query)
            session: Tuple = await cursor.fetchone()
            # print(session)
            session_id: int = session[0]
            score: int = session[1]
            lives: int = session[2]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Session does not exist")

        try:
            # Get the question
            query: str = f"SELECT id, `real` FROM questions WHERE id={body.questionId};"
            await cursor.execute(query)
            question: Tuple = await cursor.fetchone()
            question_id: int = question[0]
            real: int = question[1]
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="Question does not exist")

        try:
            # Add answer to the DB
            client_host = request.client.host
            query: str = f"INSERT INTO answers (answer, question_id, ip, session_id) VALUES ({body.answer}, {question_id}, '{client_host}', {session_id});"
            await cursor.execute(query)
            await conn.commit()
        except Exception as e:
            print(e)

        if body.answer == real:
            # Update the session with the score +1
            correct = 1
            score += 1
            query: str = f"UPDATE sessions SET score={score} WHERE `id`={session_id};"
            await cursor.execute(query)
            await conn.commit()
        else:
            correct = 0
            lives = lives - 1
            if lives > 0:
                # Update the session with the lives -1
                query: str = f"UPDATE sessions SET lives={lives} WHERE `id`={session_id};"
                await cursor.execute(query)
                await conn.commit()
            else:
                # End the session and get the top score
                ended = datetime.utcnow()
                query: str = f"UPDATE sessions SET lives=0, ended='{ended}' WHERE `id`={session_id};"
                await cursor.execute(query)
                await conn.commit()
                query: str = f"SELECT MAX(score) FROM sessions;"
                await cursor.execute(query)
                response = await cursor.fetchone()
                top_score: int = response[0]
                return {
                    "correct": correct,
                    "lives": 0,
                    "score": score,
                    "topScore": top_score,
                }

    conn.close()

    return {"correct": correct, "lives": lives, "score": score}
