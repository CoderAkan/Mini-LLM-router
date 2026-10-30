import os
import httpx
from app.schemas import ChatRequest, ChatResponse

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-oss-20b"


async def call_groq(request: ChatRequest) -> ChatResponse: 
    dict_request = request.model_dump(exclude_none=True)
    if dict_request["model"] == "auto":
        dict_request["model"] = DEFAULT_MODEL
    headers = {
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(headers=headers, url=GROQ_URL, json=dict_request)
        response.raise_for_status()
        converted_response = ChatResponse.model_validate(response.json())
    return converted_response


# if __name__ == "__main__":
#     import asyncio
#     from dotenv import load_dotenv
#     load_dotenv()

#     req = ChatRequest(messages=[{"role": "user", "content": "Say hi in Kazakh"}])
#     print(asyncio.run(call_groq(req)))

#     req2 = ChatRequest(model="openai/gpt-oss-120b",
#                        messages=[{"role": "user", "content": "Say hi in Kazakh"}])
#     print(asyncio.run(call_groq(req2)))