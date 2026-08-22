## 2024-05-30 - Caching Kokoro KPipeline Instance
**Learning:** Instantiating heavy ML pipelines like `KPipeline` on every method call introduces severe latency bottlenecks. Profiling the TTS engine revealed that this pattern severely degrades performance for repeated invocations in an application aiming for near-real-time responsiveness.
**Action:** Implemented caching for the `KPipeline` object as a class attribute `self._kokoro_pipe` in `TTSEngine`. In the future, always inspect methods executing ML or deep-learning models to ensure the model instance is instantiated lazily once and reused.
## 2024-06-11 - Local LLM Embedding Bottlenecks
**Learning:** List comprehensions containing `await` evaluate sequentially. When batch processing text chunks for local LLM embeddings (e.g., in `SecondBrain._embed_all`), this sequential execution acts as a major performance bottleneck for I/O-bound tasks.
**Action:** Use chunked concurrency with `asyncio.gather(batch_size=5)` instead of sequential `await` list comprehensions. This ensures concurrent execution to significantly speed up processing while still preventing the system from being overloaded by too many concurrent embedding requests.

## 2026-07-10 - Batched Concurrency for Embedding
**Learning:** List comprehensions with await evaluate sequentially, causing performance bottlenecks for I/O tasks. Aggressive concurrency overloads local Ollama instances.
**Action:** Replaced sequential await with `asyncio.gather` combined with chunking (batch size of 5) to balance speed and system load.
## 2024-05-18 - [Optimize aiohttp session in LLMClient]
**Learning:** Creating a new `aiohttp.ClientSession()` on every call inside `LLMClient` destroys the benefits of HTTP connection pooling and adds significant latency overhead per request when repeatedly calling the local LLM backend.
**Action:** Reused a single `aiohttp.ClientSession` by caching it as a class attribute `self._session` to enable connection pooling and improve performance on sequential backend requests.
## 2024-08-02 - Batched Canvas Rendering
**Learning:** In animation loops (`requestAnimationFrame`), drawing many static elements (like a dot grid) using separate `beginPath()` and `fill()` calls per element causes a severe CPU bottleneck in this codebase's monolithic UI.
**Action:** Always batch drawing of identical elements (same color/style) into a single path. Call `beginPath()` once, use `moveTo()` to separate sub-paths, and call `fill()` once at the end.
## 2026-08-03 - HTML5 Canvas Batching vs Pre-rendering
**Learning:** While batching canvas paths (e.g., using moveTo to separate sub-paths before a single fill) avoids redundant state changes, drawing hundreds of static shapes repeatedly inside a requestAnimationFrame loop still incurs heavy CPU overhead due to evaluating the paths frame after frame.
**Action:** Always pre-render complex static canvas elements (like grids or dots) to an offscreen canvas. Then, simply copy the pre-rendered texture using drawImage(offscreenCanvas, 0, 0) during the main animation loop to vastly reduce CPU usage.
## 2024-05-19 - Concurrent WebSocket Broadcasting
**Learning:** In the `broadcast` function, iterating over connected websocket clients with a sequential `await ws.send_text(msg)` causes a major performance bottleneck as the number of clients increases. Each client's send operation blocks the loop until it completes, severely degrading the near-real-time responsiveness required for broadcasting.
**Action:** Replaced the sequential `await` loop in `broadcast` (both `backend/main.py` and `edith/backend/main.py`) with `asyncio.gather(*tasks, return_exceptions=True)`. This allows all messages to be sent concurrently, and gracefully collects any connection exceptions for dead connection cleanup, drastically reducing the overall broadcast latency.
