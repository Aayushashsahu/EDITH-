
## 2024-05-24 - Cache ML pipelines to avoid expensive re-instantiation
**Learning:** Instantiating heavy ML pipelines like Kokoro `KPipeline` on every TTS method call causes significant performance degradation and unnecessary computational overhead.
**Action:** When implementing or optimizing ML models or TTS engines within classes, cache the model or pipeline instance as a class attribute during initialization or upon first use to ensure it is only created once.
