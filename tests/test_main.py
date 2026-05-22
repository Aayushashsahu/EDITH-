import sys
import os
from pathlib import Path
import unittest
from unittest.mock import MagicMock

# Ensure the mock BASE_DIR returns a string path that actually exists
# so StaticFiles can mount it without complaining
temp_static_dir = Path(__file__).parent / "test_static"
os.makedirs(temp_static_dir, exist_ok=True)

# We have to mock config differently to handle the Path operator /
mock_config = MagicMock()
mock_config.PORT = 8888
mock_config.SYSTEM_NAME = "TEST"
mock_config.SYSTEM_VERSION = "1.0"
mock_config.HOST = "127.0.0.1"
mock_config.BASE_DIR = Path(__file__).parent / "mock_base_dir"
mock_config.TASKS_DB = Path(__file__).parent / "mock_base_dir" / "tasks.db"
os.makedirs(mock_config.BASE_DIR / "frontend" / "static", exist_ok=True)
os.makedirs(mock_config.BASE_DIR / "frontend" / "templates", exist_ok=True)

# Write a dummy index.html
with open(mock_config.BASE_DIR / "frontend" / "templates" / "index.html", "w") as f:
    f.write("<html><body>TEST</body></html>")

sys.modules['backend.agents.orchestrator'] = MagicMock()
sys.modules['backend.memory.store'] = MagicMock()
sys.modules['backend.memory.brain'] = MagicMock()
sys.modules['backend.voice.tts'] = MagicMock()
sys.modules['backend.automations.scheduler'] = MagicMock()
sys.modules['config.config'] = mock_config

# Mock the whole backend.automations.task_manager module to avoid db issues inside main
mock_task_manager_module = MagicMock()
sys.modules['backend.automations.task_manager'] = mock_task_manager_module

from fastapi.testclient import TestClient
from edith.backend.main import app
import edith.backend.main as main_module

class TestMainEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

        # Reset globals in main_module before each test
        main_module.orc = MagicMock()
        main_module.mem = MagicMock()
        main_module.tts = MagicMock()
        main_module.sched = MagicMock()

    def test_serve_ui(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("TEST", response.text)

    def test_status(self):
        # Configure the mock
        main_module.orc.model = "test-model"
        main_module.orc.brain.count.return_value = 42
        main_module.orc.sys.stats_dict.return_value = {"cpu": 10, "ram": 50}

        response = self.client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["online"], True)
        self.assertEqual(data["model"], "test-model")
        self.assertEqual(data["brain_docs"], 42)
        self.assertEqual(data["cpu"], 10)
        self.assertEqual(data["ram"], 50)

    def test_history(self):
        main_module.mem.all.return_value = [{"role": "user", "content": "hi"}]
        response = self.client.get("/api/history")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["messages"], [{"role": "user", "content": "hi"}])

    def test_tasks_endpoints(self):
        mock_tm_instance = MagicMock()
        mock_task_manager_module.TaskManager.return_value = mock_tm_instance

        # GET /api/tasks
        mock_tm_instance.list_tasks.return_value = [{"id": 1, "title": "Buy milk"}]
        response = self.client.get("/api/tasks")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["tasks"], [{"id": 1, "title": "Buy milk"}])

        # POST /api/tasks
        mock_tm_instance.add.return_value = {"id": 2, "title": "Write tests"}
        response = self.client.post("/api/tasks", json={"title": "Write tests"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 2, "title": "Write tests"})
        mock_tm_instance.add.assert_called_once_with("Write tests", "", "medium")

        # PATCH /api/tasks/{task_id}
        mock_tm_instance.complete.return_value = "Task 1 marked complete."
        response = self.client.patch("/api/tasks/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], "Task 1 marked complete.")
        mock_tm_instance.complete.assert_called_once_with(1)

    def test_ingest_success(self):
        main_module.orc.brain.ingest_text.return_value = 5
        response = self.client.post("/api/ingest", json={"text": "some new info", "source": "test"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["chunks"], 5)
        main_module.orc.brain.ingest_text.assert_called_once_with("some new info", "test")

    def test_ingest_missing_text(self):
        response = self.client.post("/api/ingest", json={"source": "test"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "no text")

    def test_notes(self):
        main_module.orc.sys.read_notes.return_value = "My notes"
        response = self.client.get("/api/notes")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["notes"], "My notes")

if __name__ == '__main__':
    unittest.main()
