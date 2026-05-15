#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# E.D.I.T.H. V8 — GitHub Publisher
# Creates the repo via GitHub API and pushes all 34 files.
#
# BEFORE RUNNING:
#   1. Go to https://github.com/settings/tokens/new
#   2. Give it a name (e.g. "edith-v8")
#   3. Tick: repo (full control) — that's all you need
#   4. Click "Generate token" and paste it below
#
# RUN:   bash push_to_github.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

# ── CONFIG — fill these in ───────────────────────────────────────────────────
GITHUB_TOKEN=""            # paste your token here (classic or fine-grained)
GITHUB_USERNAME=""         # your GitHub username  e.g. betheaayush
REPO_NAME="edith-v8"       # repo name on GitHub
REPO_DESC="E.D.I.T.H. V8 — Even Dead I'm The Hero. Personal AI assistant built on Ollama, ChromaDB, FastAPI, and a Stark-tech HUD. 100% offline, runs on WSL2."
PRIVATE=false              # true = private repo, false = public
# ─────────────────────────────────────────────────────────────────────────────

G='\033[92m'; Y='\033[93m'; R='\033[91m'; B='\033[0m'; BOLD='\033[1m'

# Validate inputs
if [ -z "$GITHUB_TOKEN" ] || [ -z "$GITHUB_USERNAME" ]; then
  printf "${R}ERROR: Set GITHUB_TOKEN and GITHUB_USERNAME at the top of this script.${B}\n"
  exit 1
fi

printf "${Y}${BOLD}"
printf "  E.D.I.T.H. V8 — GitHub Publisher\n"
printf "${B}\n"

# ── Step 1: Create the GitHub repo via API ────────────────────────────────────
printf "${Y}[1/4] Creating GitHub repository '$REPO_NAME'...${B}\n"

HTTP=$(curl -s -o /tmp/gh_create_resp.json -w "%{http_code}" \
  -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$REPO_DESC\",
    \"private\": $PRIVATE,
    \"auto_init\": false,
    \"has_issues\": true,
    \"has_wiki\": false
  }")

if [ "$HTTP" = "201" ]; then
  REPO_URL=$(python3 -c "import json; d=json.load(open('/tmp/gh_create_resp.json')); print(d['html_url'])")
  CLONE_URL=$(python3 -c "import json; d=json.load(open('/tmp/gh_create_resp.json')); print(d['clone_url'])")
  printf "${G}  ✓ Repo created: $REPO_URL${B}\n"
elif [ "$HTTP" = "422" ]; then
  printf "${Y}  Repo already exists — will push to existing repo.${B}\n"
  CLONE_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
else
  printf "${R}  API error (HTTP $HTTP):${B}\n"
  cat /tmp/gh_create_resp.json
  exit 1
fi

# ── Step 2: Configure git remote ──────────────────────────────────────────────
printf "${Y}[2/4] Configuring git remote...${B}\n"

# Embed token in URL for push auth
AUTH_URL="https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git"

git remote remove origin 2>/dev/null || true
git remote add origin "$AUTH_URL"
printf "${G}  ✓ Remote set${B}\n"

# ── Step 3: Commit ────────────────────────────────────────────────────────────
printf "${Y}[3/4] Committing all files...${B}\n"

git add -A
git diff --cached --quiet || git commit -m "🤖 Initial commit — E.D.I.T.H. V8

Even Dead I'm The Hero — complete AI assistant stack.

Stack:
- LLM: Ollama (llama3.2:3b / qwen2.5:7b / codellama)
- Vision: LLaVA screenshot understanding
- Second Brain: ChromaDB + nomic-embed-text RAG
- Voice: Whisper STT + Piper neural TTS
- Backend: FastAPI + WebSocket
- HUD: Stark-tech fullscreen interface (gold/crimson)
- System: Full Windows control from WSL2
- Automations: APScheduler briefings + task manager
- Integrations: Telegram bot + ADB phone control

100% offline. Runs on Samsung Book 5 360 / WSL2 Ubuntu."

printf "${G}  ✓ Committed${B}\n"

# ── Step 4: Push ──────────────────────────────────────────────────────────────
printf "${Y}[4/4] Pushing to GitHub...${B}\n"
git push -u origin main --force
printf "${G}  ✓ Pushed!${B}\n"

# ── Done ──────────────────────────────────────────────────────────────────────
printf "\n${G}${BOLD}"
printf "  ╔══════════════════════════════════════════════════════╗\n"
printf "  ║  EDITH V8 is live on GitHub!                        ║\n"
printf "  ║                                                      ║\n"
printf "  ║  → https://github.com/$GITHUB_USERNAME/$REPO_NAME\n"
printf "  ║                                                      ║\n"
printf "  ║  Share it. Clone it. Stark would be proud.          ║\n"
printf "  ╚══════════════════════════════════════════════════════╝\n"
printf "${B}\n"

# Clean up token from remote URL (security)
git remote set-url origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"
printf "${Y}  (Token removed from remote URL for safety)${B}\n\n"
