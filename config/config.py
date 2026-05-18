"""
E.D.I.T.H. V8 — Central Configuration
Even Dead I'm The Hero — Tony Stark's legacy AI, rebuilt.
Edit this file before first run.
"""

from pathlib import Path

# ── Identity ──────────────────────────────────────────────────────────────────
SYSTEM_NAME      = "E.D.I.T.H."
SYSTEM_VERSION   = "V8"
USER_NAME        = "Astra"
CODENAME         = "EDITH"

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR         = Path(__file__).parent.parent
DATA_DIR         = BASE_DIR / "data"
BRAIN_DIR        = DATA_DIR / "second_brain"     # drop files here to ingest
CHROMA_DIR       = DATA_DIR / "chroma_db"
LOGS_DIR         = DATA_DIR / "logs"
TASKS_DB         = DATA_DIR / "tasks" / "edith.db"
MEMORY_DB        = DATA_DIR / "edith_memory.db"
NOTES_FILE       = Path.home() / "edith_notes.txt"
TTS_MODEL_DIR    = DATA_DIR / "tts_models"

# ── Ollama ────────────────────────────────────────────────────────────────────
OLLAMA_URL       = "http://localhost:11434"
OLLAMA_TIMEOUT   = 120

MODEL_FAST       = "llama3.2:3b"          # primary fast agent
MODEL_SMART      = "qwen2.5:7b"           # deep reasoning fallback
MODEL_VISION     = "llava:7b"             # screen understanding
MODEL_CODE       = "codellama:7b"         # code tasks (load on demand)
MODEL_EMBED      = "nomic-embed-text"     # RAG embeddings

# ── Voice ─────────────────────────────────────────────────────────────────────
WHISPER_MODEL    = "base"                 # tiny | base | small
WAKE_WORD        = "hey edith"
LISTEN_SECONDS   = 6
SAMPLERATE       = 16000
TTS_ENGINE       = "piper"               # piper | kokoro | pyttsx3
PIPER_BIN        = "piper"
PIPER_MODEL      = str(TTS_MODEL_DIR / "en_US-lessac-medium.onnx")

# ── Server ────────────────────────────────────────────────────────────────────
HOST             = "0.0.0.0"
PORT             = 8888
WS_PATH          = "/ws"
ALLOWED_ORIGINS  = [
    "http://localhost",
    "http://localhost:8888",
    "http://127.0.0.1",
    "http://127.0.0.1:8888",
]

# ── RAG ───────────────────────────────────────────────────────────────────────
CHUNK_SIZE       = 400
CHUNK_OVERLAP    = 50
RETRIEVAL_K      = 4
RELEVANCE_CUTOFF = 0.65                   # cosine distance threshold

# ── Memory ────────────────────────────────────────────────────────────────────
HISTORY_TURNS    = 20

# ── Windows/WSL bridge ────────────────────────────────────────────────────────
WIN_USER         = "Astra"               # your Windows username
WIN_CMD          = "/mnt/c/Windows/System32/cmd.exe"
WIN_PS           = "/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe"

# ── Telegram ──────────────────────────────────────────────────────────────────
TELEGRAM_ENABLED   = False
TELEGRAM_TOKEN     = ""                  # from @BotFather
TELEGRAM_CHAT_ID   = ""

# ── ADB phone ─────────────────────────────────────────────────────────────────
ADB_ENABLED      = False
ADB_IP           = "192.168.1.X:5555"

# ── Automations ───────────────────────────────────────────────────────────────
BRIEFING_TIME    = "08:00"
WIND_DOWN_TIME   = "21:30"
NEWS_RSS         = "https://hnrss.org/frontpage"

# ── UI theme ──────────────────────────────────────────────────────────────────
ACCENT           = "#e8c840"             # Stark gold
ACCENT2          = "#ff4d1c"             # Iron Man red
BG               = "#04080f"

# ── Security ──────────────────────────────────────────────────────────────────
API_KEY          = ""  # Set an API key to secure the web interface
