from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.agents.agent_types import AgentType

def dummy_tool_func():
    return "Tool working correctly!"

tool = Tool(
    name="TestTool",
    func=dummy_tool_func,
    description="A simple test tool"
)

memory = ConversationBufferMemory()

llm = ChatOpenAI(temperature=0)

agent = initialize_agent(
    tools=[tool],
    llm=llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    handle_parsing_errors=True
)

response = agent.run("Run the tool.")
print(response)