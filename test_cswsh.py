import sys
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

sys.modules['aiohttp'] = MagicMock()
sys.modules['kokoro'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()
sys.modules['chromadb'] = MagicMock()

patch("backend.memory.store.MemoryStore", MagicMock()).start()
patch("backend.memory.brain.SecondBrain", MagicMock()).start()
patch("backend.voice.tts.TTSEngine", MagicMock()).start()
patch("backend.agents.orchestrator.Orchestrator", MagicMock()).start()
patch("fastapi.staticfiles.StaticFiles.__init__", return_value=None).start()
patch("fastapi.staticfiles.StaticFiles.__call__", new_callable=MagicMock).start()

from backend.main import app

client = TestClient(app)

def test_allowed():
    with client.websocket_connect("/ws", headers={"Origin": "http://localhost"}) as websocket:
        data = websocket.receive_text()
        assert "online" in data

def test_disallowed():
    try:
        with client.websocket_connect("/ws", headers={"Origin": "http://malicious.com"}) as websocket:
            websocket.receive_text()
        assert False, "Should have been rejected"
    except Exception as e:
        print("Rejected as expected")

if __name__ == "__main__":
    test_allowed()
    test_disallowed()
