from fastapi import APIRouter
from backend.models.schemas import ChatRequest, ChatResponse
from backend.agents.onboarding_agent import run_onboarding_agent

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/")
def query_chat(req: ChatRequest) -> ChatResponse:
    answer = run_onboarding_agent(req.query)
    return ChatResponse(answer=answer)
