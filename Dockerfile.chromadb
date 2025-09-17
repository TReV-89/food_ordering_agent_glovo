FROM python:3.12-slim

WORKDIR /app

RUN pip install chromadb

# Create data directory
RUN mkdir -p /app/chroma_data

EXPOSE 8000

CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8000", "--path", "/app/chroma_data"]