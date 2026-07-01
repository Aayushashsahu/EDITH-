## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-24 - Optimize sequential LLM embedding calls with batched concurrency
**Learning:** List comprehensions containing `await` evaluate sequentially, causing severe bottlenecks for I/O bound tasks like LLM generation. However, using unbatched `asyncio.gather` on a large list of local Ollama LLM requests causes resource exhaustion and out-of-memory errors on the system.
**Action:** Use `asyncio.gather` combined with small chunking (e.g., batch size 5) for concurrent execution to balance speed and system load without overloading the local model.
