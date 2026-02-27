"""
Zhipu AI (Z.ai) API Client for OpenCLAW Nebula-Physicist.
Uses GLM-4/GLM-5 models.
"""

import os
import time
import jwt
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

# Key format: "id.secret"
ZAI_API_KEY = os.getenv("ZAI_API_KEY", "")

def generate_token(apikey: str, exp_seconds: int = 3600):
    try:
        id, secret = apikey.split(".")
    except Exception:
        raise ValueError("Invalid ZAI_API_KEY format. Expected 'id.secret'")

    payload = {
        "api_key": id,
        "exp": int(time.time()) + exp_seconds,
        "timestamp": int(time.time()),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )

async def complete(
    messages: list,
    max_tokens: int = 4000,
    temperature: float = 0.7,
    fast: bool = False,
) -> str:
    """
    Asynchronous completion using Zhipu AI (Open API v4).
    """
    if not ZAI_API_KEY:
        raise RuntimeError("ZAI_API_KEY not found in environment.")

    token = generate_token(ZAI_API_KEY)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Using glm-4 as a powerful stable baseline
    payload = {
        "model": "glm-4",
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    async with httpx.AsyncClient(timeout=120.0) as client:
        for attempt in range(3):
            try:
                r = await client.post(url, headers=headers, json=payload)
                
                if r.status_code == 429:
                    await asyncio.sleep(20 * (attempt + 1))
                    continue
                    
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"].strip()
                
            except Exception as e:
                if attempt == 2:
                    raise RuntimeError(f"Zhipu AI API failed: {e}")
                await asyncio.sleep(5 * (attempt + 1))

    raise RuntimeError("Zhipu AI: retries exhausted")
