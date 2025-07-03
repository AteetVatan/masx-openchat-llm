FROM python:3.10-slim

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

# Switch to that user
USER user
ENV HOME=/home/user
WORKDIR /home/user/app

# Set cache dirs inside user home
ENV HF_HOME=$HOME/.hf_home
ENV TRANSFORMERS_CACHE=$HOME/.cache/transformers

# Create cache directories
RUN mkdir -p $HF_HOME $TRANSFORMERS_CACHE

# Switch back to root to install dependencies
USER root
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install Python deps under user home
COPY --chown=user:user requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY --chown=user:user . .

# Expose port and switch user
EXPOSE 7860
USER user

# Entrypoint
CMD ["python", "app.py"]
