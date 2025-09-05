
FROM python:3.11-slim

# Update system packages to reduce vulnerabilities and remove unnecessary packages
RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY agents/ ./agents
COPY menus/ ./menus

# Expose backend port
EXPOSE 8000

# Run supervisor (entrypoint)
CMD ["python", "agents/supervisor_agent.py"]
