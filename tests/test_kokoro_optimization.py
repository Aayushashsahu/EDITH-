import unittest
from unittest.mock import MagicMock
import sys

# Mock modules to avoid ModuleNotFoundError in sandbox
sys.modules['kokoro'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()

from backend.voice.tts import TTSEngine

class TestTTSEngine(unittest.TestCase):
    def test_kokoro_caching(self):
        engine = TTSEngine()
        # Ensure _kokoro_pipe is initially None
        self.assertIsNone(engine._kokoro_pipe)

        # First call should instantiate the pipeline
        engine._kokoro("Hello")
        self.assertIsNotNone(engine._kokoro_pipe)

        # Save the instance reference
        first_instance = engine._kokoro_pipe

        # Second call should reuse the same pipeline
        engine._kokoro("World")
        self.assertIs(first_instance, engine._kokoro_pipe)

if __name__ == '__main__':
    unittest.main()
