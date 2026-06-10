## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2026-06-10 - Asyncio Gather for LLM Embeddings
**Learning:** List comprehensions with `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, causing performance bottlenecks for I/O-bound tasks.
**Action:** Use `asyncio.gather` combined with chunking/batching (e.g., batch size 5) for concurrent execution when making local LLM embedding requests, to balance speed and system load without overloading the local server.
