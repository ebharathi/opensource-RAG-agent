FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for llama-cpp-python and other packages
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create models directory if it doesn't exist
RUN mkdir -p models

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
