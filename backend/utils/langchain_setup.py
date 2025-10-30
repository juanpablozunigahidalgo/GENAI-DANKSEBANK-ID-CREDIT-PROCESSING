from pathlib import Path
from dotenv import load_dotenv  # ✅ para leer variables desde .env
from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from backend.utils.document_utils import load_documents_from_folder, split_documents

# 🔹 Cargar variables de entorno (.env)
load_dotenv()

FAISS_DIR = Path("data/faiss")

# cache en memoria para no cargar FAISS en cada request
_vectorstore_cache = None

def build_vectorstore():
    """Leer PDFs, trocearlos y crear/sobre-escribir FAISS en disco."""
    docs = load_documents_from_folder()
    chunks = split_documents(docs)
    embeddings = OpenAIEmbeddings()  # Usará OPENAI_API_KEY desde .env
    vs = FAISS.from_documents(chunks, embeddings)
    FAISS_DIR.mkdir(parents=True, exist_ok=True)
    vs.save_local(str(FAISS_DIR))
    return vs

def load_vectorstore():
    """Cargar FAISS desde disco (con cache en memoria)."""
    global _vectorstore_cache
    if _vectorstore_cache is None:
        embeddings = OpenAIEmbeddings()
        _vectorstore_cache = FAISS.load_local(
            str(FAISS_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
    return _vectorstore_cache
