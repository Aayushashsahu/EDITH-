"""
E.D.I.T.H. V8 — SQLite conversation memory
Persists across sessions, injects last N turns into every LLM prompt.
"""

import sqlite3
import datetime
import os
from config.config import MEMORY_DB, HISTORY_TURNS


class MemoryStore:
    def __init__(self):
        os.makedirs(os.path.dirname(str(MEMORY_DB)), exist_ok=True)
        # Use a single persistent connection with WAL mode to avoid connection overhead
        # check_same_thread=False allows access from different async workers
        self._conn = sqlite3.connect(str(MEMORY_DB), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._init()

    def __del__(self):
        if hasattr(self, '_conn'):
            self._conn.close()

    def _init(self):
        self._conn.execute("""CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT, content TEXT, ts TEXT)""")
        self._conn.commit()

    def add(self, role: str, content: str):
        self._conn.execute("INSERT INTO messages(role,content,ts) VALUES(?,?,?)",
                  (role, content, datetime.datetime.now().isoformat()))
        self._conn.commit()

    def context(self, n: int = HISTORY_TURNS) -> str:
        rows = self._conn.execute(
            "SELECT role,content FROM messages ORDER BY id DESC LIMIT ?",
            (n * 2,)).fetchall()
        lines = [f"{'USER' if r == 'user' else 'EDITH'}: {msg}"
                 for r, msg in reversed(rows)]
        return "\n".join(lines)

    def all(self, limit: int = 120) -> list:
        rows = self._conn.execute(
            "SELECT role,content,ts FROM messages ORDER BY id DESC LIMIT ?",
            (limit,)).fetchall()
        return [{"role": r, "content": m, "ts": t} for r, m, t in reversed(rows)]

    def clear(self):
        self._conn.execute("DELETE FROM messages")
        self._conn.commit()
