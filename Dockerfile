# Use official Python slim image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libzbar0 build-essential && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Optional: Expose a port for documentation
EXPOSE 8000

# Environment variable default (Render will override)
ENV PORT 8000

# Start FastAPI using $PORT dynamically
ENTRYPOINT ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
