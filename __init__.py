from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("api_key")
model = os.getenv("model")

llm = ChatGoogleGenerativeAI(
    model=model, google_api_key=api_key, temperature=0.5, max_tokens=None
)
