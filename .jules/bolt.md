## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2026-06-23 - Batched Concurrent LLM Calls
**Learning:** List comprehensions containing `await` evaluate sequentially, creating a significant performance bottleneck for I/O-bound tasks like requesting embeddings from a local LLM in `SecondBrain._embed_all`.
**Action:** Replaced sequential `await` loops with `asyncio.gather`. To avoid overloading local system resources with aggressive concurrency, applied batching (e.g., batch size 5) to balance speed and system load.
