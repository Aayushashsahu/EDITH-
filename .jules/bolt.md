## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-30 - Optimize Local LLM Batching
**Learning:** Sequential list comprehensions containing `await` (e.g., `[await func(x) for x in items]`) process items one-by-one, which becomes a severe bottleneck for I/O-bound tasks like embedding multiple text chunks. However, using unrestrained concurrency (e.g., `asyncio.gather` on hundreds of chunks at once) can overload local system resources.
**Action:** Always batch concurrent LLM operations. Use `asyncio.gather` combined with a small, sensible chunk/batch size (e.g., 5) to balance speed improvements and local system resource consumption.
