# Base image
FROM python:3.10-slim

# Set cache envs for Transformers & HF Hub (must come before any Python install)
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/hf_home

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create cache directories (safe fallback in Docker)
RUN mkdir -p /app/cache /app/hf_home

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port (default for HF Spaces)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
