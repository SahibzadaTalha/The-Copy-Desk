import asyncio
import json
import os

from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_random_exponential

from config import resolve_token_param, DEFAULT_MODEL
from models import MarketingCopy
from prompt_compiler import compile_prompt

MAX_CONCURRENT_REQUESTS = 5  # Groq free tier: 30 RPM, so 5 concurrent is safe


def _client() -> AsyncOpenAI:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY in your environment or .env file.")
    return AsyncOpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


@retry(wait=wait_random_exponential(multiplier=1, max=20), stop=stop_after_attempt(5))
async def _call_model(client, system_prompt, user_prompt, temperature, top_p, model):
    max_tokens = resolve_token_param(model, requested_tokens=400)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

async def generate_one(client, semaphore, product_name, product_description, platform, tone,
                        model=DEFAULT_MODEL, temperature_override=None):
    compiled = compile_prompt(product_description, platform, tone)
    temperature = temperature_override if temperature_override is not None else compiled["temperature"]
    async with semaphore:
        raw = await _call_model(client, compiled["system_prompt"], compiled["user_prompt"],
                                 temperature, compiled["top_p"], model)
    data = json.loads(raw)
    return MarketingCopy(
        product_name=product_name, platform=platform, tone=tone,
        headline=data.get("headline", ""), body=data.get("body", ""),
        call_to_action=data.get("call_to_action", ""), hashtags=data.get("hashtags", []) or [],
    )


async def generate_many(requests: list[dict], model: str = DEFAULT_MODEL) -> list[MarketingCopy]:
    client = _client()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    tasks = [
        generate_one(
            client, semaphore, r["product_name"], r["product_description"], r["platform"], r["tone"],
            model, r.get("temperature_override"),
        )
        for r in requests
    ]
    return await asyncio.gather(*tasks)