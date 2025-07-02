"""
This is the main file for the OpenChat-3.5 LLM API.
-model_loader.py file to load the model and tokenizer.
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import tokenizer, model
import uvicorn
import torch

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI app
app = FastAPI(
    title="masx-openchat-llm",
    description="MASX AI service exposing the OpenChat-3.5 LLM as an inference endpoint",
    version="1.0.0"
)

# Request ********schema*******
class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.0  # Deterministic by default

# Response ********schema*******
class ChatResponse(BaseModel):
    response: str

@app.get("/status")
async def status():
    """Check model status and max supported tokens."""
    try:
        max_context = getattr(model.config, "max_position_embeddings", "unknown")
        return {"status": "ok", "model": model.name_or_path, "max_context_tokens": max_context}
    except Exception as e:
        logger.error("Status error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(req: PromptRequest):
    """OpenChat-3.5 Run inference prompt"""
    try:
        logger.info("Received prompt: %s", req.prompt)

        # Dynamically choose device at request time
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {device}")
        
        # Move model to device if not 
        if next(model.parameters()).device != device:
            logger.info("Moving model to %s", device)
            model.to(device)
        
        # Tokenize input
        inputs = tokenizer(req.prompt, return_tensors="pt").to(device)

        # Generation parameters
        gen_kwargs = {
            "max_new_tokens": req.max_tokens,
            "temperature": req.temperature,
            "do_sample": req.temperature > 0,
        }

        # Generate output
        outputs = model.generate(**inputs, **gen_kwargs)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Trim echoed prompt if present
        response_text = generated_text[len(req.prompt):].strip()

        logger.info("Generated response: %s", response_text)
        return ChatResponse(response=response_text)

    except Exception as e:
        logger.error("Inference failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Inference failure: " + str(e))

if __name__ == "__main__":    
    uvicorn.run("app:app", host="0.0.0.0", port=8080, log_level="info")
