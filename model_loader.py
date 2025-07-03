import os
from ctransformers import AutoModelForCausalLM

# Optional: create a local cache dir for gguf model if needed
os.environ.setdefault("HF_HOME", os.path.expanduser("~/.hf_home"))

# Load environment variables if you plan to use .env (optional)
from dotenv import load_dotenv

load_dotenv()

# Model path or name from environment, fallback to default OpenChat
MODEL_REPO = os.getenv("MODEL_REPO", "TheBloke/openchat_3.5-GGUF")
MODEL_FILE = os.getenv("MODEL_FILE", "openchat_3.5.Q4_K_M.gguf")
MODEL_TYPE = os.getenv("MODEL_TYPE", "mistral")  # OpenChat 3.5 is Mistral-compatible

# Load quantized GGUF model using ctransformers
model = AutoModelForCausalLM.from_pretrained(
    MODEL_REPO,
    model_file=MODEL_FILE,
    model_type=MODEL_TYPE,
    gpu_layers=0,
    local_files_only=False,
)
