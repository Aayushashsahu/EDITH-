## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-06-14 - Local LLM Embedding Performance
**Learning:** Sequential list comprehensions with `await` (e.g., `[await func(x) for x in items]`) severely bottleneck I/O-bound local LLM embedding operations. However, aggressive concurrency (like `asyncio.gather` across all items simultaneously) can overload local system resources.
**Action:** Replaced sequential evaluation with a chunked approach using `asyncio.gather` and a batch size of 5 to balance processing speed and system load when embedding text chunks.
