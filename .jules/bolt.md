## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2024-06-25 - Optimize _embed_all LLM Batching
**Learning:** List comprehensions containing `await` inside loops evaluate sequentially, creating severe performance bottlenecks for I/O bound LLM calls. However, unbounded `asyncio.gather` on large lists overloads the local system/Ollama.
**Action:** Use chunking (e.g. batch size of 5) combined with `asyncio.gather` for local embedding tasks. This balances speed optimizations with local system resource limits, significantly speeding up execution while maintaining stability.
