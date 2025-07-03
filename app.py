"""
app.py FastAPI API for Quantized OpenChat 3.5 (GGUF) using ctransformers
"""

import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model_loader import model
import uvicorn
from ctransformers import AutoTokenizer  # Add this at the top
import time

# Logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

tokenizer = model.tokenize  # Use model's built-in tokenizer if available

# FastAPI app
app = FastAPI(
    title="masx-openchat-llm",
    description="MASX AI service exposing a quantized OpenChat-3.5 model (GGUF)",
    version="1.0.0",
)


# Request schema
class PromptRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.0


# Response schema
class ChatResponse(BaseModel):
    response: str

@app.get("/")
def root():
    return {"message": "MASX OpenChat API is running"}

@app.get("/status")
async def status():
    try:
        return {
            "status": "ok",
            "model_path": getattr(model, "model_path", "unknown"),
            "model_type": getattr(model, "model_type", "unknown"),
            "context_length": getattr(model, "context_length", "unknown"),
            "gpu_layers": getattr(model, "gpu_layers", 0),
        }
    except Exception as e:
        logger.error("Status check failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Model status check failed")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: PromptRequest):
    start_time = time.time()
    try:
        logger.info("Prompt: %s", req.prompt)

        prompt_tokens = model.tokenize(req.prompt)
        if len(prompt_tokens) > model.context_length:
            raise HTTPException(
                status_code=400,
                detail=f"Prompt too long ({len(prompt_tokens)} tokens). Max context: {model.context_length}",
            )

        response = model(
            req.prompt,
            max_new_tokens=req.max_tokens,
            temperature=req.temperature,
            stop=["</s>"],
        )
        end_time = time.time()
        logger.info("Response time: %s seconds", end_time - start_time)
        logger.info("Response: %s", response)
        return ChatResponse(response=response.strip())
    except Exception as e:
        logger.error("Chat error: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Inference failure")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=7860, log_level="info")
