# backend/agents/onboarding_agent.py
from typing import Dict
import json
from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from backend.utils.tools import (
    get_user_data_tool,
    search_docs_tool,
    get_uploaded_id_tool,
    UPLOADED_IDS,
)

# ---------------------------------------------------------------------
# 1) In-memory conversation store (per user/session)
# ---------------------------------------------------------------------
USER_MEMORIES: Dict[str, ConversationBufferMemory] = {}

# ---------------------------------------------------------------------
# 2) Simple JSON “DB” for customers
# ---------------------------------------------------------------------
CUSTOMERS_DB = Path("data/customers.json")
CUSTOMERS_DB.parent.mkdir(parents=True, exist_ok=True)


def save_customer_persistently(data: dict):
    """Append customer data to a local JSON file (POC)."""
    existing = []
    if CUSTOMERS_DB.exists():
        existing = json.loads(CUSTOMERS_DB.read_text(encoding="utf-8"))
    existing.append(data)
    CUSTOMERS_DB.write_text(json.dumps(existing, indent=2), encoding="utf-8")


def get_memory_for_user(user_id: str) -> ConversationBufferMemory:
    """Get or create the memory object for this user/session."""
    if user_id not in USER_MEMORIES:
        USER_MEMORIES[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
    return USER_MEMORIES[user_id]


# ---------------------------------------------------------------------
# 3) Base system prompt
# ---------------------------------------------------------------------
SYSTEM_PROMPT = """
You are an onboarding assistant for Danske Bank (Cloud AI Bank scenario).

Your scope INCLUDES:
- onboarding new customers,
- KYC / identity verification,
- collecting and validating Nordic ID documents,
- preparing the customer for a CREDIT / LENDING / LOAN request,
- answering questions about required documents for loans in Denmark, Sweden, Norway, and Finland,
- telling the user when they are ready to be redirected to the lending/credit agent.

Your task is to:
1. Detect the user language from the last message and answer in that language (but English is OK if unsure).
2. If the user asks for a loan / credit / mortgage / consumer loan, CONTINUE the flow (do NOT refuse). Explain that you need to verify identity first.
3. Ask what country they are onboarding from.
4. Ask for identification documents according to the country rules.
5. If the user has ALREADY uploaded ID, you may call GetUploadedId or GetVerifiedUser to confirm.
6. Use SearchBusinessProcedures to answer questions about country-specific requirements (Denmark, Sweden, Norway, Finland).
7. When the user is fully identified and VERIFIED BY THE NATIONAL REGISTRY, tell them they have been registered and that they will be redirected to another agent.

Only refuse if the user asks for something clearly OUTSIDE banking/onboarding/credit.
Be concise and compliant.
"""


# ---------------------------------------------------------------------
# 4) Build prompt for a specific user_id
# ---------------------------------------------------------------------
def build_prompt_for_user(user_id: str) -> ChatPromptTemplate:
    """Include user_id context directly in the prompt."""
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", f"User ID: {user_id}\nUser message: {{input}}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])


# ---------------------------------------------------------------------
# 5) Shared LLM + tools
# ---------------------------------------------------------------------
llm = ChatOpenAI(temperature=0, model="gpt-4")

tools = [
    get_user_data_tool,
    search_docs_tool,
    get_uploaded_id_tool,
]


def build_onboarding_agent(memory: ConversationBufferMemory, user_id: str) -> AgentExecutor:
    """Build an agent for a specific user_id."""
    prompt = build_prompt_for_user(user_id)
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt,
    )
    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        handle_parsing_errors=True,
        verbose=True,
    )
    return executor


# ---------------------------------------------------------------------
# 6) Main entrypoint called from /chat
# ---------------------------------------------------------------------
def run_onboarding_agent(user_query: str, user_id: str) -> str:
    """
    Run the onboarding agent for a specific user_id so the chat history
    is kept per user/session. When finished, persist and clear RAM.
    """
    # 1) get or create memory
    memory = get_memory_for_user(user_id)

    # 2) build agent for this session
    executor = build_onboarding_agent(memory, user_id)

    # 3) execute query
    try:
        result = executor.invoke({"input": user_query})
    except Exception as e:
        return f"[agent-error] {type(e).__name__}: {e}"

    output = result["output"]
    text = output.lower()

    # -----------------------------------------------------------------
    # 4) detect registration / completion phrases
    # -----------------------------------------------------------------
    trigger_phrases = [
        "you are being redirected",
        "you will be redirected",
        "redirected to our lending/credit agent",
        "you have been registered",
        "you're registered",
        "estás registrado",
        "identity has been successfully verified",
        "identity verified",
    ]

    if any(t in text for t in trigger_phrases):
        user_data = UPLOADED_IDS.get(user_id)
        generated_email = None

        if user_data:
            # ✅ NEW: read verification result that was produced by the independent engine
            verification = user_data.get("verification", {}) or {}
            v_status = verification.get("status", "pending")

            # if verification failed → DO NOT REGISTER
            if v_status != "approved":
                reason = verification.get("reason", "Verification not successful.")
                # don't clear memory; let user re-upload
                output += (
                    f" Note: we could not verify your ID against the national registry. "
                    f"Reason: {reason}. Please re-upload your ID or contact support."
                )
                return output

            # ✅ verification approved → proceed to registration
            first = user_data.get("first_name", "").lower().replace(" ", "")
            last = user_data.get("last_name", "").lower().replace(" ", "")
            if first and last:
                generated_email = f"{first}.{last}@danskebank.credit.com"

            user_data_to_save = {
                **user_data,
                "email": generated_email,
                "registered_user_id": user_id,
                "verification": verification,
            }
            save_customer_persistently(user_data_to_save)

            # now we can clear memory
            USER_MEMORIES.pop(user_id, None)
            UPLOADED_IDS.pop(user_id, None)

            if generated_email:
                output += f" Your temporary Danske Bank credit user is: {generated_email}"
            else:
                output += " Registration completed, but no email was generated."

        else:
            # edge: agent thought we were done but no ID in memory
            output += " However, I could not find your uploaded ID. Please upload it again."

    return output
