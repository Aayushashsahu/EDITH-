
# E.D.I.T.H. 
### *Even Dead I'm The Hero*

> Tony Stark's personal AI — rebuilt from scratch. 100% offline, runs on your Samsung Book 5 360 via WSL2.

---

## Stack

| Layer | Tech |
|---|---|
| **LLM** | Ollama — llama3.2:3b (fast) / qwen2.5:7b (smart) / codellama:7b (code) |
| **Vision** | llava:7b — screen understanding via screenshot |
| **Embeddings** | nomic-embed-text — local RAG |
| **Second Brain** | ChromaDB — persistent vector store |
| **Voice In** | OpenAI Whisper (local) |
| **Voice Out** | Piper neural TTS → Kokoro → pyttsx3 fallback |
| **Backend** | FastAPI + WebSocket (real-time) |
| **Frontend** | Stark-tech HUD — Exo 2 + Share Tech Mono |
| **System Control** | WSL → cmd.exe / PowerShell bridge (full Windows control) |
| **Automations** | APScheduler — morning briefing, task nudges |
| **Remote** | Telegram bot — control from phone anywhere |
| **Phone** | ADB wireless — call detection, answer, SMS |

---

## Quick Start

```bash
# 1. Clone / unzip into your WSL home
cd ~
unzip edith_v8.zip && cd edith

# 2. First-time setup (installs everything)
bash scripts/setup.sh

# 3. Launch
bash scripts/start.sh

# 4. Open HUD in browser
# → http://localhost:8888
```

---

## First Run

**Edit `config/config.py` first:**
```python
USER_NAME   = "Astra"          # your name
WIN_USER    = "Astra"          # your Windows username (for file paths)
WAKE_WORD   = "hey edith"      # change if you want
TTS_ENGINE  = "piper"          # piper | kokoro | pyttsx3
```

---

## File Structure

```
edith/
├── backend/
│   ├── main.py                  # FastAPI + WebSocket server
│   ├── agents/
│   │   ├── orchestrator.py      # central brain / router
│   │   ├── intent.py            # fast regex command matching
│   │   └── llm.py               # async Ollama client
│   ├── tools/
│   │   ├── system_control.py    # Windows + WSL system control
│   │   ├── web_tools.py         # DuckDuckGo, weather, scraping
│   │   └── screen_vision.py     # LLaVA screen understanding
│   ├── memory/
│   │   ├── brain.py             # ChromaDB second brain (RAG)
│   │   └── store.py             # SQLite conversation memory
│   ├── voice/
│   │   ├── tts.py               # Piper / Kokoro / pyttsx3
│   │   └── listener.py          # Whisper STT + wake word
│   ├── automations/
│   │   ├── scheduler.py         # morning briefing, reminders
│   │   └── task_manager.py      # SQLite tasks + NL due dates
│   └── integrations/
│       ├── telegram_bot.py      # remote phone control
│       └── adb_phone.py         # call detection, SMS
├── frontend/
│   └── templates/index.html     # Stark-tech HUD
├── config/config.py             # ALL settings here
├── cli.py                       # terminal mode (no browser)
├── scripts/
│   ├── setup.sh                 # first-time install
│   └── start.sh                 # launch EDITH
├── data/
│   └── second_brain/            # drop files here to ingest
└── requirements.txt
```

---

## Voice Setup (WSL)

WSL2 needs audio routing. Add to `~/.bashrc`:

```bash
export PULSE_SERVER=tcp:localhost:4713
```

Then install PulseAudio on Windows side:
- Download [PulseAudio for Windows](https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/Support/)
- Or use **WSLg** (Windows 11) which handles audio automatically

**Run the voice listener in a separate terminal:**
```bash
source .venv/bin/activate
python -m backend.voice.listener
```

---

## Second Brain

Drop any `.txt`, `.md`, or `.pdf` files into `data/second_brain/`.  
They auto-ingest on every startup.

**From the HUD:** click `+ BRAIN` in the comms panel to paste text directly.

**Voice command:** *"Remember that [fact/note]"*

---

## System Control Commands

| Command | What EDITH does |
|---|---|
| "Open Spotify" | Launches Spotify on Windows |
| "Search for [query]" | DuckDuckGo search in browser |
| "What's on my screen?" | LLaVA screenshot analysis |
| "Lock the screen" | Windows lock |
| "Set volume to 40" | System volume |
| "Take a screenshot" | Saves to Pictures |
| "What's the weather in Pune?" | wttr.in weather |
| "System status" | CPU / RAM / battery |
| "Note: [text]" | Saves to ~/edith_notes.txt |
| "Sleep" | Windows sleep mode |
| "Run command [cmd]" | WSL shell execution |

---

## Piper TTS Setup (best voice)

```bash
# Download piper binary
wget https://github.com/rhasspy/piper/releases/latest/download/piper_linux_x86_64.tar.gz
tar -xzf piper_linux_x86_64.tar.gz -C /usr/local/bin/

# Download voice model
mkdir -p data/tts_models
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx \
     -O data/tts_models/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json \
     -O data/tts_models/en_US-lessac-medium.onnx.json
```

---

## Telegram Remote Setup

1. Message [@BotFather](https://t.me/BotFather) on Telegram → `/newbot`
2. Copy the token
3. In `config/config.py`:
   ```python
   TELEGRAM_ENABLED = True
   TELEGRAM_TOKEN   = "your_token_here"
   TELEGRAM_CHAT_ID = "your_chat_id"  # get from @userinfobot
   ```

---

## RAM Budget (10GB WSL limit)

| Component | ~RAM |
|---|---|
| llama3.2:3b (active) | 2.2 GB |
| nomic-embed-text | 0.3 GB |
| ChromaDB + Python | 0.5 GB |
| FastAPI + deps | 0.3 GB |
| **Total fast mode** | **~3.3 GB** |
| qwen2.5:7b (when loaded) | +4.5 GB |
| llava:7b (when loaded) | +4.5 GB |

Models are loaded on demand and unloaded after 5 minutes of inactivity (Ollama default).

---

## CLI Mode

No browser needed:
```bash
python cli.py           # text input
python cli.py --voice   # voice input
```

---

*Built for Astra · EDITH V8 · WSL2 Ubuntu · Samsung Book 5 360*
=======
# E.D.I.T.H. — Even Dead I'm The Hero

**My fully offline personal AI system** — inspired by Iron Man's JARVIS.

Built from scratch as a first-year CSE student. Runs completely locally on WSL2 and gives me real-time voice + visual interaction with powerful local LLMs.

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


