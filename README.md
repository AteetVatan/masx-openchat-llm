---
title: MASX OpenChat
emoji: 🏹🏹🏹
colorFrom: indigo
colorTo: blue
sdk: docker
pinned: false
app_file: app.py
---      
       
# MASX OpenChat LLM

> **A FastAPI service that brings the OpenChat-3.5 language model to life through a clean, scalable REST API.**

## What is this?

MASX OpenChat LLM is your gateway to conversational AI powered by the state-of-the-art OpenChat-3.5 model. Think of it as your personal AI assistant that you can integrate into any application, website, or service through simple HTTP requests.

### Key Features
- **Powered by OpenChat-3.5**: Latest conversational AI model with 7B parameters

## 🚀 Quick Start

### Requirements

- **8GB+ RAM** (16GB+ recommended for optimal performance)
- **GPU with 8GB+ VRAM** (optional, but recommended for speed)

### Dependencies
   ```bash
   pip install -r requirements.txt
   ```

### Config
   ```bash
   cp env.example .env
   # Edit .env with your preferred settings
   ```

### Start the server
   ```bash
   python app.py
   ```

**That's it!** Your AI service is now running at `http://localhost:8080`

##  Use

### Basic Chat Request

```bash
curl -X POST "http://localhost:8080/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello! Can you help me write a Python function?",
    "max_tokens": 256,
    "temperature": 0.7
  }'
```

### Response Format

```json
{
  "response": "Of course! I'd be happy to help you write a Python function. What kind of function would you like to create? Please let me know what it should do, and I'll help you implement it with proper syntax and best practices."
}
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/status` | GET | Check service health and get model info |
| `/chat` | POST | Generate AI responses |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/redoc` | GET | Alternative API documentation |

### Request Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt` | string | **required** | Your input text/question |
| `max_tokens` | integer | 256 | Maximum tokens to generate |
| `temperature` | float | 0.0 | Creativity level (0.0 = deterministic, 2.0 = very creative) |

## 🔧 Configuration

The service is highly configurable through environment variables. Copy `env.example` to `.env` and customize:

### Essential Settings

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8080
LOG_LEVEL=info
```

### Advanced S

## 🐳 Docker Deployment

## 📊 Monitoring & Health

### Health Check

```bash
curl http://localhost:8080/status
```

Response:
```json
{
  "status": "ok",
  "max_tokens": 4096
}
```

### Logs

The service provides comprehensive logging:
- **Application logs**: `./logs/app.log`
- **Console output**: Real-time server logs
- **Error tracking**: Detailed error information with stack traces

## 🛠️ Development

### Project Structure

```
masx-openchat-llm/
├── app.py              # FastAPI application
├── model_loader.py     # Model loading and configuration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md          # This file
```

### Adding Features

1. **New Endpoints**: Add routes in `app.py`
2. **Model Configuration**: Modify `model_loader.py`
3. **Dependencies**: Update `requirements.txt`
4. **Environment Variables**: Add to `env.example`

---

**Made by the MASX AI **

*Ready to build the future of AI-powered applications? Start with MASX OpenChat LLM!*
