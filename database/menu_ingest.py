import os
import re
import fitz  # PyMuPDF for PDF text extraction
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


# 1. PDF Text Extraction
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text



# 2. Extract Menu Items

def extract_menu_items(text):
    items = []
    lines = text.splitlines()

    # Handles prices with dots, commas, UGX, /=, $, etc.
    pattern = re.compile(
        r"^(?P<dish>[A-Za-z0-9\s\-\&]+?)\s*(?:[.\-–\s]*)\s*(?P<price>(UGX\s*)?[\d,]+(?:\.\d{2})?(?:\/=| USD|\$)?)$",
        re.IGNORECASE
    )

    for line in lines:
        line = line.strip()
        if not line:
            continue  # skip empty lines

        match = pattern.search(line)
        if match:
            dish = match.group("dish").strip()
            price = match.group("price").strip()
            print(f"Matched: {dish} -> {price}")  # Debug log
            items.append({"dish": dish, "price": price})
        else:
            print(f" No match: {line}")  # Debug log

    return items




# Setup ChromaDB

def setup_chroma_db():
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    persist_directory = os.path.join(os.path.dirname(__file__), "chroma_db")

    collection = Chroma(
        collection_name="restaurant_menus",
        embedding_function=embedding_model,
        persist_directory=persist_directory
    )
    return collection


# Store Items in ChromaDB

def store_in_chroma(items, collection, restaurant, path):
    docs = []
    for item in items:
        page_content = f"{item['dish']} - {item.get('price', 'N/A')}"  # Always include dish + price
        docs.append(
            Document(
                page_content=page_content,
                metadata={
                    "restaurant": restaurant,
                    "dish": item.get("dish"),
                    "price": item.get("price"),
                    "source": path,
                },
            )
        )

    if docs:
        collection.add_documents(docs)
        print(f"Added {len(docs)} items from {restaurant} to ChromaDB.")



# 5. Main Pipeline

if __name__ == "__main__":
    folder = "menus"
    collection = setup_chroma_db()

    if not os.path.exists(folder):
        print(f"Folder '{folder}' not found.")
        exit(1)

    for pdf_file in os.listdir(folder):
        if pdf_file.endswith(".pdf"):
            path = os.path.join(folder, pdf_file)
            restaurant = os.path.splitext(pdf_file)[0]  # filename = restaurant name

            print(f"Processing {restaurant}...")
            text = extract_text_from_pdf(path)
            items = extract_menu_items(text)
            store_in_chroma(items, collection, restaurant, path)

    print(" All menus ingested into ChromaDB!")
