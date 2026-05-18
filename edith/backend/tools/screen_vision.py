"""
E.D.I.T.H. V8 — Screen Vision
Uses LLaVA to understand what's on screen. Called when user says
"what's on my screen", "read this page", "describe the error", etc.
"""

import asyncio
import base64
import os
import subprocess
import tempfile
import datetime
import aiohttp
from pathlib import Path
from config.config import OLLAMA_URL, MODEL_VISION, OLLAMA_TIMEOUT, WIN_USER


class ScreenVision:

    async def capture_and_describe(self, prompt: str = "Describe what is on the screen in detail.") -> str:
        """Take a screenshot and ask LLaVA to describe it."""
        path = await self._capture()
        if not path or not os.path.exists(path):
            return "Could not capture screen."
        description = await self._ask_llava(path, prompt)
        return description

    async def read_screen_text(self) -> str:
        return await self.capture_and_describe(
            "Extract and list all visible text on the screen, preserving layout where possible."
        )

    async def describe_error(self) -> str:
        return await self.capture_and_describe(
            "Is there any error message, warning, or exception visible on screen? "
            "If so, describe it precisely and suggest what might be causing it."
        )

    async def analyse_code_on_screen(self) -> str:
        return await self.capture_and_describe(
            "There is code visible on screen. Identify the language, describe what it does, "
            "and note any obvious bugs or improvements."
        )

    # ── Internal ──────────────────────────────────────────────────────────────
    async def _capture(self) -> str | None:
        """Capture screen via PowerShell and return path to PNG."""
        ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        win  = f"C:\\Users\\{WIN_USER}\\AppData\\Local\\Temp\\edith_vision_{ts}.png"
        wsl  = win.replace("C:\\", "/mnt/c/").replace("\\", "/")

        ps = (
            "Add-Type -AssemblyName System.Windows.Forms,System.Drawing;"
            "$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds;"
            "$bmp=New-Object System.Drawing.Bitmap($b.Width,$b.Height);"
            "$g=[System.Drawing.Graphics]::FromImage($bmp);"
            "$g.CopyFromScreen($b.Location,[System.Drawing.Point]::Empty,$b.Size);"
            f"$bmp.Save('{win}');"
        )
        try:
            from config.config import WIN_PS
            subprocess.run([WIN_PS, "-NoProfile", "-Command", ps],
                           capture_output=True, timeout=15)
            await asyncio.sleep(0.5)
            return wsl if os.path.exists(wsl) else None
        except Exception as e:
            print(f"[Vision] Capture failed: {e}")
            return None

    async def _ask_llava(self, image_path: str, prompt: str) -> str:
        """Send image to LLaVA via Ollama and return description."""
        try:
            with open(image_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
        except Exception as e:
            return f"Could not read image: {e}"

        payload = {
            "model":  MODEL_VISION,
            "prompt": prompt,
            "images": [img_b64],
            "stream": False,
            "options": {"num_predict": 512}
        }
        try:
            async with aiohttp.ClientSession() as s:
                async with s.post(
                    f"{OLLAMA_URL}/api/generate", json=payload,
                    timeout=aiohttp.ClientTimeout(total=OLLAMA_TIMEOUT)
                ) as r:
                    data = await r.json()
                    return data.get("response", "").strip()
        except aiohttp.ClientConnectorError:
            return "LLaVA unavailable — run: ollama pull llava:7b"
        except Exception as e:
            return f"Vision error: {e}"
