## 2026-05-23 - ML Model Caching for TTS pipelines
**Learning:** Instantiating ML pipeline classes (like `kokoro.KPipeline`) on every method call incurs extremely high latency due to reloading models, weights, and configurations repeatedly.
**Action:** Always cache these heavy ML pipeline objects as class attributes (e.g., `self._kokoro_pipe`) so they are initialized only once per application lifecycle.
