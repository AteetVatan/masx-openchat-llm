# 🔹 Base image
FROM python:3.10-slim

# 🔹 Create Hugging Face-compliant non-root user
RUN useradd -m -u 1000 user

# 🔹 Set environment variables
ENV HOME=/home/user
ENV APP_HOME=/home/user/app
ENV HF_HOME=/home/user/.hf_home
ENV OMP_NUM_THREADS=8

# 🔹 Set working directory
WORKDIR $APP_HOME

# 🔹 Install system dependencies (root)
USER root
RUN apt-get update && apt-get install -y \
    git curl \
    && rm -rf /var/lib/apt/lists/*

# 🔹 Install Python dependencies
COPY --chown=user:user requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 🔹 Copy app code and give ownership to non-root user
COPY --chown=user:user . .

# 🔹 Ensure HF model cache dir is writable
RUN mkdir -p $HF_HOME && chown -R user:user $HF_HOME

# 🔹 Switch to non-root user (required by HF Spaces)
USER user

# 🔹 Expose the FastAPI port
EXPOSE 7860

# 🔹 Start your app
CMD ["python", "app.py"]
