# Dockerfile (at project root)
FROM python:3.12-slim

# Update system packages
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements files
COPY agents/requirements.txt ./agents_requirements.txt
COPY frontend/requirements.txt ./frontend_requirements.txt

# Install all dependencies
RUN pip install --no-cache-dir -r agents_requirements.txt
RUN pip install --no-cache-dir -r frontend_requirements.txt

# Copy all source code
COPY agents/ ./agents/
COPY frontend/ ./frontend/
COPY menus/ ./menus/

ENV PYTHONPATH=/app

# Expose both ports (though Render typically uses one)
EXPOSE 8501

# Default to frontend (change as needed)
CMD ["streamlit", "run", "frontend/user_interface.py"]