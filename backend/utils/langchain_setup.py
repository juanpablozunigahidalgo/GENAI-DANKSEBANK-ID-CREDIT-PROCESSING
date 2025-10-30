from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType

from backend.utils.tools import get_user_data_tool

def setup_agent(memory):
    llm = ChatOpenAI(temperature=0)
    tools = [get_user_data_tool]

    agent_executor = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        memory=memory,
        handle_parsing_errors=True,
        verbose=True
    )

    return agent_executor