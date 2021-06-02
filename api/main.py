from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import ormar
from random import randint

from api.models import Comment


app = FastAPI()

# For security (avoid another app to connect to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    # allow_origins=[
    #     "http://localhost",
    #     "http://127.0.0.1",
    #     "http://artificial-non-intelligence.herokuapp.com"
    # ],
    allow_credentials=True,
    # allow_methods=["*"],  # Allows all methods
    allow_methods=["GET"],  # Allows only GET method
    allow_headers=["*"],  # Allows all headers
)


@app.get('/get-random-comment')
async def get_random_comment():
        """
        Endpoint which takes a random comment from the database (human-generated or AI-generated), and sends it back along with its ID in the database.
        """

        num_records = await Comment.objects.count()

        #np.random.seed(42)   ## optional to set
        id = randint(1, num_records)
        comment = await Comment.objects.get(id=id)

        return {
            'id': id, 
            'comment': comment.content,
            # 'realness': comment.realness, # maybe no need to send, to avoid hackers cheating :)
            'difficulty': comment.difficulty
            } 


@app.get('/verify-answer')
async def verify_answer(questionId: int, answer: int):
    """
    Endpoint which receives the answer from the user from the frontend, compares to the fake flag of the comment in the DB, and answers if it was a good or bad answer.
    """

    content = await Comment.objects.get(id=questionId)
    realness: int = content.realness
    
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
