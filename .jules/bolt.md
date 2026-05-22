## 2024-05-18 - Caching ML Pipelines
**Learning:** Instantiating heavy ML pipelines (like Kokoro's KPipeline) inside a method called frequently causes a significant performance bottleneck due to repeated model loading.
**Action:** Always cache such pipeline instances as class attributes (e.g., `self._kokoro_pipe`) so they are loaded once and reused across subsequent calls.
