## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-30 - Batched Concurrency for LLM I/O Operations
**Learning:** Sequential `await` statements in list comprehensions (e.g., `[await func(x) for x in items]`) cause severe performance bottlenecks for I/O-bound tasks like local LLM embedding generations. Conversely, unbounded `asyncio.gather` can overload local system resources or the local LLM model (Ollama).
**Action:** When handling multiple concurrent I/O requests to the local LLM or embedding endpoints, use `asyncio.gather` coupled with small batch chunking (e.g., batch size 5) to balance speed and local system load.
