from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

from backend.utils.tools import get_user_data_tool, search_docs_tool

SYSTEM_PROMPT = """
You are an onboarding assistant for Danske Bank (Cloud AI Bank scenario).
Your job is to:
1. Greet the user.
2. Ask what country they are onboarding from.
3. Ask for identification documents according to the country rules.
4. If the user has ALREADY uploaded ID, you may call GetVerifiedUser to confirm.
5. Use SearchBusinessProcedures to answer questions about country-specific requirements (Denmark, Sweden, Norway, Finland).
6. If the question is NOT about onboarding, KYC, credit onboarding, or branch routing, politely refuse.

Be concise and compliant.
"""

# 👇 ESTE prompt ya incluye el agent_scratchpad que pide LangChain
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    # historial de conversación
    MessagesPlaceholder(variable_name="chat_history"),
    # lo que pregunta el usuario
    ("human", "{input}"),
    # espacio para que el agente escriba llamadas a tools
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# memoria
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
)

llm = ChatOpenAI(temperature=0, model="gpt-4")

tools = [get_user_data_tool, search_docs_tool]

agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    handle_parsing_errors=True,
    verbose=True,
)

def run_onboarding_agent(user_query: str) -> str:
    result = agent_executor.invoke({"input": user_query})
    return result["output"]
