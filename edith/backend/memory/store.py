"""
E.D.I.T.H. V8 — SQLite conversation memory
Persists across sessions, injects last N turns into every LLM prompt.
"""

import sqlite3, datetime, os
from config.config import MEMORY_DB, HISTORY_TURNS


class MemoryStore:
    def __init__(self):
        os.makedirs(os.path.dirname(str(MEMORY_DB)), exist_ok=True)
        self._init()

    def _init(self):
        with sqlite3.connect(str(MEMORY_DB)) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT, content TEXT, ts TEXT)""")
            c.commit()

    def add(self, role: str, content: str):
        with sqlite3.connect(str(MEMORY_DB)) as c:
            c.execute("INSERT INTO messages(role,content,ts) VALUES(?,?,?)",
                      (role, content, datetime.datetime.now().isoformat()))
            c.commit()

    def context(self, n: int = HISTORY_TURNS) -> str:
        with sqlite3.connect(str(MEMORY_DB)) as c:
            rows = c.execute(
                "SELECT role,content FROM messages ORDER BY id DESC LIMIT ?",
                (n * 2,)).fetchall()
        lines = [f"{'USER' if r == 'user' else 'EDITH'}: {msg}"
                 for r, msg in reversed(rows)]
        return "\n".join(lines)

    def all(self, limit: int = 120) -> list:
        with sqlite3.connect(str(MEMORY_DB)) as c:
            rows = c.execute(
                "SELECT role,content,ts FROM messages ORDER BY id DESC LIMIT ?",
                (limit,)).fetchall()
        return [{"role": r, "content": m, "ts": t} for r, m, t in reversed(rows)]

    def clear(self):
        with sqlite3.connect(str(MEMORY_DB)) as c:
            c.execute("DELETE FROM messages"); c.commit()
