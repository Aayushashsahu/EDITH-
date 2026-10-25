import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocketDisconnect
import sys

# Mocking missing dependencies as instructed by memory
sys.modules['aiohttp'] = MagicMock()
sys.modules['kokoro'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()
sys.modules['chromadb'] = MagicMock()

# Need to mock the agent dependencies as well so we can test the main.py
patch("backend.memory.store.MemoryStore", MagicMock()).start()
patch("backend.memory.brain.SecondBrain", MagicMock()).start()
patch("backend.voice.tts.TTSEngine", MagicMock()).start()
patch("backend.agents.orchestrator.Orchestrator", MagicMock()).start()

# Mock fastap StaticFiles mount check
patch("fastapi.staticfiles.StaticFiles.__init__", return_value=None).start()
patch("fastapi.staticfiles.StaticFiles.__call__", new_callable=MagicMock).start()


from edith.backend.main import app, verify_api_key

class TestCors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        app.dependency_overrides[verify_api_key] = lambda: True

    def tearDown(self):
        app.dependency_overrides = {}

    def test_cors_allowed_origin(self):
        # We test that an allowed origin gets the correct CORS response headers
        headers = {
            "Origin": "http://localhost:8888",
            "Access-Control-Request-Method": "GET"
        }
        response = self.client.options("/api/status", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("access-control-allow-origin"), "http://localhost:8888")

    def test_cors_disallowed_origin(self):
        # Disallowed origins should either not be returned in access-control-allow-origin or be rejected
        headers = {
            "Origin": "http://malicious.com",
            "Access-Control-Request-Method": "GET"
        }
        response = self.client.options("/api/status", headers=headers)
        # In FastAPI with CORSMiddleware, if origin is not allowed, it responds with 400 Bad Request
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("access-control-allow-origin", response.headers)

    def test_cswsh_allowed_origin(self):
        # Allow connecting with an allowed origin
        with self.client.websocket_connect("/ws", headers={"Origin": "http://localhost:8888"}) as websocket:
            data = websocket.receive_json()
            self.assertEqual(data["type"], "system")

    def test_cswsh_disallowed_origin(self):
        # Reject connection from disallowed origin with 1008
        with self.assertRaises(WebSocketDisconnect) as context:
            with self.client.websocket_connect("/ws", headers={"Origin": "http://malicious.com"}):
                pass
        self.assertEqual(context.exception.code, 1008)

    def test_cswsh_no_origin(self):
        # Allow connection without an Origin header (e.g. non-browser clients)
        with self.client.websocket_connect("/ws") as websocket:
            data = websocket.receive_json()
            self.assertEqual(data["type"], "system")

if __name__ == "__main__":
    unittest.main()
