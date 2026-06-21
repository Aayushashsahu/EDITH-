## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2025-02-12 - Sequential List Comprehension vs Batch Concurrency for Embeddings
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, acting as a significant performance bottleneck for I/O-bound or LLM operations. However, using `asyncio.gather` for too many concurrent operations against a local LLM can overload local system resources.
**Action:** When handling multiple embedding requests or other local LLM calls, replace sequential list comprehensions with `asyncio.gather`, but enforce batched concurrency (e.g., chunked into batches of 5) to balance speed and system load without triggering rate-limits or timeouts.
