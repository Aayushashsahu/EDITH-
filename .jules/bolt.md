## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-07-02 - Sequential Async Evaluation in List Comprehensions
**Learning:** In Python, list comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially, creating severe performance bottlenecks for I/O-bound tasks. The application was waiting for each embedding to complete before starting the next one.
**Action:** Replace `[await func(x) for x in items]` with `asyncio.gather` for concurrent execution. However, when working with local LLMs (like Ollama), ensure you chunk or batch the gathering (e.g., in batches of 5) to balance speed and system load without overloading local resources.
