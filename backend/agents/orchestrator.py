"""
E.D.I.T.H. V8 — Orchestrator (Full)
Brain of EDITH: intent routing → vision → RAG → LLM with model selection.
"""

import datetime
from typing import Callable

from backend.agents.llm import LLMClient
from backend.agents.intent import IntentRouter
from backend.memory.store import MemoryStore
from backend.memory.brain import SecondBrain
from backend.tools.system_control import SystemControl
from backend.tools.web_tools import WebTools
from backend.tools.screen_vision import ScreenVision
from backend.voice.tts import TTSEngine
from config.config import (
    USER_NAME, SYSTEM_NAME, SYSTEM_VERSION,
    MODEL_FAST, MODEL_SMART, MODEL_CODE, MODEL_VISION
)

PERSONA = f"""You are {SYSTEM_NAME} {SYSTEM_VERSION} — Even Dead I'm The Hero.
You are {USER_NAME}'s personal AI system, modelled on Tony Stark's EDITH glasses AI.
Personality: razor intellect, dry wit, supremely capable, occasionally sardonic, never verbose.
Rules:
- 1-3 sentences unless depth is genuinely warranted.
- Never say "As an AI" or "I cannot" — you are EDITH, you find a way.
- If second-brain context was used, reference it naturally ("Based on your notes…").
- For code, be precise and technical. Return runnable code when asked.
- Today is {{date}}.
"""

COMPLEX_KW = [
    "explain","analyse","analyze","compare","write","summarise","summarize",
    "research","essay","plan","strategy","how does","why does","what would",
    "pros and cons","difference between","help me understand","walk me through",
    "give me a detailed","step by step",
]
CODE_KW = [
    "code","function","script","debug","refactor","write a","implement",
    "class","bug","error in","syntax","algorithm","program","fix this",
]
VISION_KW = [
    "what's on my screen","what is on my screen","read my screen",
    "describe the screen","what do you see","read this page",
    "describe the error","analyse this screen","what am i looking at",
    "screenshot analysis","read the error",
]


class Orchestrator:
    def __init__(self, memory: MemoryStore, tts: TTSEngine, broadcast: Callable):
        self.memory    = memory
        self.tts       = tts
        self.broadcast = broadcast
        self.llm       = LLMClient()
        self.brain     = SecondBrain()
        self.sys       = SystemControl()
        self.web       = WebTools()
        self.vision    = ScreenVision()
        self.router    = IntentRouter(self.sys, self.web, self.brain)
        self.model     = MODEL_FAST

    async def init(self):
        await self.brain.init()
        online = await self.llm.is_alive()
        print(f"  [LLM]    Ollama {'online ✓' if online else 'OFFLINE — start with: ollama serve'}")
        print(f"  [Brain]  {self.brain.count()} chunks indexed")
        models = await self.llm.list_models()
        print(f"  [Models] {', '.join(models) if models else 'none found — run ollama pull llama3.2:3b'}")

    # ── Main entry ────────────────────────────────────────────────────────────
    async def handle(self, query: str) -> str:
        ql = query.lower().strip()

        # 1. Screen vision fast-path
        if any(kw in ql for kw in VISION_KW):
            await self.broadcast({"type": "state", "state": "processing", "model": MODEL_VISION})
            result = await self._vision_handle(query)
            self._save(query, result)
            return result

        # 2. Deterministic tool fast-path (no LLM tokens spent)
        result, handled = await self.router.route(query)
        if handled:
            self._save(query, result)
            return result

        # 3. Pick the right model
        model = self._pick_model(ql)
        self.model = model
        await self.broadcast({"type": "state", "state": "thinking", "model": model})

        # 4. Second brain context
        brain_ctx = await self.brain.retrieve(query)

        # 5. Build augmented prompt and generate
        prompt   = self._build_prompt(query, brain_ctx)
        response = await self.llm.generate(prompt, model=model)

        self._save(query, response)
        return response

    # ── Vision ────────────────────────────────────────────────────────────────
    async def _vision_handle(self, query: str) -> str:
        ql = query.lower()
        if any(w in ql for w in ["error","exception","bug","warning","crash"]):
            return await self.vision.describe_error()
        if any(w in ql for w in ["code","script","function","class"]):
            return await self.vision.analyse_code_on_screen()
        if any(w in ql for w in ["text","read","extract","copy"]):
            return await self.vision.read_screen_text()
        return await self.vision.capture_and_describe(query)

    # ── Model selection ───────────────────────────────────────────────────────
    def _pick_model(self, ql: str) -> str:
        if any(k in ql for k in CODE_KW):
            return MODEL_CODE
        if any(k in ql for k in COMPLEX_KW) or len(ql) > 180:
            return MODEL_SMART
        return MODEL_FAST

    # ── Prompt builder ────────────────────────────────────────────────────────
    def _build_prompt(self, query: str, brain_ctx: str) -> str:
        now     = datetime.datetime.now().strftime("%A %d %B %Y · %I:%M %p")
        history = self.memory.context(n=12)
        persona = PERSONA.replace("{{date}}", now)

        brain_block = (
            f"\n\n[SECOND BRAIN — relevant from {USER_NAME}'s knowledge base]\n{brain_ctx}"
            if brain_ctx.strip() else ""
        )
        hist_block = (
            f"\n\n[RECENT CONVERSATION]\n{history}"
            if history.strip() else ""
        )

        return (
            f"{persona}"
            f"{brain_block}"
            f"{hist_block}"
            f"\n\n{USER_NAME.upper()}: {query}"
            f"\n{SYSTEM_NAME} {SYSTEM_VERSION}:"
        )

    # ── Persist ───────────────────────────────────────────────────────────────
    def _save(self, q: str, r: str):
        self.memory.add("user",      q)
        self.memory.add("assistant", r)
