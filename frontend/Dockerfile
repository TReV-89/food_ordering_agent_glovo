# frontend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY agents/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy both frontend and agents code
COPY frontend/user_interface.py .
COPY agents/ ./agents


# Set Python path for imports
ENV PYTHONPATH=/app

# Expose frontend port
EXPOSE 8501

# Run frontend app
CMD ["streamlit", "run", "user_interface.py"]
