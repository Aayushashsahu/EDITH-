import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import sys

# Mocking missing dependencies as instructed by memory
sys.modules['aiohttp'] = MagicMock()
sys.modules['kokoro'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()
sys.modules['pyaudio'] = MagicMock()
sys.modules['chromadb'] = MagicMock()

# Need to mock the agent dependencies as well so we can test the main.py
sys.modules['backend.agents'] = MagicMock()
sys.modules['backend.agents.orchestrator'] = MagicMock()
sys.modules['backend.memory'] = MagicMock()
sys.modules['backend.memory.store'] = MagicMock()
sys.modules['backend.memory.brain'] = MagicMock()
sys.modules['backend.voice'] = MagicMock()
sys.modules['backend.voice.tts'] = MagicMock()
sys.modules['backend.automations'] = MagicMock()
sys.modules['backend.automations.scheduler'] = MagicMock()

# Mock fastap StaticFiles mount check
patch("fastapi.staticfiles.StaticFiles.__init__", return_value=None).start()
patch("fastapi.staticfiles.StaticFiles.__call__", new_callable=MagicMock).start()


from edith.backend.main import app

class TestCors(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

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

if __name__ == "__main__":
    unittest.main()
