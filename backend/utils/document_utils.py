import os
from pathlib import Path
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

DOCS_DIR = Path("data/docs")

def load_documents_from_folder(folder_path: str | Path = DOCS_DIR):
    docs = []
    folder_path = Path(folder_path)
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            loader = PyPDFLoader(str(folder_path / file_name))
            docs.extend(loader.load())
    return docs

def split_documents(docs, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_documents(docs)
