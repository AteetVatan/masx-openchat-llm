# model_loader.py
import os

# Safe fallback if ENV vars are not set (e.g., during local dev)
os.environ.setdefault("TRANSFORMERS_CACHE", "/app/cache")
os.environ.setdefault("HF_HOME", "/app/hf_home")

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "openchat/openchat-3.5-1210")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

# Load model initially on CPU
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to("cpu")
