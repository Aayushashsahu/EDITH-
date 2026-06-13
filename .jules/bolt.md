## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.

## 2024-06-13 - LLMClient aiohttp Session Pooling
**Learning:** Caching `aiohttp.ClientSession` instead of recreating it on every request enables connection pooling, which is a key performance optimization when repeatedly hitting the local Ollama backend for embeddings and generations.
**Action:** Always instantiate a single `aiohttp.ClientSession` per client class instance (and ensure it's closed properly) when making frequent HTTP requests.
