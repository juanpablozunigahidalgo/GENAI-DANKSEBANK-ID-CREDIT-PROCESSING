from langchain.tools import Tool
from backend.utils.langchain_setup import load_vectorstore

# 1) tool para leer usuario verificado (mock)
def fetch_user_info():
    # aquí podrías leer de una base o de algo que llenaste en /upload-id
    return "User: John Doe, CPR: 123456-7890, verified for Denmark."

get_user_data_tool = Tool(
    name="GetVerifiedUser",
    func=fetch_user_info,
    description="Use this only AFTER the user has uploaded their ID to retrieve their verified data."
)

# 2) tool para buscar en los documentos (appendix)
def search_procedure(query: str):
    try:
        vs = load_vectorstore()
    except Exception:
        return "Knowledge base not ready. Please ingest the PDF documents first."
    docs = vs.similarity_search(query, k=4)
    return "\n\n".join([d.page_content for d in docs])

search_docs_tool = Tool(
    name="SearchBusinessProcedures",
    func=search_procedure,
    description="Use this to answer questions about required documents, branches, or country-specific onboarding rules."
)
