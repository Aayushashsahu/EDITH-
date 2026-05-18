import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

class TestOrchestrator(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Mock dependencies that might not be available in the testing environment
        cls.mock_aiohttp = MagicMock()
        cls.mock_sounddevice = MagicMock()
        cls.mock_kokoro = MagicMock()
        cls.mock_chromadb = MagicMock()
        cls.mock_ollama = MagicMock()
        cls.mock_psutil = MagicMock()
        cls.mock_mss = MagicMock()
        cls.mock_pytesseract = MagicMock()
        cls.mock_PIL = MagicMock()
        cls.mock_bs4 = MagicMock()

        cls.mock_config = MagicMock()
        cls.mock_config.USER_NAME = "Tony"
        cls.mock_config.SYSTEM_NAME = "EDITH"
        cls.mock_config.SYSTEM_VERSION = "V8"
        cls.mock_config.MODEL_FAST = "fast-model"
        cls.mock_config.MODEL_SMART = "smart-model"
        cls.mock_config.MODEL_CODE = "code-model"
        cls.mock_config.MODEL_VISION = "vision-model"

        # Patch sys.modules
        cls.sys_modules_patcher = patch.dict(sys.modules, {
            'aiohttp': cls.mock_aiohttp,
            'sounddevice': cls.mock_sounddevice,
            'kokoro': cls.mock_kokoro,
            'chromadb': cls.mock_chromadb,
            'ollama': cls.mock_ollama,
            'psutil': cls.mock_psutil,
            'mss': cls.mock_mss,
            'pytesseract': cls.mock_pytesseract,
            'PIL': cls.mock_PIL,
            'bs4': cls.mock_bs4,
            'config': MagicMock(),
            'config.config': cls.mock_config
        })
        cls.sys_modules_patcher.start()

        # Now import the modules that depend on the mocked ones
        from backend.agents.orchestrator import Orchestrator, VISION_KW
        cls.Orchestrator = Orchestrator
        cls.VISION_KW = VISION_KW

    @classmethod
    def tearDownClass(cls):
        cls.sys_modules_patcher.stop()

    def setUp(self):
        # Create mocks for dependencies injected into Orchestrator
        self.mock_memory = MagicMock()
        self.mock_tts = MagicMock()
        self.mock_broadcast = AsyncMock()

        # Create instance of Orchestrator
        self.orchestrator = self.Orchestrator(
            memory=self.mock_memory,
            tts=self.mock_tts,
            broadcast=self.mock_broadcast
        )

        # Mock internal components to isolate testing of `handle` method
        self.orchestrator.vision = MagicMock()
        self.orchestrator.router = MagicMock()
        self.orchestrator.llm = MagicMock()
        self.orchestrator.brain = MagicMock()
        self.orchestrator.sys = MagicMock()
        self.orchestrator.web = MagicMock()

        # Mock the specific async methods we expect to be called
        self.orchestrator._vision_handle = AsyncMock()
        self.orchestrator.router.route = AsyncMock()
        self.orchestrator.brain.retrieve = AsyncMock()
        self.orchestrator.llm.generate = AsyncMock()

        # Mock sync methods
        self.orchestrator._pick_model = MagicMock()
        self.orchestrator._build_prompt = MagicMock()
        self.orchestrator._save = MagicMock()

    async def test_handle_vision_path(self):
        # Use a keyword from VISION_KW to trigger vision path
        query = f"hello, {self.VISION_KW[0]} please"
        expected_result = "vision analysis result"

        self.orchestrator._vision_handle.return_value = expected_result

        result = await self.orchestrator.handle(query)

        self.assertEqual(result, expected_result)

        # Verify broadcast was called with correct state and model
        self.mock_broadcast.assert_called_once_with(
            {"type": "state", "state": "processing", "model": self.mock_config.MODEL_VISION}
        )

        # Verify _vision_handle was called
        self.orchestrator._vision_handle.assert_called_once_with(query)

        # Verify result was saved
        self.orchestrator._save.assert_called_once_with(query, expected_result)

        # Verify router and llm were NOT called
        self.orchestrator.router.route.assert_not_called()
        self.orchestrator.llm.generate.assert_not_called()

    async def test_handle_deterministic_tool_path(self):
        # A query that doesn't trigger vision
        query = "turn off the lights"
        expected_result = "lights are off"

        # Setup router to handle the query
        self.orchestrator.router.route.return_value = (expected_result, True)

        result = await self.orchestrator.handle(query)

        self.assertEqual(result, expected_result)

        # Verify router was called
        self.orchestrator.router.route.assert_called_once_with(query)

        # Verify result was saved
        self.orchestrator._save.assert_called_once_with(query, expected_result)

        # Verify vision and llm were NOT called
        self.orchestrator._vision_handle.assert_not_called()
        self.mock_broadcast.assert_not_called() # No broadcast for tool fast path
        self.orchestrator.llm.generate.assert_not_called()

    async def test_handle_standard_llm_path(self):
        # A standard query
        query = "what is the capital of France?"
        expected_model = "fast-model"
        expected_brain_ctx = "brain context"
        expected_prompt = "augmented prompt"
        expected_response = "Paris"

        # Setup mocks
        self.orchestrator.router.route.return_value = (None, False) # Router doesn't handle it
        self.orchestrator._pick_model.return_value = expected_model
        self.orchestrator.brain.retrieve.return_value = expected_brain_ctx
        self.orchestrator._build_prompt.return_value = expected_prompt
        self.orchestrator.llm.generate.return_value = expected_response

        result = await self.orchestrator.handle(query)

        self.assertEqual(result, expected_response)

        # Verify router was called and didn't handle it
        self.orchestrator.router.route.assert_called_once_with(query)

        # Verify model selection and broadcast
        self.orchestrator._pick_model.assert_called_once_with(query.lower().strip())
        self.mock_broadcast.assert_called_once_with(
            {"type": "state", "state": "thinking", "model": expected_model}
        )
        self.assertEqual(self.orchestrator.model, expected_model)

        # Verify context retrieval and prompt building
        self.orchestrator.brain.retrieve.assert_called_once_with(query)
        self.orchestrator._build_prompt.assert_called_once_with(query, expected_brain_ctx)

        # Verify LLM generation
        self.orchestrator.llm.generate.assert_called_once_with(expected_prompt, model=expected_model)

        # Verify result was saved
        self.orchestrator._save.assert_called_once_with(query, expected_response)

        # Verify vision was NOT called
        self.orchestrator._vision_handle.assert_not_called()

if __name__ == '__main__':
    unittest.main()
