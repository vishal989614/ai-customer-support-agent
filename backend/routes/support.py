from fastapi import APIRouter
from pydantic import BaseModel

from rag.rag_chain import answer_question


router = APIRouter(
    prefix="/support",
    tags=["Support"]
)


class ChatRequest(BaseModel):

    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    answer = answer_question(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }