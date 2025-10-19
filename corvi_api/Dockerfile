FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install itsdangerous

# Copy all files
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Simple startup
CMD ["python", "-m", "uvicorn", "app_simple:app", "--host", "0.0.0.0", "--port", "8000"]