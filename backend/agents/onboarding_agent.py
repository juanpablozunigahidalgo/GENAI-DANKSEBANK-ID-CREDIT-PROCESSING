from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import ChatPromptTemplate  # Optional, can remove if unused
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool


# Simulated tool to fetch ID-verified user info
def fetch_user_info():
    return "User: John Doe, CPR: 123456-7890, verified for Denmark."


get_user_data_tool = Tool(
    name="GetVerifiedUser",
    func=fetch_user_info,
    description="Use this only AFTER the user has uploaded their ID to retrieve their verified data."
)

# System prompt guiding agent behaviour
system_prompt = """
You are a professional, courteous agent at Danske Bank, assigned to assist users with onboarding and credit-related questions.

You MUST always:
1. Greet the user and ask how you can help with credit onboarding.
2. Politely request a government-issued ID (PDF or image) if not already provided.
3. ONLY provide personalized advice once ID has been uploaded and verified.
4. Refuse to answer questions unrelated to credit or account onboarding.

Remain compliant, helpful, and concise.
"""

# Initialize conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the agent
llm = ChatOpenAI(temperature=0, model="gpt-4")

agent_executor = initialize_agent(
    tools=[get_user_data_tool],
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True
)

def run_onboarding_agent(user_query: str):
    return agent_executor.run(user_query)
