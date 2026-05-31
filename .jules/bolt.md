## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-25 - Batch concurrent embedding extraction in SecondBrain
**Learning:** Sequential coroutine awaiting in list comprehensions (e.g., `[await embed(t) for t in texts]`) causes severe latency bottlenecks during bulk file ingestion by blocking on each item.
**Action:** Replaced sequential execution with batched concurrent execution using `asyncio.gather` (batch size of 5) to balance system load and significantly accelerate embedding generation for large documents.
