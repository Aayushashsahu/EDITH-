import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

class TestLLMClientEmbed(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Mock aiohttp and config before importing LLMClient
        cls.mock_aiohttp = MagicMock()
        cls.mock_config = MagicMock()
        cls.mock_config.OLLAMA_URL = "http://localhost:11434"
        cls.mock_config.OLLAMA_TIMEOUT = 120
        cls.mock_config.MODEL_FAST = "llama3.2:3b"
        cls.mock_config.MODEL_EMBED = "nomic-embed-text"

        cls.sys_modules_patcher = patch.dict(sys.modules, {
            'aiohttp': cls.mock_aiohttp,
            'config': MagicMock(),
            'config.config': cls.mock_config
        })
        cls.sys_modules_patcher.start()

        # Import LLMClient from edith.backend.agents.llm
        from edith.backend.agents.llm import LLMClient
        cls.LLMClient = LLMClient

    @classmethod
    def tearDownClass(cls):
        cls.sys_modules_patcher.stop()

    def setUp(self):
        self.client = self.LLMClient()

    @patch('aiohttp.ClientSession')
    async def test_embed_success(self, mock_session_cls):
        # Setup mock session
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        # Setup mock response
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"embedding": [0.1, 0.2, 0.3]})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.post.return_value = mock_response

        result = await self.client.embed("test text")

        self.assertEqual(result, [0.1, 0.2, 0.3])
        mock_session.post.assert_called_once()
        # Verify call arguments
        args, kwargs = mock_session.post.call_args
        self.assertEqual(args[0], "http://localhost:11434/api/embeddings")
        self.assertEqual(kwargs['json'], {"model": "nomic-embed-text", "prompt": "test text"})

    @patch('aiohttp.ClientSession')
    async def test_embed_exception(self, mock_session_cls):
        # Setup mock session to raise an exception during post
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        mock_session.post.side_effect = Exception("Connection error")

        result = await self.client.embed("test text")

        self.assertEqual(result, [])

    @patch('aiohttp.ClientSession')
    async def test_embed_json_exception(self, mock_session_cls):
        # Setup mock session
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        # Setup mock response to raise exception during json()
        mock_response = MagicMock()
        mock_response.json = AsyncMock(side_effect=Exception("JSON error"))
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.post.return_value = mock_response

        result = await self.client.embed("test text")

        self.assertEqual(result, [])

    @patch('aiohttp.ClientSession')
    async def test_embed_missing_key(self, mock_session_cls):
        # Setup mock session
        mock_session = MagicMock()
        mock_session_cls.return_value = mock_session
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        # Setup mock response with missing 'embedding' key
        mock_response = MagicMock()
        mock_response.json = AsyncMock(return_value={"something": "else"})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=None)

        mock_session.post.return_value = mock_response

        result = await self.client.embed("test text")

        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
