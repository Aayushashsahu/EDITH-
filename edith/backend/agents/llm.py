"""
E.D.I.T.H. V8 — Ollama async LLM + embedding client
"""

import aiohttp
import asyncio
import json
from config.config import OLLAMA_URL, OLLAMA_TIMEOUT, MODEL_FAST, MODEL_EMBED


class LLMClient:
    _close_tasks = set()

    def __init__(self):
        self.base = OLLAMA_URL
        self._session = None

    def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __del__(self):
        if self._session and not self._session.closed:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    task = loop.create_task(self.close())
                    self.__class__._close_tasks.add(task)
                    task.add_done_callback(self.__class__._close_tasks.discard)
                else:
                    loop.run_until_complete(self.close())
            except Exception:
                pass

    async def generate(self, prompt: str, model: str = MODEL_FAST,
                       temperature: float = 0.72, max_tokens: int = 512) -> str:
        payload = {
            "model":   model,
            "prompt":  prompt,
            "stream":  False,
            "options": {"temperature": temperature, "num_predict": max_tokens}
        }
        try:
            s = self._get_session()
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
            s = self._get_session()
            async with s.post(
                f"{self.base}/api/embeddings", json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as r:
                data = await r.json()
                return data.get("embedding", [])
        except Exception:
            return []

    async def is_alive(self) -> bool:
        try:
            s = self._get_session()
            async with s.get(
                f"{self.base}/api/tags",
                timeout=aiohttp.ClientTimeout(total=3)
            ) as r:
                return r.status == 200
        except Exception:
            return False

    async def list_models(self) -> list:
        try:
            s = self._get_session()
            async with s.get(f"{self.base}/api/tags") as r:
                data = await r.json()
                return [m["name"] for m in data.get("models", [])]
        except Exception:
            return []
