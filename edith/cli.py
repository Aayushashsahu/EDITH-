"""
E.D.I.T.H. V8 — CLI Mode
Run EDITH entirely in the terminal without the HUD.
Useful for testing, low-resource mode, or SSH sessions.

Usage:
    python cli.py            # text input
    python cli.py --voice    # voice input via Whisper
"""

import asyncio
import os
import sys
import datetime
sys.path.insert(0, os.path.dirname(__file__))

from backend.agents.orchestrator import Orchestrator
from backend.memory.store import MemoryStore
from backend.voice.tts import TTSEngine
from config.config import SYSTEM_NAME, SYSTEM_VERSION, USER_NAME

# ── Colours ───────────────────────────────────────────────────────────────────
G  = "\033[92m"
Y  = "\033[93m"
C  = "\033[96m"
R  = "\033[91m"
DIM = "\033[2m"
B  = "\033[0m"
BOLD = "\033[1m"


async def broadcast(event: dict):
    """CLI broadcast — just prints state changes."""
    t = event.get("type", "")
    if t == "state":
        state = event.get("state", "")
        model = event.get("model", "")
        icons = {"thinking":"🧠","processing":"⚡","standby":"●","listening":"🎤"}
        icon  = icons.get(state, "·")
        suffix = f" [{model}]" if model else ""
        print(f"\r{DIM}{icon} {state.upper()}{suffix}...{B}         ", end="", flush=True)


async def main():
    use_voice = "--voice" in sys.argv

    print(f"\n{Y}{BOLD}")
    print("  ╔═══════════════════════════════════════════╗")
    print("  ║  E . D . I . T . H .   V 8               ║")
    print("  ║  Even Dead I'm The Hero  — CLI Mode       ║")
    print("  ╚═══════════════════════════════════════════╝")
    print(f"{B}")

    memory = MemoryStore()
    tts    = TTSEngine()
    orc    = Orchestrator(memory=memory, tts=tts, broadcast=broadcast)

    print(f"{Y}Initialising...{B}")
    await orc.init()
    print(f"\n{G}EDITH online.{B} Type your command. Say 'exit' to quit.\n")
    print(f"{DIM}Special: 'remember: <text>' | 'ingest: <filepath>' | 'clear memory' | 'status'{B}\n")

    if use_voice:
        await voice_loop(orc, tts)
    else:
        await text_loop(orc, tts)


async def text_loop(orc: Orchestrator, tts: TTSEngine):
    while True:
        try:
            query = input(f"{G}{USER_NAME}{B} › ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{Y}EDITH offline.{B}")
            break

        if not query:
            continue

        # Special commands
        if query.lower() in ["exit", "quit", "bye", "goodbye"]:
            await tts.speak_async(f"Goodbye, {USER_NAME}.")
            print(f"{Y}EDITH offline.{B}")
            break

        if query.lower() == "status":
            info = orc.sys.system_info()
            print(f"{DIM}{info}{B}")
            continue

        if query.lower() == "clear memory":
            orc.memory.clear()
            print(f"{DIM}Memory cleared.{B}")
            continue

        if query.lower().startswith("remember:"):
            text = query[9:].strip()
            orc.brain.ingest_text(text, source="cli")
            print(f"{DIM}Stored in second brain.{B}")
            continue

        if query.lower().startswith("ingest:"):
            path = query[7:].strip()
            n = await orc.brain.ingest_file(path)
            print(f"{DIM}Ingested {n} chunks from {path}.{B}")
            continue

        # Normal query
        print(f"{DIM}", end="", flush=True)
        response = await orc.handle(query)
        print(f"\r{B}", end="")
        ts = datetime.datetime.now().strftime("%H:%M")
        print(f"\n{C}{BOLD}EDITH{B} {DIM}[{ts}]{B}\n{response}\n")
        asyncio.create_task(tts.speak_async(response))


async def voice_loop(orc: Orchestrator, tts: TTSEngine):
    try:
        import whisper
        import sounddevice as sd
        import tempfile
        import os
        from scipy.io.wavfile import write as wav_write
        from config.config import WHISPER_MODEL, LISTEN_SECONDS, SAMPLERATE, WAKE_WORD
    except ImportError as e:
        print(f"{R}Voice deps missing: {e}{B}")
        print("pip install openai-whisper sounddevice scipy")
        return

    print(f"{Y}Loading Whisper ({WHISPER_MODEL})…{B}")
    model = whisper.load_model(WHISPER_MODEL)
    print(f"{G}Voice active. Say \"{WAKE_WORD.title()}\" to activate.{B}\n")

    while True:
        try:
            audio = sd.rec(int(LISTEN_SECONDS * SAMPLERATE),
                           samplerate=SAMPLERATE, channels=1, dtype="int16")
            sd.wait()
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            wav_write(tmp.name, SAMPLERATE, audio)
            result = model.transcribe(tmp.name, language="en")
            os.unlink(tmp.name)
            text = result["text"].strip().lower()

            if not text or len(text) < 3:
                continue

            if WAKE_WORD in text:
                query = text.replace(WAKE_WORD, "").strip(" ,.")
                if not query:
                    print(f"{Y}Command?{B} ", end="", flush=True)
                    audio2 = sd.rec(int(LISTEN_SECONDS * SAMPLERATE),
                                    samplerate=SAMPLERATE, channels=1, dtype="int16")
                    sd.wait()
                    tmp2 = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
                    wav_write(tmp2.name, SAMPLERATE, audio2)
                    r2 = model.transcribe(tmp2.name, language="en")
                    os.unlink(tmp2.name)
                    query = r2["text"].strip()

                if query:
                    print(f"{G}{USER_NAME}{B} [voice] › {query}")
                    response = await orc.handle(query)
                    print(f"\n{C}{BOLD}EDITH{B}\n{response}\n")
                    await tts.speak_async(response)

        except KeyboardInterrupt:
            print(f"\n{Y}EDITH offline.{B}")
            break


if __name__ == "__main__":
    asyncio.run(main())
