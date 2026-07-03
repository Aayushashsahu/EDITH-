## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2024-06-11 - Local LLM Embedding Bottlenecks
**Learning:** List comprehensions containing `await` evaluate sequentially. When batch processing text chunks for local LLM embeddings (e.g., in `SecondBrain._embed_all`), this sequential execution acts as a major performance bottleneck for I/O-bound tasks.
**Action:** Use chunked concurrency with `asyncio.gather(batch_size=5)` instead of sequential `await` list comprehensions. This ensures concurrent execution to significantly speed up processing while still preventing the system from being overloaded by too many concurrent embedding requests.
