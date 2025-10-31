from fastapi import APIRouter
from backend.models.schemas import ChatRequest, ChatResponse
from backend.agents.onboarding_agent import (
    run_onboarding_agent,
    USER_MEMORIES,
    get_memory_for_user,   # 👈 import this
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
def query_chat(req: ChatRequest) -> ChatResponse:
    user_id = req.user_id or "anonymous"

    # 👇 First time this user_id appears
    if user_id not in USER_MEMORIES:
        # create the memory so that on the next call the agent will run
        get_memory_for_user(user_id)
        welcome_message = "How can I help you in regards to Credit at Danske Bank?"
        return ChatResponse(answer=welcome_message)

    # 👇 From the second message on, run the full agent
    answer = run_onboarding_agent(req.query, user_id)
    return ChatResponse(answer=answer)
