import httpx
from dotenv import load_dotenv
from fastapi import HTTPException, FastAPI
from app.schemas import ChatResponse, ChatRequest
from app.providers.groq import call_groq

load_dotenv()
app = FastAPI(title="Mini LLM Router")


@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def chat_completions(req: ChatRequest) -> ChatResponse:
    try:
        return await call_groq(req)
    except httpx.HTTPStatusError as e:
        raise HTTPException(502, f"Groq {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise HTTPException(502, f"Groq unreachable {e}")
        