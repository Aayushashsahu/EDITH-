## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-01 - Optimize asynchronous I/O loops
**Learning:** Sequential list comprehensions with `await` (like `[await func(x) for x in items]`) process items one-by-one and cause severe performance bottlenecks for I/O-bound tasks.
**Action:** Use `asyncio.gather` combined with chunking/batching for concurrent execution without overloading local system resources.
