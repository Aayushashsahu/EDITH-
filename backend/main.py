"""
E.D.I.T.H. V8 — FastAPI Backend
WebSocket real-time comms, REST API, static file serving.
Start: uvicorn backend.main:app --host 0.0.0.0 --port 8888 --reload
"""

import asyncio, json, os, sys, secrets
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.agents.orchestrator import Orchestrator
from backend.memory.store import MemoryStore
from backend.memory.brain import SecondBrain
from backend.voice.tts import TTSEngine
from backend.automations.scheduler import setup as setup_sched
from config.config import HOST, PORT, BASE_DIR, SYSTEM_NAME, SYSTEM_VERSION, API_KEY, ALLOWED_ORIGINS


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(request: Request, api_key_header: str = Security(api_key_header)):
    if not API_KEY: return True
    if request.url.path == "/" or request.url.path.startswith("/static"):
        return True
    if api_key_header and secrets.compare_digest(api_key_header, API_KEY):
        return True

    query_key = request.query_params.get("api_key")
    if query_key and secrets.compare_digest(query_key, API_KEY):
        return True
    raise HTTPException(status_code=401, detail="Unauthorized")

app = FastAPI(title=f"{SYSTEM_NAME} {SYSTEM_VERSION}", dependencies=[Depends(verify_api_key)])

app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")

# ── Shared state ──────────────────────────────────────────────────────────────
clients: list[WebSocket] = []
orc: Orchestrator = None
mem: MemoryStore  = None
tts: TTSEngine    = None
sched             = None


async def broadcast(event: dict):
    dead = []
    msg  = json.dumps(event)
    for ws in clients:
        try:
            await ws.send_text(msg)
        except Exception:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)


@app.on_event("startup")
async def startup():
    global orc, mem, tts, sched
    print(f"\n\033[93m{'═'*50}")
    print(f"  E.D.I.T.H. {SYSTEM_VERSION}  —  Even Dead I'm The Hero")
    print(f"{'═'*50}\033[0m\n")
    mem   = MemoryStore()
    tts   = TTSEngine()
    orc   = Orchestrator(memory=mem, tts=tts, broadcast=broadcast)
    await orc.init()
    sched = setup_sched(orc, broadcast)
    sched.start()
    print(f"\n\033[92m  ✓ EDITH online → http://localhost:{PORT}\033[0m\n")


@app.on_event("shutdown")
async def shutdown():
    if sched:
        sched.shutdown(wait=False)


# ── WebSocket ─────────────────────────────────────────────────────────────────
@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    query_key = ws.query_params.get("api_key")
    if API_KEY and (not query_key or not secrets.compare_digest(query_key, API_KEY)):
        await ws.close(code=1008)
        return
    await ws.accept()
    clients.append(ws)
    await ws.send_text(json.dumps({
        "type": "system",
        "content": f"{SYSTEM_NAME} {SYSTEM_VERSION} online. How can I assist you?"
    }))
    try:
        while True:
            raw  = await ws.receive_text()
            data = json.loads(raw)
            t    = data.get("type", "")

            if t == "query":
                query = data.get("content", "").strip()
                if not query:
                    continue
                await broadcast({"type": "user_message",  "content": query})
                await broadcast({"type": "state", "state": "processing"})
                response = await orc.handle(query)
                await broadcast({"type": "edith_message", "content": response})
                await broadcast({"type": "state", "state": "standby", "model": orc.model})
                asyncio.create_task(tts.speak_async(response))

            elif t == "ingest":
                text   = data.get("text", "")
                source = data.get("source", "ws")
                if text:
                    await orc.brain.ingest_text(text, source)
                    await ws.send_text(json.dumps({"type": "system", "content": "Stored in second brain."}))

            elif t == "ping":
                await ws.send_text(json.dumps({"type": "pong"}))

    except WebSocketDisconnect:
        if ws in clients:
            clients.remove(ws)


# ── REST ──────────────────────────────────────────────────────────────────────
@app.get("/")
async def serve_ui():
    return FileResponse(str(BASE_DIR / "frontend" / "templates" / "index.html"))

@app.get("/api/status")
async def status():
    stats = orc.sys.stats_dict() if orc else {}
    return {
        "online":     True,
        "model":      orc.model if orc else "loading",
        "brain_docs": orc.brain.count() if orc else 0,
        **stats
    }

@app.get("/api/history")
async def history():
    return {"messages": mem.all() if mem else []}

@app.get("/api/tasks")
async def tasks():
    from backend.automations.task_manager import TaskManager
    return {"tasks": TaskManager().list_tasks()}

@app.post("/api/tasks")
async def add_task(body: dict):
    from backend.automations.task_manager import TaskManager
    t = TaskManager().add(body.get("title",""), body.get("due",""), body.get("priority","medium"))
    return t

@app.patch("/api/tasks/{task_id}")
async def complete_task(task_id: int):
    from backend.automations.task_manager import TaskManager
    return {"result": TaskManager().complete(task_id)}

@app.post("/api/ingest")
async def ingest(body: dict):
    text   = body.get("text", "")
    source = body.get("source", "api")
    if text and orc:
        n = await orc.brain.ingest_text(text, source)
        return {"chunks": n}
    return JSONResponse({"error": "no text"}, status_code=400)

@app.get("/api/notes")
async def notes():
    return {"notes": orc.sys.read_notes() if orc else ""}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=False)
