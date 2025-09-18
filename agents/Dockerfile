FROM python:3.12-slim

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY generator_agent.py .
COPY supervisor_agent.py .
COPY __init__.py .
COPY initialize.py .
COPY retriever_agent.py .
COPY state_models.py .
COPY tools.py .
COPY user_interface.py .
COPY menus/ ./menus

# Set Python path to allow absolute imports
ENV PYTHONPATH=/app

EXPOSE 8501

# Run supervisor agent using absolute imports
CMD ["streamlit", "run", "user_interface.py","--server.port", "8501", "--server.address", "0.0.0.0"]