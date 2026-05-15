"""
E.D.I.T.H. V8 — Ollama async LLM + embedding client
"""

import aiohttp
import asyncio
import json
from config.config import OLLAMA_URL, OLLAMA_TIMEOUT, MODEL_FAST, MODEL_EMBED


class LLMClient:
    def __init__(self):
        self.base = OLLAMA_URL

    async def generate(self, prompt: str, model: str = MODEL_FAST,
                       temperature: float = 0.72, max_tokens: int = 512) -> str:
        payload = {
            "model":   model,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": temperature, "num_predict": max_tokens}
        }
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(
                    f"{self.base}/api/generate", json=payload,
                    timeout=aiohttp.ClientTimeout(total=OLLAMA_TIMEOUT)
                ) as r:
                    data = await r.json()
                    return data.get("response", "").strip()
        except aiohttp.ClientConnectorError:
            return "EDITH offline — Ollama not running. Start with: ollama serve"
        except asyncio.TimeoutError:
            return "Request timed out. Try a smaller model or shorter query."
        except Exception as e:
            return f"LLM error: {e}"

    async def embed(self, text: str, model: str = MODEL_EMBED) -> list:
        payload = {"model": model, "prompt": text}
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(
                    f"{self.base}/api/embeddings", json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as r:
                    data = await r.json()
                    return data.get("embedding", [])
        except aiohttp.ClientError as e:
            print(f"[LLM] Embed network error: {e}")
            return []
        except asyncio.TimeoutError as e:
            print(f"[LLM] Embed timeout error: {e}")
            return []
        except Exception as e:
            print(f"[LLM] Embed unexpected error: {e}")
            return []

    async def is_alive(self) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(
                    f"{self.base}/api/tags",
                    timeout=aiohttp.ClientTimeout(total=3)
                ) as r:
                    return r.status == 200
        except aiohttp.ClientError as e:
            print(f"[LLM] is_alive network error: {e}")
            return False
        except asyncio.TimeoutError as e:
            print(f"[LLM] is_alive timeout error: {e}")
            return False
        except Exception as e:
            print(f"[LLM] is_alive unexpected error: {e}")
            return False

    async def list_models(self) -> list:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(f"{self.base}/api/tags") as r:
                    data = await r.json()
                    return [m["name"] for m in data.get("models", [])]
        except aiohttp.ClientError as e:
            print(f"[LLM] list_models network error: {e}")
            return []
        except asyncio.TimeoutError as e:
            print(f"[LLM] list_models timeout error: {e}")
            return []
        except Exception as e:
            print(f"[LLM] list_models unexpected error: {e}")
            return []
