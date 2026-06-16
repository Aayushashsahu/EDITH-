## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-16 - Replacing Sequential List Comprehensions with Batch-Limited asyncio.gather
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, causing significant performance bottlenecks for I/O-bound tasks like local LLM embeddings.
**Action:** When executing concurrent LLM calls or I/O bound loops, avoid sequential comprehensions. Replace them with `asyncio.gather` combined with batching (e.g., chunks of 5) to maximize concurrent performance while preventing local system resource overload.
