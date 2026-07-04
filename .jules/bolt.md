## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-30 - Replace Sequential Awaits in Comprehensions with Batching
**Learning:** Sequential list comprehensions with `await` (e.g., `[await func(x) for x in items]`) evaluate one by one, causing severe performance bottlenecks for I/O-bound tasks. This is especially true for Ollama LLM embeddings which are repeatedly accessed during document ingestion.
**Action:** Replaced sequential awaits in memory vector stores with concurrent execution using `asyncio.gather`. To avoid overloading local system resources or the local LLM, batching with a fixed chunk size (e.g., 5) must be combined with concurrent execution.
