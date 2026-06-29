## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-18 - Optimize _embed_all concurrency
**Learning:** List comprehensions containing `await` (e.g., `[await self.llm.embed(t) for t in texts]`) evaluate sequentially, which can cause severe performance bottlenecks for I/O-bound tasks like embedding generation.
**Action:** Use `asyncio.gather` combined with chunking/batching (e.g. batch size of 5) for concurrent execution to improve speed without overloading local system resources.
