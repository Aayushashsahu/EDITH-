## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-25 - Optimizing Async I/O in Iterables
**Learning:** Using a list comprehension with `await` (e.g., `[await func(x) for x in items]`) evaluates sequentially, which can cause severe performance bottlenecks for I/O-bound tasks like repeatedly calling an LLM or vector embedding service.
**Action:** Use `asyncio.gather` combined with chunking/batching (e.g., `batch_size = 5`) for concurrent execution. This executes I/O requests concurrently while preventing overload on local system resources (like Ollama).
