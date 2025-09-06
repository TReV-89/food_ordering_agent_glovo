from langchain.tools import tool
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader, DirectoryLoader
from .initialize import google_ef
from chromadb import HttpClient
import os

client = chromadb.PersistentClient(path="./database")

collection = client.get_or_create_collection(
    name="food_data", embedding_function=google_ef
)
# CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
# CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# client = HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

# collection = client.get_or_create_collection(
#     name="food_data", embedding_function=google_ef
# )

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
    results = collection.query(query_texts=[query], n_results=5, include=["distances"])
    filtered_docs = []
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        if distance <= 1.0:
            filtered_docs.append(doc.strip())

    # Return filtered results or a message if no relevant results found
    if filtered_docs:
        return "\n".join(filtered_docs)


__all__ = ["rag_tool"]
