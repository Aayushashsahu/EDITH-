## 2024-05-19 - ML Pipeline Caching for TTS Performance
**Learning:** Instantiating ML pipelines (like Kokoro TTS `KPipeline`) on every method call introduces severe latency and re-initialization overhead. Re-importing heavy modules (`kokoro`, `sounddevice`) also adds minor overhead.
**Action:** When working with ML models or heavy pipelines, always lazy-initialize them and cache the instances as class attributes (e.g., `self._kokoro_pipe`) for reuse across subsequent calls to drastically improve response times.
