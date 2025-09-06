FROM python:3.11-slim

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY agents/ ./agents
COPY menus/ ./menus

# Set Python path to allow absolute imports
ENV PYTHONPATH=/app

# Expose backend port
EXPOSE 8000

# Run supervisor agent using absolute imports
CMD ["python", "-m", "agents.supervisor_agent"]
