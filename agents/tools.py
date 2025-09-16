from dotenv import load_dotenv
from langchain.tools import tool
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader, DirectoryLoader

# from .initialize import google_ef
from chromadb.utils import embedding_functions


#from chromadb import HttpClient
#import os

load_dotenv()

client = chromadb.PersistentClient(path="./database")

# collection = client.get_or_create_collection(
#      name="food_data", embedding_function=google_ef
#  )
# CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
# CHROMA_PORT = int(os.getenv("CHROMA_PORT", 8000))

# client = chromadb.HttpClient(host="chromadb", port=8000)

default_ef = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="food_data", embedding_function=default_ef
)

# menu_dir = "/app/menus"
menu_dir = "menus"

loader = DirectoryLoader(menu_dir, glob="**/*.pdf", loader_cls=PDFPlumberLoader)

docs = loader.load()

chunker = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

chunked_docs = chunker.split_documents(docs)


def documents_to_texts(docs):
    return [doc.page_content for doc in docs]


def documents_to_metadatas(docs):
    return [doc.metadata for doc in docs]


texts = documents_to_texts(chunked_docs)
metadatas = documents_to_metadatas(chunked_docs)

collection.add(
    documents=texts,
    metadatas=metadatas,
    ids=[f"id{i}" for i in range(len(chunked_docs))],
)


@tool
def rag_tool(query: str) -> str:
    """Use this tool to retrieve information from a knowledge base."""
    results = collection.query(query_texts=[query], n_results=5)
    return results


__all__ = ["rag_tool"]
