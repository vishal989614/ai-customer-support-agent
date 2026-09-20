from fastapi import FastAPI
from pydantic import BaseModel

from agents.graph import build_support_graph


app = FastAPI(
    title="AI Customer Support Agent",
    description="AI support agent for a food delivery application",
    version="1.0.0"
)


# ==========================================
# BUILD AGENT
# ==========================================

support_agent = build_support_graph()


# ==========================================
# REQUEST MODEL
# ==========================================

class ChatRequest(BaseModel):

    question: str
    user_id: int


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def home():

    return {
        "message": "AI Customer Support Agent is running"
    }


# ==========================================
# CHAT
# ==========================================

@app.post("/chat")
def chat(
    request: ChatRequest
):

    result = support_agent.invoke(
        {
            "question": request.question,
            "user_id": request.user_id
        }
    )

    return {
    "question": request.question,
    "user_id": request.user_id,
    "capability": result.get("capability"),
    "intent": result.get("intent"),
    "order_id": result.get("order_id"),
    "restaurant_name": result.get("restaurant_name"),
    "payment_id": result.get("payment_id"),
    "ticket_id": result.get("ticket_id"),
    "new_status": result.get("new_status"),
    "answer": result.get("answer"),
    "verification": result.get("verification_result")
}