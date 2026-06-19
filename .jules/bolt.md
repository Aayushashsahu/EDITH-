## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-06-19 - Concurrent Batched Execution for I/O Bound Tasks
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially. In the case of `_embed_all`, making sequential network calls for embeddings introduces severe latency bottlenecks, especially when processing many chunks of text. However, attempting to use `asyncio.gather` on all chunks concurrently can overload local systems (like a local Ollama server).
**Action:** Replace sequential `await` list comprehensions with `asyncio.gather`, but combine it with small batching (e.g., batch size of 5) for tasks like local LLM interactions or embeddings to balance execution speed and system load.
