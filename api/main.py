from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import ormar
import random
import sqlite3
from typing import Optional

from api.models import Answer, Comment


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

        # # Get a random record among all of them
        # num_records = await Comment.objects.count()
        # id = randint(1, num_records)

        # Get a random record with equal chances between real and AI
        if random.choice([True, False]):
            records = Comment.objects.filter(realness=1).fields("id")
        else:
            records = Comment.objects.filter(realness=0).fields("id")
        # Add the aggressive filter if it exists
        try:
            if aggressive:
                records = await records.filter(aggressive=1).all()
            else:
                records = await records.filter(aggressive=0).all()
        except:
            records = await records.all()
        id = random.choice([r.id for r in records])

        comment = await Comment.objects.get(id=id)

        return {
            'id': id, 
            'comment': comment.content,
            # 'realness': comment.realness, # maybe no need to send, to avoid hackers cheating :)
            'difficulty': comment.difficulty
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

    comment = await Comment.objects.get(id=questionId)

    try:
        client_host = request.client.host
        answer = await Answer.objects.create(
            answer=answerId,
            comment=comment,
            ip=client_host
        )
    except Exception as e:
        print(e)

    if answerId == comment.realness:
        return {
            'id': questionId,
            'correct': 1 # correct answer  
            }
    else:
        return {
            'id': questionId,
            'correct': 0  # 0 = wrong answer
            }
