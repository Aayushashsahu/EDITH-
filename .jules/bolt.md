## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2024-05-24 - Async IO Loop Bottlenecks
**Learning:** List comprehensions containing `await` (e.g., `[await func(x) for x in items]`) evaluate sequentially rather than concurrently. This causes severe performance bottlenecks for I/O-bound tasks like embedding bulk document chunks with local LLMs.
**Action:** Replace sequential async comprehensions with `asyncio.gather` for concurrent execution, but chunk/batch the requests (e.g., using a small batch size like 5) to prevent overloading local system resources and avoid "Too Many Requests" errors from the local Ollama instance.
