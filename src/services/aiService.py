import openai
from fastapi import HTTPException
from src.core.config import get_openapi_key


class AIService:
    def __init__(self):
        openai.api_key = get_openapi_key()

    async def generate_chat(
        self, prompt: str, model: str = "gpt-4.1-nano", temp: float = 0.7
    ) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temp,
            )
            return resp.choices[0].message.content
        except Exception as e:
            # wrap any API error as HTTPException for the router to catch
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
