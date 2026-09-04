from fastapi import FastAPI

from config import settings
from routes.support import router as support_router

app = FastAPI(
    title="AI Customer Support Agent"
)

app.include_router(
    support_router
)


@app.get("/")
def root():
    return {
        "message": "AI Customer Support Agent API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }