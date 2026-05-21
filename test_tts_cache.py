import sys
from unittest.mock import MagicMock
sys.modules['kokoro'] = MagicMock()
sys.modules['sounddevice'] = MagicMock()

from backend.voice.tts import TTSEngine

engine = TTSEngine()
engine._kokoro("Hello")
engine._kokoro("World")

# Check if KPipeline was called exactly once
assert sys.modules['kokoro'].KPipeline.call_count == 1
print("KPipeline called exactly once, caching works!")
