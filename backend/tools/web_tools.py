"""
E.D.I.T.H. V8 — Web Tools
DuckDuckGo search (no API key), wttr.in weather, page scraping, RSS.
"""

import aiohttp
import urllib.parse
import asyncio
from bs4 import BeautifulSoup


class WebTools:
    _close_tasks = set()

    def __init__(self):
        self._session = None

    def _get_session(self):
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    def __del__(self):
        if self._session and not self._session.closed:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    task = loop.create_task(self.close())
                    self.__class__._close_tasks.add(task)
                    task.add_done_callback(self.__class__._close_tasks.discard)
                else:
                    loop.run_until_complete(self.close())
            except Exception:
                pass

    async def ddg_search(self, query: str, k: int = 5) -> str:
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        hdr = {"User-Agent": "Mozilla/5.0 (EDITH-V8)"}
        try:
            s = self._get_session()
            async with s.get(url, headers=hdr,
                             timeout=aiohttp.ClientTimeout(total=10)) as r:
                html = await r.text()
            soup    = BeautifulSoup(html, "html.parser")
            results = soup.select(".result__body")[:k]
            if not results:
                return f"No results for '{query}'."
            lines = [f"Search: {query}"]
            for item in results:
                t = item.select_one(".result__title")
                s = item.select_one(".result__snippet")
                title   = t.get_text(strip=True) if t else "—"
                snippet = s.get_text(strip=True)[:180] if s else ""
                lines.append(f"• {title} — {snippet}")
            return "\n".join(lines)
        except Exception as e:
            return f"Search error: {e}"

    async def weather(self, city: str = "Pune") -> str:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3"
        try:
            s = self._get_session()
            async with s.get(url, headers={"User-Agent": "curl/7.68.0"},
                             timeout=aiohttp.ClientTimeout(total=8)) as r:
                return (await r.text()).strip()
        except Exception as e:
            return f"Weather unavailable: {e}"

    async def scrape(self, url: str, max_chars: int = 3000) -> str:
        if not url.startswith("http"):
            url = "https://" + url
        try:
            s = self._get_session()
            async with s.get(url, headers={"User-Agent": "Mozilla/5.0"},
                             timeout=aiohttp.ClientTimeout(total=12)) as r:
                html = await r.text()
            soup = BeautifulSoup(html, "html.parser")
            for tag in soup(["script","style","nav","footer","header","aside"]):
                tag.decompose()
            import re
            text = re.sub(r"\s{2,}", " ", soup.get_text(" ", strip=True))
            return text[:max_chars]
        except Exception as e:
            return f"Scrape failed: {e}"

    async def rss(self, url: str, k: int = 5) -> list:
        try:
            s = self._get_session()
            async with s.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                xml = await r.text()
            soup  = BeautifulSoup(xml, "xml")
            items = []
            for i in soup.find_all("item")[:k]:
                items.append({
                    "title": i.find("title").get_text(strip=True) if i.find("title") else "",
                    "desc":  i.find("description").get_text(strip=True)[:160] if i.find("description") else "",
                    "link":  i.find("link").get_text(strip=True) if i.find("link") else "",
                })
            return items
        except Exception as e:
            return [{"title": f"RSS error: {e}", "desc": "", "link": ""}]
