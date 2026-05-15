"""
E.D.I.T.H. V8 — Intent Router
Regex-based fast path: matches commands without spending LLM tokens.
Returns (result, handled). If handled=False → orchestrator calls LLM.
"""

import re
from backend.tools.system_control import SystemControl
from backend.tools.web_tools import WebTools
from backend.memory.brain import SecondBrain


class IntentRouter:
    def __init__(self, sys: SystemControl, web: WebTools, brain: SecondBrain):
        self.sys   = sys
        self.web   = web
        self.brain = brain

    async def route(self, q: str):
        ql = q.lower().strip()

        # ── time / date ───────────────────────────────────────────────────────
        if any(x in ql for x in ["what time","current time","what's the time","what day","today's date","what date"]):
            return self.sys.get_time(), True

        # ── system stats ──────────────────────────────────────────────────────
        if any(x in ql for x in ["system info","system status","cpu","ram usage","battery","disk space","how's my system","system health","performance"]):
            return self.sys.system_info(), True

        # ── weather ───────────────────────────────────────────────────────────
        m = re.search(r"weather(?:\s+in\s+([\w\s]+))?", ql)
        if m:
            city = (m.group(1) or "Pune").strip().rstrip("?. ")
            return await self.web.weather(city), True

        # ── search ────────────────────────────────────────────────────────────
        m = re.search(r"(?:search|google|ddg|look up|find info on|research)\s+(?:for\s+)?(.+)", ql)
        if m:
            return await self.web.ddg_search(m.group(1).strip()), True

        # ── youtube ───────────────────────────────────────────────────────────
        m = re.search(r"(?:youtube|play on youtube|yt)\s+(.+)", ql)
        if m:
            kw = m.group(1).strip().replace(" ", "+")
            return self.sys.open_url(f"https://www.youtube.com/results?search_query={kw}"), True

        # ── open url ──────────────────────────────────────────────────────────
        m = re.search(r"open\s+(https?://\S+|[\w-]+\.[\w.]{2,}[\S]*)", ql)
        if m:
            return self.sys.open_url(m.group(1)), True

        # ── open app ──────────────────────────────────────────────────────────
        m = re.search(
            r"open\s+(edge|chrome|firefox|vs\s?code|code|spotify|discord|telegram|"
            r"vlc|notepad|explorer|task\s?manager|calculator|settings|whatsapp|steam|"
            r"obs|powershell|cmd|paint|word|excel)", ql)
        if m:
            return self.sys.open_app(m.group(1)), True

        # ── close app ─────────────────────────────────────────────────────────
        m = re.search(r"(?:close|kill|quit|exit)\s+(\w[\w\s]*)", ql)
        if m:
            return self.sys.close_app(m.group(1).strip()), True

        # ── volume ────────────────────────────────────────────────────────────
        m = re.search(r"(?:set volume|volume to|volume at)\s+(\d+)", ql)
        if m:
            return self.sys.set_volume(int(m.group(1))), True
        if re.search(r"\b(mute|unmute)\b", ql):
            return self.sys.mute(), True
        if "volume up"   in ql: return self.sys.volume_up(),   True
        if "volume down" in ql: return self.sys.volume_down(), True

        # ── power management ──────────────────────────────────────────────────
        if re.search(r"\block\s*(the\s*)?(?:screen|pc|computer|system)?\b", ql):
            return self.sys.lock(), True
        if re.search(r"\bsleep\s*(mode)?\b", ql):
            return self.sys.sleep(), True
        if re.search(r"\bshutdown\b|\bturn off\b|\bpower off\b", ql):
            return self.sys.shutdown(), True
        if re.search(r"\brestart\b|\breboot\b", ql):
            return self.sys.restart(), True

        # ── screenshot ────────────────────────────────────────────────────────
        if "screenshot" in ql:
            return self.sys.screenshot(), True

        # ── files ─────────────────────────────────────────────────────────────
        m = re.search(r"(?:list|show)\s+(?:files|folder|directory)(?:\s+in\s+)?(.+)?", ql)
        if m:
            return self.sys.ls(m.group(1) or "~"), True

        m = re.search(r"read\s+(?:file\s+)?(.+\.[\w]{1,6})", ql)
        if m:
            return self.sys.read_file(m.group(1).strip()), True

        m = re.search(r"(?:run|execute|shell)\s+(?:command\s+)?(.+)", ql)
        if m:
            return self.sys.shell(m.group(1).strip()), True

        # ── notes ─────────────────────────────────────────────────────────────
        m = re.search(r"(?:note|remember|save)\s*:\s*(.+)", ql)
        if m:
            return self.sys.save_note(m.group(1).strip()), True
        if any(x in ql for x in ["show notes","read notes","my notes","what are my notes"]):
            return self.sys.read_notes(), True

        # ── second brain ingest from voice ────────────────────────────────────
        m = re.search(r"(?:remember that|learn that|store in brain|add to brain)\s+(.+)", ql)
        if m:
            self.brain.ingest_text(m.group(1).strip(), source="voice_command")
            return "Stored in your second brain, sir.", True

        # ── type text ─────────────────────────────────────────────────────────
        m = re.search(r"^type\s+(.+)$", ql)
        if m:
            return self.sys.type_text(m.group(1).strip()), True

        # ── network ───────────────────────────────────────────────────────────
        if any(x in ql for x in ["my ip","ip address","network info","hostname"]):
            return self.sys.net_info(), True

        # ── processes ─────────────────────────────────────────────────────────
        if any(x in ql for x in ["running apps","what's running","list processes","active apps"]):
            return self.sys.list_processes(), True

        # ── scrape ────────────────────────────────────────────────────────────
        m = re.search(r"(?:read|scrape|fetch|summarise)\s+(https?://\S+)", ql)
        if m:
            text = await self.web.scrape(m.group(1))
            return text[:800], True

        return None, False
