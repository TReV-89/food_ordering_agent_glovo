# Dockerfile (at project root)
FROM python:3.12-slim


WORKDIR /app

RUN pip install chromadb

RUN mkdir -p /app/chromadb_data

EXPOSE 8000 

CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8000", "--path", "/app/chromadb_data"]