## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-08 - Batched async execution for local LLM requests
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially. In the context of local LLM endpoints (like embeddings), this introduces significant I/O performance bottlenecks when processing large lists (e.g., chunks in `SecondBrain`). However, aggressive unbounded concurrency (e.g., using `asyncio.gather` for all chunks at once) can overload local system resources (Ollama).
**Action:** Replaced sequential `await` list comprehensions with `asyncio.gather` batched in chunks of 5 for local LLM and embedding calls to maximize throughput while balancing system load.
