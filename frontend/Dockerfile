# frontend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend code
COPY frontend/ ./frontend

# Expose frontend port)
EXPOSE 8501

# Run frontend app
CMD ["python", "frontend/user_interface.py"]
