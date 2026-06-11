## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-30 - Concurrent API calls for Embeddings
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, which can cause severe performance bottlenecks for I/O-bound tasks. This was occurring in `SecondBrain._embed_all` during file ingestion.
**Action:** Replaced sequential awaits with concurrent execution using `asyncio.gather`. To prevent overloading local Ollama LLM system resources, added batching (size=5) alongside gather. Always use `asyncio.gather` for concurrent execution of I/O bound tasks and apply batching when hitting local LLMs.
