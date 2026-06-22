## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-06-22 - Batched Concurrency for Local LLM Calls
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, which causes severe performance bottlenecks for I/O-bound tasks like local LLM or embedding calls. Aggressive concurrency (such as gathering across all chunks at once) can overload local system resources.
**Action:** Use `asyncio.gather` combined with small chunking/batch sizes (e.g., 5) for concurrent execution of local LLM operations to balance speed and system load.
