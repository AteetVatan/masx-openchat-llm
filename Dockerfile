# Base image
FROM python:3.10-slim

# Set cache envs for Transformers & HF Hub (must come before any Python install)
ENV HF_HOME=/data/hf_home
ENV TRANSFORMERS_CACHE=/data/cache

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose port (default for HF Spaces)
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
