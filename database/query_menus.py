from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os

# 1. Load ChromaDB
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
persist_directory = os.path.join(os.path.dirname(__file__), "chroma_db")

vectorstore = Chroma(
    collection_name="restaurant_menus",
    embedding_function=embedding_model,
    persist_directory=persist_directory
)


print("Collections available:", vectorstore._collection.name)
print("Number of items:", vectorstore._collection.count())

# 2. Run a Query
def query_menus(query, k=5):
    results = vectorstore.similarity_search(query, k=k)

    if not results:
        print("No results found.")
    else:
        for r in results:
            meta = r.metadata
            print(f"{meta.get('restaurant')} | {meta.get('dish')} | {meta.get('price')}")
            print(f"{r.page_content}\n")

if __name__ == "__main__":
    query = "chicken"  
    query_menus(query, k=5)
