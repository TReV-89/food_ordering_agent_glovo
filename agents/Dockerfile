FROM python:3.12-slim

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY agents/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY agents/generator_agent.py .
COPY agents/supervisor_agent.py .
COPY agents/__init__.py .
COPY agents/initialize.py .
COPY agents/retrieval_agent.py .
COPY agents/state_models.py .
COPY agents/tools.py .
COPY menus/ ./menus
# COPY user_interface.py .

# Set Python path to allow absolute imports
ENV PYTHONPATH=/app

# EXPOSE 8501

# Run supervisor agent using absolute imports
# CMD ["streamlit", "run", "user_interface.py","--server.port", "8501", "--server.address", "0.0.0.0"]