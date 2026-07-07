## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-07-07 - Sequential I/O bottleneck in List Comprehensions
**Learning:** Using `await` inside a sequential list comprehension (e.g., `[await func(x) for x in items]`) evaluates each call sequentially, creating severe performance bottlenecks for I/O-bound tasks like local LLM embedding requests.
**Action:** Replace sequential list comprehensions for I/O-bound asynchronous functions with `asyncio.gather`. When calling local or resource-heavy services, batch the execution (e.g., chunk size of 5) to balance execution speed without overloading system resources.
