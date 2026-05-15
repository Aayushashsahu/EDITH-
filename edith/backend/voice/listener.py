"""
E.D.I.T.H. V8 — Voice Listener
Whisper STT with wake word detection. Sends queries to backend via WebSocket.
Run standalone: python -m backend.voice.listener
"""

import asyncio, json, os, sys, tempfile
import websockets
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../"))
from config.config import WHISPER_MODEL, WAKE_WORD, LISTEN_SECONDS, SAMPLERATE, PORT


def record_and_transcribe(model, sd, wav_write):
    audio = sd.rec(int(LISTEN_SECONDS * SAMPLERATE),
                   samplerate=SAMPLERATE, channels=1, dtype="int16")
    sd.wait()
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wav_write(tmp.name, SAMPLERATE, audio)
    result = model.transcribe(tmp.name, language="en")
    os.unlink(tmp.name)
    return result["text"].strip()


async def run():
    try:
        import whisper
        import sounddevice as sd
        import numpy as np
        from scipy.io.wavfile import write as wav_write
    except ImportError as e:
        print(f"[Listener] Missing dep: {e}")
        print("  pip install openai-whisper sounddevice scipy numpy")
        return

    print(f"[Listener] Loading Whisper ({WHISPER_MODEL})…")
    model = whisper.load_model(WHISPER_MODEL)
    print(f"[Listener] Ready. Say \"{WAKE_WORD.title()}\" to activate.")

    async with websockets.connect(f"ws://localhost:{PORT}/ws") as ws:
        print("[Listener] Connected to EDITH backend.")
        while True:
            # Capture audio
            text = record_and_transcribe(model, sd, wav_write).lower()

            if not text or len(text) < 3:
                continue

            print(f"[Heard] {text}")

            if WAKE_WORD in text:
                query = text.replace(WAKE_WORD, "").strip(" ,.")
                if not query:
                    # listen again for the actual command
                    print("[Listener] Wake word detected — command?")
                    query = record_and_transcribe(model, sd, wav_write)

                if query:
                    print(f"[Sending] {query}")
                    await ws.send(json.dumps({"type": "query", "content": query}))
                    try:
                        resp = await asyncio.wait_for(ws.recv(), timeout=90)
                        data = json.loads(resp)
                        if data.get("type") == "edith_message":
                            print(f"[EDITH] {data['content']}")
                    except asyncio.TimeoutError:
                        print("[Listener] Response timeout.")


if __name__ == "__main__":
    asyncio.run(run())
