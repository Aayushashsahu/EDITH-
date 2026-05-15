"""
E.D.I.T.H. V8 — Automations
Morning briefing, evening wind-down, task nudges via APScheduler.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config.config import BRIEFING_TIME, WIND_DOWN_TIME, NEWS_RSS, USER_NAME


def setup(orchestrator, broadcast) -> AsyncIOScheduler:
    sched = AsyncIOScheduler()

    bh, bm = map(int, BRIEFING_TIME.split(":"))
    wh, wm = map(int, WIND_DOWN_TIME.split(":"))

    sched.add_job(morning_briefing, "cron", hour=bh, minute=bm,
                  args=[orchestrator, broadcast], id="briefing")
    sched.add_job(evening_reminder, "cron", hour=wh, minute=wm,
                  args=[orchestrator, broadcast], id="wind_down")
    sched.add_job(task_check, "interval", hours=1,
                  args=[orchestrator, broadcast], id="task_check")

    print(f"  [Sched]  Briefing at {BRIEFING_TIME}, wind-down at {WIND_DOWN_TIME}")
    return sched


async def morning_briefing(orchestrator, broadcast):
    weather    = await orchestrator.web.weather("Pune")
    news_items = await orchestrator.web.rss(NEWS_RSS, k=5)
    news_text  = "\n".join(f"- {n['title']}" for n in news_items)

    from backend.automations.task_manager import TaskManager
    tm   = TaskManager()
    due  = tm.due_today()
    task_text = "\n".join(f"- {t['title']}" for t in due) or "None."

    prompt = (
        f"Give {USER_NAME} a sharp 3-sentence morning briefing. "
        f"Be EDITH — intelligent, slightly sardonic.\n"
        f"Weather: {weather}\nTop news:\n{news_text}\nTasks due today:\n{task_text}"
    )
    response = await orchestrator.llm.generate(prompt)
    await broadcast({"type": "edith_message", "content": f"🌅 {response}"})
    await orchestrator.tts.speak_async(response)


async def evening_reminder(orchestrator, broadcast):
    msg = (f"Good evening, {USER_NAME}. Time to wind down. "
           f"Review your day, close your loops, and get some rest.")
    await broadcast({"type": "edith_message", "content": msg})
    await orchestrator.tts.speak_async(msg)


async def task_check(orchestrator, broadcast):
    from backend.automations.task_manager import TaskManager
    tm  = TaskManager()
    due = [t for t in tm.due_today() if not t["notified"]]
    for t in due:
        await broadcast({
            "type": "notification",
            "title": "📋 Task Due",
            "message": t["title"]
        })
        tm.mark_notified(t["id"])
