## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-07-05 - Optimize _embed_all Concurrency
**Learning:** Sequential list comprehensions with `await` (e.g. `[await func(x) for x in items]`) cause severe performance bottlenecks for I/O-bound tasks like embedding generation. However, unbounded `asyncio.gather` can overload local system resources. Chunking with a small batch size (e.g., 5) strikes the perfect balance between throughput and system stability.
**Action:** Replaced sequential list comprehensions in `SecondBrain._embed_all` with a batched `asyncio.gather` implementation to improve embedding generation throughput.
