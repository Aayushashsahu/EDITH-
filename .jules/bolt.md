## 2024-05-20 - Cache ML Pipeline Instances
**Learning:** Instantiating ML pipelines (like Kokoro's `KPipeline`) on every method call introduces severe latency due to repeated model loading overhead.
**Action:** Always cache heavy ML pipeline or model instances as class attributes to avoid re-instantiation and significantly reduce generation latency.
