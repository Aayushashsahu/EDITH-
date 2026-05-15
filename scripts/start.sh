#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# E.D.I.T.H. V8 — One-click startup
# Run from project root: bash scripts/start.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e
G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[0m'; BOLD='\033[1m'

printf "${Y}${BOLD}"
printf "  ╔══════════════════════════════════════════╗\n"
printf "  ║  E . D . I . T . H .  —  V 8            ║\n"
printf "  ║  Even Dead I'm The Hero                  ║\n"
printf "  ╚══════════════════════════════════════════╝\n"
printf "${B}\n"

# 1. Ollama
printf "${Y}[1/4] Checking Ollama...${B}\n"
if ! pgrep -x "ollama" > /dev/null 2>&1; then
  printf "      Starting ollama serve in background...\n"
  nohup ollama serve > /tmp/edith_ollama.log 2>&1 &
  sleep 3
fi
printf "${G}      ✓ Ollama running${B}\n"

# 2. Models
printf "${Y}[2/4] Verifying models...${B}\n"
ollama pull llama3.2:3b    2>/dev/null | tail -1 && printf "      ✓ llama3.2:3b\n" || true
ollama pull nomic-embed-text 2>/dev/null | tail -1 && printf "      ✓ nomic-embed-text\n" || true

# 3. Virtualenv
printf "${Y}[3/4] Environment...${B}\n"
if [ -d ".venv" ]; then
  source .venv/bin/activate
  printf "${G}      ✓ virtualenv active${B}\n"
else
  printf "      (no .venv found — using system Python)\n"
fi

# 4. Launch
printf "${Y}[4/4] Launching E.D.I.T.H. V8...${B}\n"
printf "\n${G}  ╔══════════════════════════════════════════╗"
printf "\n  ║  HUD →  http://localhost:8888             ║"
printf "\n  ║  Press Ctrl+C to shutdown EDITH            ║"
printf "\n  ╚══════════════════════════════════════════╝${B}\n\n"

python -m uvicorn backend.main:app \
  --host 0.0.0.0 \
  --port 8888 \
  --log-level warning
