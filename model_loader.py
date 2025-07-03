import os
from dotenv import load_dotenv
from ctransformers import AutoModelForCausalLM

# Optional: Set Hugging Face cache dir
os.environ.setdefault("HF_HOME", os.path.expanduser("~/.hf_home"))

# Load variables from .env if available
load_dotenv()

# === High-Precision GGUF Model Configuration ===
MODEL_REPO = os.getenv("MODEL_REPO", "TheBloke/openchat-3.5-0106-GGUF")
MODEL_FILE = os.getenv("MODEL_FILE", "openchat-3.5-0106.Q8_0.gguf")
MODEL_TYPE = os.getenv("MODEL_TYPE", "mistral")  # OpenChat 3.5 is Mistral-compatible
CTX_LEN = int(os.getenv("CTX_LEN", "8192"))  # Use full 8K context

# === Load Model ===
model = AutoModelForCausalLM.from_pretrained(
    MODEL_REPO,
    model_file=MODEL_FILE,
    model_type=MODEL_TYPE,
    context_length=CTX_LEN,
    gpu_layers=0,
    local_files_only=False,
)
