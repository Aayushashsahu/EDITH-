## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2025-02-24 - Avoiding Sequential Execution in Coroutine List Comprehensions
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially. When executing I/O-bound tasks like local LLM embeddings, this causes a severe performance bottleneck.
**Action:** Use `asyncio.gather(*tasks)` combined with chunking/batching to achieve safe concurrency without overloading local system resources. Avoid sequential list comprehensions for heavy asynchronous operations.
