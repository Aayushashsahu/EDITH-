"""
E.D.I.T.H. V8 — Task Manager
SQLite tasks with natural language due date parsing.
"""

import sqlite3
import datetime
import os
import re
from config.config import TASKS_DB


class TaskManager:
    def __init__(self):
        os.makedirs(os.path.dirname(str(TASKS_DB)), exist_ok=True)
        self._init()

    def _init(self):
        with sqlite3.connect(str(TASKS_DB)) as c:
            c.execute("""CREATE TABLE IF NOT EXISTS tasks(
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                title    TEXT,
                due      TEXT,
                priority TEXT DEFAULT 'medium',
                done     INTEGER DEFAULT 0,
                notified INTEGER DEFAULT 0,
                created  TEXT)""")
            c.commit()

    def add(self, title: str, due_str: str = None, priority: str = "medium") -> dict:
        due = self._parse_due(due_str) if due_str else None
        ts  = datetime.datetime.now().isoformat()
        with sqlite3.connect(str(TASKS_DB)) as c:
            cur = c.execute(
                "INSERT INTO tasks(title,due,priority,created) VALUES(?,?,?,?)",
                (title, due, priority, ts))
            c.commit()
            return {"id": cur.lastrowid, "title": title, "due": due}

    def list_tasks(self, done: bool = False) -> list:
        with sqlite3.connect(str(TASKS_DB)) as c:
            rows = c.execute(
                "SELECT id,title,due,priority,done FROM tasks WHERE done=? ORDER BY due ASC",
                (1 if done else 0,)).fetchall()
        return [{"id":r[0],"title":r[1],"due":r[2],"priority":r[3],"done":bool(r[4])} for r in rows]

    def complete(self, task_id: int) -> str:
        with sqlite3.connect(str(TASKS_DB)) as c:
            c.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,)); c.commit()
        return f"Task {task_id} marked complete."

    def due_today(self) -> list:
        today = datetime.date.today().isoformat()
        with sqlite3.connect(str(TASKS_DB)) as c:
            rows = c.execute(
                "SELECT id,title,due,priority,notified FROM tasks WHERE done=0 AND due<=?",
                (today,)).fetchall()
        return [{"id":r[0],"title":r[1],"due":r[2],"priority":r[3],"notified":bool(r[4])} for r in rows]

    def mark_notified(self, task_id: int):
        with sqlite3.connect(str(TASKS_DB)) as c:
            c.execute("UPDATE tasks SET notified=1 WHERE id=?", (task_id,)); c.commit()

    def _parse_due(self, text: str) -> str | None:
        t = text.lower().strip()
        today = datetime.date.today()
        if "today"     in t: return today.isoformat()
        if "tomorrow"  in t: return (today + datetime.timedelta(1)).isoformat()
        if "next week" in t: return (today + datetime.timedelta(7)).isoformat()
        days = {"monday":0,"tuesday":1,"wednesday":2,"thursday":3,"friday":4,"saturday":5,"sunday":6}
        for name, wd in days.items():
            if name in t:
                ahead = (wd - today.weekday()) % 7 or 7
                return (today + datetime.timedelta(ahead)).isoformat()
        m = re.search(r"in\s+(\d+)\s+days?", t)
        if m:
            return (today + datetime.timedelta(int(m.group(1)))).isoformat()
        m = re.search(r"(\d{4}-\d{2}-\d{2})", t)
        if m:
            return m.group(1)
        return None
