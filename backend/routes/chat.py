# routes/chat.py
from fastapi import APIRouter, Request
from backend.models.schemas import ChatRequest, ChatResponse  # updated import if needed


router = APIRouter(prefix="/chat")


@router.post("/")
def query_chat(req: ChatRequest):
    # Placeholder for LangChain query logic
    return ChatResponse(answer="This will contain the LLM's response")
