"""
E.D.I.T.H. V8 — TTS Engine
Priority: Piper (neural, offline) → Kokoro → pyttsx3 (fallback)
"""

import asyncio
import os
import re
import subprocess
from config.config import TTS_ENGINE, PIPER_BIN, PIPER_MODEL


class TTSEngine:
    def __init__(self):
        self._pyttsx = None
        self._kokoro_pipe = None
        print(f"  [TTS]    Engine: {TTS_ENGINE}")

    def speak(self, text: str):
        text = self._clean(text)
        if not text:
            return
        if TTS_ENGINE == "piper":
            self._piper(text)
        elif TTS_ENGINE == "kokoro":
            self._kokoro(text)
        else:
            self._pyttsx3(text)

    async def speak_async(self, text: str):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.speak, text)

    def _piper(self, text: str):
        if not os.path.exists(PIPER_MODEL):
            print(f"  [TTS]    Piper model not found: {PIPER_MODEL}")
            self._pyttsx3(text)
            return
        try:
            proc = subprocess.Popen(
                [PIPER_BIN, "--model", PIPER_MODEL, "--output-raw"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            raw, _ = proc.communicate(input=text.encode())
            player = subprocess.Popen(
                ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-"],
                stdin=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            player.communicate(input=raw)
        except FileNotFoundError:
            self._pyttsx3(text)

    def _kokoro(self, text: str):
        try:
            from kokoro import KPipeline
            import sounddevice as sd

            # ⚡ Bolt: Cache the Kokoro pipeline model to avoid re-initializing
            # weights and config for every utterance, significantly reducing latency.
            if self._kokoro_pipe is None:
                self._kokoro_pipe = KPipeline(lang_code="a")

            for _, _, audio in self._kokoro_pipe(text, voice="af_heart"):
                sd.play(audio, 24000)
                sd.wait()
        except Exception:
            self._pyttsx3(text)

    def _pyttsx3(self, text: str):
        try:
            if self._pyttsx is None:
                import pyttsx3
                self._pyttsx = pyttsx3.init()
                self._pyttsx.setProperty("rate", 172)
                for v in self._pyttsx.getProperty("voices"):
                    if "english" in v.name.lower():
                        self._pyttsx.setProperty("voice", v.id)
                        break
            self._pyttsx.say(text)
            self._pyttsx.runAndWait()
        except Exception as e:
            print(f"  [TTS]    pyttsx3 error: {e}")

    def _clean(self, text: str) -> str:
        text = re.sub(r"[*_`#>~]", "", text)
        text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text[:600]
