# E.D.I.T.H. — Even Dead I'm The Hero

**My fully offline personal AI system** — inspired by Iron Man's JARVIS.

Built from scratch as a first-year CSE student. Runs completely locally on WSL2 and gives me real-time voice + visual interaction with powerful local LLMs.

![EDITH HUD](https://via.placeholder.com/800x400?text=EDITH+HUD+Screenshot)  
*(Add 3-4 screenshots/GIFs here after you upload them)*

## ✨ Key Features

- **Multi-Model LLM Routing** — Automatically picks between `llama3.2:3b` (fast), `qwen2.5:7b` (smart), `codellama` (code), and `llava` (vision)
- **Local RAG (Second Brain)** — Persistent memory with ChromaDB + nomic embeddings
- **Full Voice Interface** — Whisper STT + Neural TTS (Piper / Kokoro)
- **Real-time Stark HUD** — Beautiful Iron Man style frontend with WebSocket
- **System Control** — Controls Windows (open apps, volume, lock, sleep, etc.)
- **Automations** — Scheduled briefings, reminders via APScheduler
- **Remote Access** — Full control via Telegram bot from phone
- **Phone Integration** — ADB for call detection, SMS, etc.

## Tech Stack

- **Backend**: FastAPI + WebSocket
- **Frontend**: HTML/CSS/JS (Exo 2 + Share Tech Mono font)
- **AI**: Ollama, ChromaDB, Whisper, Piper TTS
- **Others**: Python, SQLite, ADB, APScheduler

## Quick Start

```bash
# Clone the repo
git clone https://github.com/Aayushashsahu/EDITH-.git
cd EDITH-/edith

# Run setup
bash scripts/setup.sh

# Start EDITH
bash scripts/start.sh
