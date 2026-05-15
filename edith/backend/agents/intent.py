"""
E.D.I.T.H. V8 — Intent Router
Regex-based fast path: matches commands without spending LLM tokens.
Returns (result, handled). If handled=False → orchestrator calls LLM.
"""

import re
import inspect
from backend.tools.system_control import SystemControl
from backend.tools.web_tools import WebTools
from backend.memory.brain import SecondBrain


class IntentRouter:
    def __init__(self, sys: SystemControl, web: WebTools, brain: SecondBrain):
        self.sys   = sys
        self.web   = web
        self.brain = brain

        # Pre-compile intent regexes to avoid compiling on every query
        self.handlers = [
            # Exact matches / keywords are checked via functions, regexes via search
            (
                lambda ql: any(x in ql for x in ["what time","current time","what's the time","what day","today's date","what date"]),
                lambda ql, m: self.sys.get_time()
            ),
            (
                lambda ql: any(x in ql for x in ["system info","system status","cpu","ram usage","battery","disk space","how's my system","system health","performance"]),
                lambda ql, m: self.sys.system_info()
            ),
            (
                re.compile(r"weather(?:\s+in\s+([\w\s]+))?"),
                self._handle_weather
            ),
            (
                re.compile(r"(?:search|google|ddg|look up|find info on|research)\s+(?:for\s+)?(.+)"),
                lambda ql, m: self.web.ddg_search(m.group(1).strip())
            ),
            (
                re.compile(r"(?:youtube|play on youtube|yt)\s+(.+)"),
                self._handle_youtube
            ),
            (
                re.compile(r"open\s+(https?://\S+|[\w-]+\.[\w.]{2,}[\S]*)"),
                lambda ql, m: self.sys.open_url(m.group(1))
            ),
            (
                re.compile(
                    r"open\s+(edge|chrome|firefox|vs\s?code|code|spotify|discord|telegram|"
                    r"vlc|notepad|explorer|task\s?manager|calculator|settings|whatsapp|steam|"
                    r"obs|powershell|cmd|paint|word|excel)"),
                lambda ql, m: self.sys.open_app(m.group(1))
            ),
            (
                re.compile(r"(?:close|kill|quit|exit)\s+(\w[\w\s]*)"),
                lambda ql, m: self.sys.close_app(m.group(1).strip())
            ),
            (
                re.compile(r"(?:set volume|volume to|volume at)\s+(\d+)"),
                lambda ql, m: self.sys.set_volume(int(m.group(1)))
            ),
            (
                re.compile(r"\b(mute|unmute)\b"),
                lambda ql, m: self.sys.mute()
            ),
            (
                lambda ql: "volume up" in ql,
                lambda ql, m: self.sys.volume_up()
            ),
            (
                lambda ql: "volume down" in ql,
                lambda ql, m: self.sys.volume_down()
            ),
            (
                re.compile(r"\block\s*(the\s*)?(?:screen|pc|computer|system)?\b"),
                lambda ql, m: self.sys.lock()
            ),
            (
                re.compile(r"\bsleep\s*(mode)?\b"),
                lambda ql, m: self.sys.sleep()
            ),
            (
                re.compile(r"\bshutdown\b|\bturn off\b|\bpower off\b"),
                lambda ql, m: self.sys.shutdown()
            ),
            (
                re.compile(r"\brestart\b|\breboot\b"),
                lambda ql, m: self.sys.restart()
            ),
            (
                lambda ql: "screenshot" in ql,
                lambda ql, m: self.sys.screenshot()
            ),
            (
                re.compile(r"(?:list|show)\s+(?:files|folder|directory)(?:\s+in\s+)?(.+)?"),
                lambda ql, m: self.sys.ls(m.group(1) or "~")
            ),
            (
                re.compile(r"read\s+(?:file\s+)?(.+\.[\w]{1,6})"),
                lambda ql, m: self.sys.read_file(m.group(1).strip())
            ),
            (
                re.compile(r"(?:run|execute|shell)\s+(?:command\s+)?(.+)"),
                lambda ql, m: self.sys.shell(m.group(1).strip())
            ),
            (
                re.compile(r"(?:note|remember|save)\s*:\s*(.+)"),
                lambda ql, m: self.sys.save_note(m.group(1).strip())
            ),
            (
                lambda ql: any(x in ql for x in ["show notes","read notes","my notes","what are my notes"]),
                lambda ql, m: self.sys.read_notes()
            ),
            (
                re.compile(r"(?:remember that|learn that|store in brain|add to brain)\s+(.+)"),
                self._handle_brain_ingest
            ),
            (
                re.compile(r"^type\s+(.+)$"),
                lambda ql, m: self.sys.type_text(m.group(1).strip())
            ),
            (
                lambda ql: any(x in ql for x in ["my ip","ip address","network info","hostname"]),
                lambda ql, m: self.sys.net_info()
            ),
            (
                lambda ql: any(x in ql for x in ["running apps","what's running","list processes","active apps"]),
                lambda ql, m: self.sys.list_processes()
            ),
            (
                re.compile(r"(?:read|scrape|fetch|summarise)\s+(https?://\S+)"),
                self._handle_scrape
            ),
        ]

    async def _handle_weather(self, ql, m):
        city = (m.group(1) or "Pune").strip().rstrip("?. ")
        return await self.web.weather(city)

    def _handle_youtube(self, ql, m):
        kw = m.group(1).strip().replace(" ", "+")
        return self.sys.open_url(f"https://www.youtube.com/results?search_query={kw}")

    async def _handle_brain_ingest(self, ql, m):
        await self.brain.ingest_text(m.group(1).strip(), source="voice_command")
        return "Stored in your second brain, sir."

    async def _handle_scrape(self, ql, m):
        text = await self.web.scrape(m.group(1))
        return text[:800]

    async def route(self, q: str):
        ql = q.lower().strip()

        for matcher, handler in self.handlers:
            if hasattr(matcher, "search"):
                # It's a compiled regex
                m = matcher.search(ql)
                if m:
                    res = handler(ql, m)
                    if inspect.isawaitable(res):
                        res = await res
                    return res, True
            else:
                # It's a function/lambda taking the string
                if matcher(ql):
                    res = handler(ql, None)
                    if inspect.isawaitable(res):
                        res = await res
                    return res, True

        return None, False
