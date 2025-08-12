import openai
import os, time, datetime, requests
from fastapi import HTTPException
from src.core.config import (
    get_openai_key,
    get_openai_admin_key,
)  # or get_api_key, whichever you’re using
from src.core.logger import setup_logger

logger = setup_logger()


class AIService:
    def __init__(self):
        openai.api_key = get_openai_key()
        self.openapi_api_admin_key = get_openai_admin_key()

    async def generate_chat(
        self, prompt: str, model: str = "gpt-4.1-nano", temperature: float = 0.7
    ) -> dict:
        """
        Sends `prompt` to OpenAI and returns a dict with:
          - `response`: the assistant's text
          - `usage`: { prompt_tokens, completion_tokens, total_tokens }
        """
        if not prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        try:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as e:
            # wrap any API error as HTTPException for the router to catch
            raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")

        # Extract the reply and usage metrics
        content = resp.choices[0].message.content
        usage = {
            "prompt_tokens": resp.usage.prompt_tokens,
            "completion_tokens": resp.usage.completion_tokens,
            "total_tokens": resp.usage.total_tokens,
        }

        return {"response": content, "usage": usage}

    async def get_balance(self) -> dict:
        """
        Returns month-to-date spend (USD) using the Costs API.
        """
        try:
            headers = {"Authorization": f"Bearer {self.openapi_api_admin_key}"}
            # First day of the current month (UTC) – OpenAI usage/costs use Unix seconds.
            today_utc = datetime.datetime.utcnow()
            start_of_month = int(
                datetime.datetime(today_utc.year, today_utc.month, 1).timestamp()
            )

            params = {"start_time": start_of_month, "bucket_width": "1d", "limit": 31}
            r = requests.get(
                "https://api.openai.com/v1/organization/costs",
                headers=headers,
                params=params,
                timeout=10,
            )
            r.raise_for_status()
            payload = r.json()
            buckets = payload.get("data", [])
            mtd_usd = 0.0
            for bucket in buckets:
                for res in bucket.get("results", []):
                    amt = res.get("amount", {}).get("value", 0.0)
                    mtd_usd += float(amt or 0)
            return {
                "billing_mode": "postpaid_or_prepaid",
                "month_to_date_spend_usd": round(mtd_usd, 6),
            }
        except requests.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"OpenAI Costs API error: {e.response.status_code} {e.response.text}",
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch spend: {e}")
