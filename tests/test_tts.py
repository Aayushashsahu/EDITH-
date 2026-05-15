import sys
import unittest
from unittest.mock import MagicMock, patch

class TestTTSEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Mock config before importing TTSEngine
        cls.mock_config = MagicMock()
        cls.mock_config.TTS_ENGINE = "pyttsx3"
        cls.mock_config.PIPER_BIN = "piper"
        cls.mock_config.PIPER_MODEL = "model.onnx"

        cls.sys_modules_patcher = patch.dict(sys.modules, {
            'config': MagicMock(),
            'config.config': cls.mock_config
        })
        cls.sys_modules_patcher.start()

        # Import TTSEngine from edith.backend.voice.tts
        from edith.backend.voice.tts import TTSEngine
        cls.TTSEngine = TTSEngine

    @classmethod
    def tearDownClass(cls):
        cls.sys_modules_patcher.stop()

    def setUp(self):
        self.engine = self.TTSEngine()

    @patch('edith.backend.voice.tts.traceback')
    def test_pyttsx3_exception_traceback(self, mock_traceback):
        # Mock sys.modules['pyttsx3'] to raise an exception when imported
        mock_pyttsx3 = MagicMock()
        mock_pyttsx3.init.side_effect = Exception("Test initialization error")

        with patch.dict(sys.modules, {'pyttsx3': mock_pyttsx3}):
            # Trigger the fallback or direct call
            self.engine._pyttsx3("Test text")

            # Assert that traceback.print_exc() was called
            mock_traceback.print_exc.assert_called_once()

if __name__ == '__main__':
    unittest.main()
