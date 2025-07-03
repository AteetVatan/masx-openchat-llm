# Base image
FROM python:3.10-slim

# Create non-root user (required for Hugging Face Spaces)
RUN useradd -m -u 1000 user

# Set paths
ENV HOME=/home/user
ENV APP_HOME=$HOME/app
ENV HF_HOME=$HOME/.hf_home

# Use app directory
WORKDIR $APP_HOME

# Switch to root for system setup
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY --chown=user:user . .

# Ensure cache directories exist and are user-writable
RUN mkdir -p $HF_HOME && chown -R user:user $HF_HOME

# Set to non-root user (required for HF Spaces)
USER user

# Expose default port
EXPOSE 7860

# Entrypoint
CMD ["python", "app.py"]
