## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-31 - Sequential await in List Comprehensions
**Learning:** Using `await` inside a list comprehension (e.g., `[await func(x) for x in items]`) forces sequential execution, creating a significant latency bottleneck for I/O-bound tasks like LLM embedding generation.
**Action:** Replace sequential list comprehensions containing `await` with `asyncio.gather` for concurrent execution. For potentially large lists or heavy API calls, process items in chunks/batches to balance speed and system load without overloading resources.
