import sys
import unittest
from unittest.mock import MagicMock, AsyncMock, patch

class TestSecondBrain(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        # Mock chromadb, aiohttp, and config before importing SecondBrain
        cls.mock_chromadb = MagicMock()
        cls.mock_aiohttp = MagicMock()
        cls.mock_config = MagicMock()
        cls.mock_config.CHROMA_DIR = "/tmp/chroma"
        cls.mock_config.BRAIN_DIR = "/tmp/brain"
        cls.mock_config.CHUNK_SIZE = 100
        cls.mock_config.CHUNK_OVERLAP = 20
        cls.mock_config.RETRIEVAL_K = 3
        cls.mock_config.RELEVANCE_CUTOFF = 0.5

        # We also need to mock backend.agents.llm to prevent its own imports from failing,
        # or we just let our aiohttp mock handle it. The LLMClient uses aiohttp.
        cls.sys_modules_patcher = patch.dict(sys.modules, {
            'chromadb': cls.mock_chromadb,
            'aiohttp': cls.mock_aiohttp,
            'config': MagicMock(),
            'config.config': cls.mock_config
        })
        cls.sys_modules_patcher.start()

        # Mock the path behavior for tests
        cls.mock_path = MagicMock()

        # Import SecondBrain
        from edith.backend.memory.brain import SecondBrain
        cls.SecondBrain = SecondBrain

    @classmethod
    def tearDownClass(cls):
        cls.sys_modules_patcher.stop()

    def setUp(self):
        # Reset mocks
        self.mock_chromadb.reset_mock()
        self.mock_aiohttp.reset_mock()

        # Setup mock collection
        self.mock_collection = MagicMock()
        self.mock_collection.count.return_value = 5
        self.mock_client = MagicMock()
        self.mock_client.get_or_create_collection.return_value = self.mock_collection
        self.mock_chromadb.PersistentClient.return_value = self.mock_client

        with patch('os.makedirs'):
            self.brain = self.SecondBrain()

        # Mock the LLMClient inside the brain
        self.brain.llm = MagicMock()
        self.brain.llm.embed = AsyncMock(return_value=[0.1, 0.2, 0.3])

    @patch('edith.backend.memory.brain.Path')
    async def test_init_auto_ingest(self, mock_path_cls):
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance

        # Setup rglob to return a text file and a non-text file
        mock_file1 = MagicMock()
        mock_file1.suffix = ".txt"
        mock_file1.name = "test.txt"

        mock_file2 = MagicMock()
        mock_file2.suffix = ".jpg"
        mock_file2.name = "test.jpg"

        mock_path_instance.rglob.return_value = [mock_file1, mock_file2]

        # Mock get to simulate file not yet ingested
        self.mock_collection.get.return_value = {"ids": []}

        # Mock ingest_file
        self.brain.ingest_file = AsyncMock()

        await self.brain.init()

        # Should only call ingest for .txt
        self.brain.ingest_file.assert_called_once_with(str(mock_file1))

    def test_ingest_text(self):
        text = "This is a test text that needs to be long enough to pass the 60 char strip length check inside the chunking method. Adding some more text to ensure it passes."

        result = self.brain.ingest_text(text, source="test_source")

        self.assertEqual(result, 1) # Should result in 1 chunk
        self.mock_collection.upsert.assert_called_once()

        args, kwargs = self.mock_collection.upsert.call_args
        self.assertIn('documents', kwargs)
        self.assertIn('embeddings', kwargs)
        self.assertIn('ids', kwargs)
        self.assertIn('metadatas', kwargs)
        self.assertEqual(kwargs['metadatas'][0]['source'], "test_source")

    def test_ingest_text_empty(self):
        result = self.brain.ingest_text("")
        self.assertEqual(result, 0)
        self.mock_collection.upsert.assert_not_called()

    @patch('edith.backend.memory.brain.Path')
    async def test_ingest_file_text(self, mock_path_cls):
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.suffix = ".txt"
        mock_path_instance.name = "test.txt"
        mock_path_instance.read_text.return_value = "Test content " * 10

        self.brain.ingest_text = MagicMock(return_value=1)

        result = await self.brain.ingest_file("test.txt")

        self.assertEqual(result, 1)
        self.brain.ingest_text.assert_called_once_with("Test content " * 10, source="test.txt")

    @patch('edith.backend.memory.brain.Path')
    async def test_ingest_file_not_exist(self, mock_path_cls):
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        result = await self.brain.ingest_file("test.txt")

        self.assertEqual(result, 0)

    @patch('edith.backend.memory.brain.Path')
    async def test_ingest_file_pdf_no_module(self, mock_path_cls):
        mock_path_instance = MagicMock()
        mock_path_cls.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.suffix = ".pdf"
        mock_path_instance.name = "test.pdf"

        # Test the fallback text when fitz is not installed
        self.brain.ingest_text = MagicMock(return_value=1)

        result = await self.brain.ingest_file("test.pdf")

        self.assertEqual(result, 1)
        self.brain.ingest_text.assert_called_once_with("[PDF support: pip install pymupdf]", source="test.pdf")

    async def test_retrieve_success(self):
        self.mock_collection.count.return_value = 5
        self.mock_collection.query.return_value = {
            "documents": [["Doc 1", "Doc 2"]],
            "distances": [[0.1, 0.2]]
        }

        result = await self.brain.retrieve("test query")

        self.assertEqual(result, "Doc 1\n---\nDoc 2")
        self.brain.llm.embed.assert_called_once_with("test query")
        self.mock_collection.query.assert_called_once()

    async def test_retrieve_no_docs(self):
        self.mock_collection.count.return_value = 0

        result = await self.brain.retrieve("test query")

        self.assertEqual(result, "")
        self.brain.llm.embed.assert_not_called()

    async def test_retrieve_no_embed(self):
        self.mock_collection.count.return_value = 5
        self.brain.llm.embed = AsyncMock(return_value=[])

        result = await self.brain.retrieve("test query")

        self.assertEqual(result, "")
        self.mock_collection.query.assert_not_called()


    async def test_add_memory_success(self):
        self.brain.store = MagicMock()
        self.brain.log = MagicMock()

        await self.brain.add_memory("test memory", meta={"key": "value"})

        self.brain.llm.embed.assert_called_once_with("test memory")
        self.brain.store.add.assert_called_once_with("test memory", [0.1, 0.2, 0.3], {"key": "value"})
        self.brain.log.info.assert_called_once()

    async def test_add_memory_empty_text(self):
        self.brain.store = MagicMock()
        self.brain.log = MagicMock()

        await self.brain.add_memory("")

        self.brain.llm.embed.assert_not_called()
        self.brain.store.add.assert_not_called()

    async def test_add_memory_no_embed(self):
        self.brain.store = MagicMock()
        self.brain.log = MagicMock()
        self.brain.llm.embed = AsyncMock(return_value=[])

        await self.brain.add_memory("test memory")

        self.brain.store.add.assert_not_called()

if __name__ == '__main__':
    unittest.main()
