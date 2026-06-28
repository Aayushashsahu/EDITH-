## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-05-30 - Optimizing Async IO-Bound Operations (Embeddings)
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially. This can become a severe performance bottleneck for I/O-bound tasks such as calling a local LLM or making embedding requests.
**Action:** Use `asyncio.gather` combined with small batches/chunks (e.g., batch size 5) to balance execution speed through concurrency without causing resource exhaustion or overloading local systems like Ollama.
