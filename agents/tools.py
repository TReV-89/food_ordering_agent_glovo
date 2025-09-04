from langchain.tools import tool
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
from .initialize import google_ef


client = chromadb.PersistentClient(path="./food_ordering_agent_glovo/database")

collection = client.get_or_create_collection(
    name="food_data", embedding_function=google_ef
)

docs = PDFPlumberLoader(
    "/Users/trevorsaaka/Desktop/Timepledge projects/food_ordering_agent_glovo/data/takeoutstar.com_order_printer_restaurant_82943.pdf"
).load()

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
    smallest_distance = results["distances"][0][0]

    if smallest_distance < 0.6:
        response = "\n".join([doc.strip() for doc in results["documents"][0]])
        return response
    return "No relevant information found."


@tool
def calculate_final_fee(delivery_fee: float, price: float) -> str:
    """Use this tool to calculate the final fee by adding delivery fee and price of the menu item."""
    return f"UGX {delivery_fee + price}"


final_fee = calculate_final_fee

__all__ = ["rag_tool", "final_fee"]
