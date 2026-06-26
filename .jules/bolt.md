## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-06-26 - Optimizing Concurrent LLM Operations with Batching
**Learning:** Using sequential `await` in a list comprehension for local LLM requests (e.g., embeddings) causes a massive performance bottleneck due to lack of concurrency. On the other hand, a single unbounded `asyncio.gather()` across all chunks can overload local system resources. A batching approach provides the best balance.
**Action:** Replaced sequential `[await func(x) for x in items]` with `asyncio.gather()` chunked in small batches (e.g., batch size 5) to significantly speed up file ingestion while keeping system load manageable.
