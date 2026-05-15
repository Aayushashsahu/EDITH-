#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# E.D.I.T.H. V8 — First-time setup script
# Run once: bash scripts/setup.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e
G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[0m'; BOLD='\033[1m'

printf "${Y}${BOLD}  E.D.I.T.H. V8 — First Run Setup${B}\n\n"

# ── Check Python ────────────────────────────────────────────────────────────
printf "${Y}[1] Checking Python 3.10+...${B}\n"
python3 --version
PY=$(python3 -c "import sys; print(sys.version_info >= (3, 10))")
if [ "$PY" != "True" ]; then
  printf "${R}  Python 3.10+ required. Install via: sudo apt install python3.11${B}\n"; exit 1
fi
printf "${G}  ✓ Python OK${B}\n\n"

# ── Create virtualenv ────────────────────────────────────────────────────────
printf "${Y}[2] Creating virtual environment (.venv)...${B}\n"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip --quiet
printf "${G}  ✓ .venv created${B}\n\n"

# ── Install Python deps ──────────────────────────────────────────────────────
printf "${Y}[3] Installing Python dependencies...${B}\n"
pip install -r requirements.txt --quiet
printf "${G}  ✓ Python deps installed${B}\n\n"

# ── Install voice deps ───────────────────────────────────────────────────────
printf "${Y}[4] Installing voice dependencies...${B}\n"
pip install openai-whisper sounddevice scipy --quiet
# ALSA / PulseAudio for WSL audio
sudo apt-get install -y -q alsa-utils pulseaudio libportaudio2 ffmpeg 2>/dev/null || \
  printf "  (apt packages may need sudo — install manually if needed)\n"
printf "${G}  ✓ Voice deps installed${B}\n\n"

# ── Install Ollama ───────────────────────────────────────────────────────────
printf "${Y}[5] Checking Ollama...${B}\n"
if ! command -v ollama &>/dev/null; then
  printf "  Installing Ollama...\n"
  curl -fsSL https://ollama.com/install.sh | sh
else
  printf "  Ollama already installed.\n"
fi
printf "${G}  ✓ Ollama ready${B}\n\n"

# ── Pull models ──────────────────────────────────────────────────────────────
printf "${Y}[6] Pulling required Ollama models (this may take a while)...${B}\n"
printf "  Starting ollama serve in background...\n"
nohup ollama serve > /tmp/edith_setup_ollama.log 2>&1 & sleep 4

printf "  Pulling llama3.2:3b (primary, ~2GB)...\n"
ollama pull llama3.2:3b

printf "  Pulling nomic-embed-text (embeddings, ~270MB)...\n"
ollama pull nomic-embed-text

printf "  Optional: pull qwen2.5:7b for smarter reasoning? [y/N] "
read -r ans
if [[ "$ans" =~ ^[Yy]$ ]]; then
  ollama pull qwen2.5:7b
fi

printf "  Optional: pull llava:7b for screen vision? [y/N] "
read -r ans2
if [[ "$ans2" =~ ^[Yy]$ ]]; then
  ollama pull llava:7b
fi

printf "${G}  ✓ Models ready${B}\n\n"

# ── Create data dirs ─────────────────────────────────────────────────────────
printf "${Y}[7] Creating data directories...${B}\n"
mkdir -p data/second_brain data/tasks data/logs data/tts_models data/chroma_db
printf "${G}  ✓ Directories created${B}\n\n"

# ── WSL audio fix ────────────────────────────────────────────────────────────
printf "${Y}[8] Configuring WSL audio...${B}\n"
if grep -q "microsoft" /proc/version 2>/dev/null; then
  cat >> ~/.bashrc << 'EOF'
# EDITH V8 — WSL audio
export PULSE_SERVER=tcp:localhost:4713
export DISPLAY=:0
EOF
  printf "  Added PULSE_SERVER to ~/.bashrc — restart terminal after setup.\n"
fi
printf "${G}  ✓ Audio config done${B}\n\n"

# ── Done ─────────────────────────────────────────────────────────────────────
printf "${G}${BOLD}"
printf "  ╔══════════════════════════════════════════╗\n"
printf "  ║  Setup complete! Launch EDITH with:      ║\n"
printf "  ║  bash scripts/start.sh                   ║\n"
printf "  ║                                          ║\n"
printf "  ║  CLI mode (no browser):                  ║\n"
printf "  ║  python cli.py                           ║\n"
printf "  ╚══════════════════════════════════════════╝\n"
printf "${B}\n"
