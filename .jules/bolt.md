## 2025-03-01 - Cache Kokoro TTS pipeline to reduce latency
**Learning:** Instantiating heavy ML models like Kokoro's `KPipeline` on every inference call leads to massive performance bottlenecks (latency of seconds per call).
**Action:** Always cache expensive ML pipeline instances as class attributes and lazy-load them on first use to drastically improve performance on subsequent calls.