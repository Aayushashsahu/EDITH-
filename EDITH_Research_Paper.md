# EDITH: A Resource-Constrained Offline Personal AI Architecture  
## with Multi-Stage Routing and Hybrid Memory on Consumer Hardware

**Aayush Sahu**  
Department of Computer Science and Engineering  
MIT-ADT University (MITSOE), Pune, Maharashtra, India  
May 2026

---

## Abstract

Cloud-hosted AI assistants introduce latency, privacy risk, and ongoing API cost — constraints that motivate fully offline alternatives. This paper describes **EDITH V8**, a personal AI architecture that operates entirely on-device within a 10 GB RAM budget under WSL2 on consumer laptop hardware. The primary technical contribution is a three-stage, resource-aware routing architecture that resolves 63.6% of real daily queries through deterministic tool dispatch — with zero LLM inference — at a median latency of 27 ms for non-network operations. The remaining queries are dispatched to one of three locally hosted LLMs selected by query-feature classification, keeping the fast-path inference latency at 1.82 s (warm model). Ablation studies confirm that removing the routing layer increases mean query latency by 3.1× and that RAG augmentation reduces factual error rate on personal-knowledge queries by 41%. The system integrates voice input, OS-level automation, persistent semantic memory, and scheduled tasks in a single deployable stack. Limitations include a fixed 6-second voice capture window, heuristic model selection, and the absence of a formal user study.

**Keywords:** local LLM, edge inference, personal AI, dynamic model routing, retrieval-augmented generation, privacy-preserving AI, WSL2, offline AI

---

## 1. Introduction

The dominant paradigm for AI assistants in 2026 routes all user queries through cloud-hosted large language models. This design offers capable models but imposes three structural costs: network round-trip latency (typically 500 ms–4 s depending on region and load), transmission of all query content to third-party infrastructure, and per-token API fees that accumulate substantially under daily heavy use.

Advances in model quantization and local inference runtimes have made it feasible to run capable LLMs on consumer hardware [1][2]. However, existing user-facing tools in this space — GPT4All, Jan, LM Studio — address inference and chat interfaces, but not the broader requirements of a daily-use personal assistant: persistent memory, voice I/O, OS-level automation, remote access, and task scheduling. Users who require these capabilities must either retain cloud dependency or assemble a custom stack.

This paper describes EDITH V8, a system that integrates all of these capabilities within a single deployable architecture. The design operates under a deliberate constraint: all computation must fit within a 10 GB WSL2 RAM allocation on a mid-range consumer laptop. This constraint is meaningful because it matches the practical reality of a large population of potential users and forces architectural decisions that would not arise on unconstrained hardware.

**The central contribution is not the integration of components per se, but the routing strategy that makes the integration practical under tight resource constraints.** Specifically, the claim evaluated in this paper is: *a tiered deterministic-then-heuristic routing architecture, applied before any LLM invocation, is the primary latency lever in a resource-constrained local AI system — more impactful than model size, quantization level, or hardware acceleration.* This claim is evaluated through ablation studies in Section 4.

Contributions of this paper:

1. A three-stage query routing architecture (vision check → regex tool dispatch → keyword model selection) that eliminates LLM inference for the majority of real daily queries, with measured latency impact
2. Ablation studies isolating the latency and quality contributions of the routing layer and RAG memory system independently
3. A structured comparison of EDITH's capability set against GPT4All, Jan, and LM Studio on six dimensions relevant to personal assistant use
4. A RAM budgeting analysis for concurrent quantized model management within a 10 GB constraint
5. A TTS fallback chain with three degradation tiers ensuring voice output under hardware variability

The rest of this paper is structured as follows: Section 2 reviews related work. Section 3 describes the architecture. Section 4 reports experiments and results. Section 5 discusses limitations. Section 6 concludes.

---

## 2. Related Work

### 2.1 Edge LLM Deployment

Zheng, Chen, Qian, Shi, Shu, and Chen [3] survey the full lifecycle of edge LLM deployment — from quantization and pruning strategies to runtime scheduling and on-device applications. They identify three core advantages of on-device inference: elimination of network latency, removal of cloud data transmission risk, and the ability to adapt models to user-specific context. Their survey does not address multi-model routing or full-stack personal assistant integration.

Matsutani, Matsuda, and Sugiura [4] propose distributed prompt caching across multiple low-end edge devices, sharing intermediate KV-cache states to accelerate local inference for repeated query patterns. Their work targets throughput optimization across cooperative devices; EDITH targets latency minimization on a single device through routing rather than caching.

Yang, Yang, Zhao, Guo, He, and Ji [5] present PerLLM, a personalized inference scheduling framework using edge-cloud collaboration modeled as a constrained multi-armed bandit problem. PerLLM achieves 2.2× throughput improvement and over 50% energy cost reduction compared to naive scheduling. Their framework assumes hybrid edge-cloud operation; EDITH takes the stricter position of zero cloud dependency.

### 2.2 LLM Routing

RAGRouter [6] trains a routing classifier to dispatch queries across multiple RAG-augmented LLMs, outperforming the best single model by 3.61% on average. Self-Routing RAG [7] reduces unnecessary retrievals by 29% through selective retrieval routing. Both works address routing in the context of multiple cloud or server-hosted models. EDITH applies a related intuition — that not all queries should follow the same inference path — to the specific constraint of local RAM-limited model management.

METIS [8] adapts RAG configurations per query, achieving 12–15% higher quality and 2.5–3× lower latency compared to fixed configurations. This per-query adaptation approach is related to EDITH's model selection step, though METIS targets cloud RAG systems rather than local consumer hardware.

### 2.3 Personal AI Assistants

Ghamati, Banitalebi Dehkordi, and Zaraki [9] propose a Personalised LLM (PLLM) agent for human-robot interaction, demonstrating personality and context adaptation through domain-specific fine-tuning on EEG sensor data. Their work establishes feasibility of adaptive local LLM agents but focuses on fine-tuning methodology rather than system integration.

A domain-specific comparison by Kiefer et al. [10] evaluates RAG-augmented local LLMs (Llama 3.2-11B) against cloud models for radiology consultation, finding that RAG eliminates hallucinations (0% vs. 8%, p=0.012) and improves response ranking by 1.3 positions on average. This result — that RAG provides measurable quality benefit over baseline local LLM inference — informs EDITH's RAG design and the ablation study in Section 4.4.

Existing user-facing local LLM tools — GPT4All, Jan, LM Studio — provide chat interfaces and model management. None implement persistent cross-session semantic memory, scheduled automations, voice I/O pipelines, or OS-level system control. Section 4.1 provides a structured capability comparison.

### 2.4 Retrieval-Augmented Generation

Lewis, Perez, Piktus, Petroni, Karpukhin, Goyal et al. [11] established RAG as a general method for grounding LLM responses in retrieved external documents, reducing hallucinations and enabling personalized context. ChromaDB [12] provides HNSW-indexed vector storage suitable for edge deployment. EDITH implements a cosine distance threshold gate on retrieved chunks — a design decision that trades recall for precision in retrieval quality, discussed in Section 5.2.

### 2.5 Positioning

EDITH V8 combines on-device LLM inference, multi-stage routing, RAG-based memory, and voice/automation integration within a single RAM-constrained system. The ablation study in Section 4 provides the empirical grounding that distinguishes this work from prior integration-focused descriptions.

---

## 3. System Architecture

EDITH V8 is organized across five tiers: user interfaces, server, orchestration, tool execution with memory, and model serving.

---

### Figure 1 — System Overview

```
╔═══════════════════════════════════════════════════════════════════╗
║                         USER INTERFACES                          ║
║                                                                   ║
║  ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐  ║
║  │  Voice Listener  │  │   Browser HUD    │  │  Telegram Bot  │  ║
║  │  (Whisper STT +  │  │  (WebSocket,     │  │  (Remote ctrl, │  ║
║  │   wake word)     │  │   real-time HUD) │  │   polling)     │  ║
║  └────────┬─────────┘  └────────┬─────────┘  └───────┬────────┘  ║
╚═══════════╪════════════════════╪═══════════════════╪═══════════╝
            └────────────────────┼───────────────────┘
                                 │  WebSocket / HTTP
                                 ▼
╔═══════════════════════════════════════════════════════════════════╗
║               FASTAPI + WEBSOCKET SERVER  (port 8888)            ║
║               Async event loop — aiohttp — broadcast()           ║
╚═══════════════════════════════╤═══════════════════════════════════╝
                                │
                                ▼
╔═══════════════════════════════════════════════════════════════════╗
║                          ORCHESTRATOR                            ║
║                                                                   ║
║  ┌─────────────────────────────────────────────────────────────┐  ║
║  │                 3-STAGE ROUTING PIPELINE                    │  ║
║  │                                                             │  ║
║  │  Stage 1              Stage 2             Stage 3          │  ║
║  │  Vision Check  ──►    Intent Router  ──►  LLM Select       │  ║
║  │  (10 keywords)        (18 regex patt.)    (keyword class.)  │  ║
║  │  → LLaVA:7b           → Tool direct       → 3b / 7b / code │  ║
║  └─────────────────────────────────────────────────────────────┘  ║
╚══════╤════════════════════════╤════════════════════════╤══════════╝
       │                        │                        │
       ▼                        ▼                        ▼
╔════════════╗  ╔═══════════════════════════╗  ╔═════════════════════╗
║   SCREEN   ║  ║      TOOL EXECUTION       ║  ║   MEMORY + RAG      ║
║   VISION   ║  ║                           ║  ║                     ║
║            ║  ║  SystemControl            ║  ║  SQLite (turns)     ║
║  PS script ║  ║  (WSL→Windows bridge)     ║  ║  ChromaDB (vectors) ║
║  → PNG     ║  ║                           ║  ║  nomic-embed-text   ║
║  → base64  ║  ║  WebTools                 ║  ║                     ║
║  → LLaVA  ║  ║  (DuckDuckGo, wttr.in,    ║  ║  Ingest: chunk →    ║
║            ║  ║   BeautifulSoup scrape)   ║  ║  embed → upsert     ║
╚════════════╝  ║                           ║  ║                     ║
                ║  TaskManager              ║  ║  Retrieve: embed →  ║
                ║  (SQLite, NL due dates)   ║  ║  cosine query →     ║
                ║                           ║  ║  dist < 0.65 filter ║
                ║  APScheduler              ║  ╚═════════════════════╝
                ║  (briefing, wind-down,    ║
                ║   hourly task check)      ║
                ╚═══════════════════════════╝
                                │ prompt injected context
                                ▼
╔═══════════════════════════════════════════════════════════════════╗
║                    OLLAMA LOCAL MODEL SERVER                     ║
║                                                                   ║
║  ┌──────────────────┐  ┌─────────────┐  ┌──────────┐  ┌───────┐  ║
║  │  llama3.2:3b     │  │ qwen2.5:7b  │  │codellama │  │llava  ║
║  │  Q4_K_M ~2.2 GB  │  │ Q4_K_M      │  │:7b ~4.5GB│  │:7b    ║
║  │  always warm     │  │ ~4.5 GB     │  │on demand │  │~4.5GB ║
║  │  fast path       │  │ on demand   │  │code path │  │vision ║
║  └──────────────────┘  └─────────────┘  └──────────┘  └───────┘  ║
║  nomic-embed-text: ~0.3 GB (always loaded for RAG)               ║
╚═══════════════════════════════════════════════════════════════════╝
```
*Figure 1: Full system architecture. Arrows indicate data flow direction.*

---

### Figure 2 — Three-Stage Routing Decision Tree

```
                     ┌──────────────────────────┐
                     │       Incoming Query      │
                     └─────────────┬────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │  STAGE 1: Vision keyword?    │
                    │  ("what's on my screen",     │
                    │   "describe the error", ...)  │
                    └──────────┬──────────────────┘
                          YES  │        NO
                 ┌─────────────┘         │
                 ▼                       │
        ┌────────────────┐               │
        │  → LLaVA:7b    │               │
        │  (screenshot + │               │
        │   vision LLM)  │               ▼
        │  ~9.8s warm    │  ┌────────────────────────────┐
        └────────────────┘  │  STAGE 2: Matches any of   │
                            │  18 regex intent patterns?  │
                            │  (time, system, weather,    │
                            │   apps, volume, power,      │
                            │   files, notes, web, ...)   │
                            └──────────┬─────────────────┘
                                  YES  │       NO
                    ┌─────────────────┘         │
                    ▼                           │
         ┌──────────────────────┐               │
         │  → Tool Direct Call  │               │
         │  (SystemControl /    │               │
         │   WebTools / DB)     │               ▼
         │  0 LLM tokens        │  ┌────────────────────────────┐
         │  median: 27ms        │  │  STAGE 3: Query features?  │
         │  63.6% of queries    │  └──────────────┬─────────────┘
         └──────────────────────┘                 │
                                     ┌────────────┴───────────┐
                                     │                        │
                              CODE_KW match?           COMPLEX_KW match
                              or "bug","syntax"        OR len > 180?
                                     │                        │
                              YES    │              YES       │   NO
                              ┌──────┘         ┌─────────────┘    │
                              ▼                ▼                   ▼
                   ┌─────────────────┐  ┌────────────┐  ┌───────────────┐
                   │  codellama:7b   │  │ qwen2.5:7b │  │  llama3.2:3b  │
                   │  ~5.5s warm     │  │ ~4.4s warm │  │  ~1.82s warm  │
                   │  2.2% queries   │  │ 8.2% quer. │  │  24.8% quer.  │
                   └─────────────────┘  └────────────┘  └───────────────┘
```
*Figure 2: Query routing decision tree. Percentages from 500-query real-usage sample (Table 4).*

---

### Figure 3 — Hybrid Memory Architecture

```
╔═══════════════════════════════════════════════════════════════════╗
║                      HYBRID MEMORY SYSTEM                        ║
╠═══════════════════════════════╦═══════════════════════════════════╣
║   SHORT-TERM: SQLite          ║   LONG-TERM: ChromaDB (RAG)       ║
║   ─────────────────────       ║   ────────────────────────        ║
║                               ║                                   ║
║   Table: messages             ║   INGESTION PIPELINE:             ║
║   ┌────────────────────┐      ║   Raw text / .md / .pdf           ║
║   │id│role│content│ts  │      ║          │                        ║
║   └────────────────────┘      ║          ▼                        ║
║                               ║   Split: 400-word chunks          ║
║   Retrieval:                  ║   50-word overlap                 ║
║   SELECT ... ORDER BY id      ║          │                        ║
║   DESC LIMIT 40               ║          ▼                        ║
║   < 1ms latency               ║   nomic-embed-text (local)        ║
║                               ║   → embedding vector              ║
║   Injected as:                ║          │                        ║
║   [RECENT CONVERSATION]       ║          ▼                        ║
║   last 20 turns (40 msgs)     ║   ChromaDB upsert                 ║
║                               ║   (HNSW index, cosine space)      ║
║                               ║                                   ║
║                               ║   RETRIEVAL PIPELINE:             ║
║                               ║   1. embed query   ~40ms          ║
║                               ║   2. cosine search top-4          ║
║                               ║   3. filter dist > 0.65 ──► drop  ║
║                               ║   4. inject as [SECOND BRAIN]     ║
║                               ║   Total overhead: ~55–62ms        ║
║                               ║   Constant w.r.t. collection size ║
╚═══════════════════════════════╩═══════════════════════════════════╝
```
*Figure 3: Hybrid memory. SQLite handles short-term turns; ChromaDB handles long-term semantic retrieval.*

---

### Figure 4 — Voice Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                         VOICE PIPELINE                           │
│                                                                  │
│  INPUT PROCESS  (listener.py — separate process)                 │
│  ─────────────────────────────────────────────                   │
│                                                                  │
│  sounddevice.rec(6s, 16kHz)                                      │
│       │  ← FIXED WINDOW — largest latency bottleneck            │
│       ▼                                                          │
│  Whisper base STT (CPU)  ─── ~1.1–1.8s ───►  transcript text    │
│       │                                                          │
│       ▼                                                          │
│  "hey edith" in text?                                            │
│       │ YES                                                      │
│       ▼                                                          │
│  extract command (if empty → 2nd 6s capture)                     │
│       │                                                          │
│       ▼                                                          │
│  ws.send({"type":"query","content": command})                    │
│       │                                                          │
│  ─────┼─── WebSocket boundary ──────────────────────────────    │
│       │                                                          │
│  OUTPUT PROCESS  (tts.py — called post-inference)                │
│  ───────────────────────────────────────────────                 │
│       │                                                          │
│       ▼                                                          │
│  _clean(text): strip markdown, cap 600 chars                     │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  TTS_ENGINE priority check                              │    │
│  │                                                         │    │
│  │  "piper" → piper binary + en_US-lessac-medium.onnx     │    │
│  │            → raw PCM 22050Hz → aplay  (~180–220ms)     │    │
│  │                                                         │    │
│  │  "kokoro" → KPipeline(lang_code="a")                   │    │
│  │             → sounddevice.play(24000Hz)                 │    │
│  │                                                         │    │
│  │  fallback  → pyttsx3 (always available)                │    │
│  └─────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────┘
```
*Figure 4: Voice pipeline. Fixed 6s capture window dominates total voice latency. TTS fallback chain ensures output under model unavailability.*

---

### Figure 5 — WSL2-to-Windows Control Bridge

```
┌──────────────────────────────────────────────────────────────────┐
│                 WSL2 → WINDOWS CONTROL BRIDGE                   │
│                                                                  │
│  LINUX SIDE (EDITH backend)        WINDOWS HOST                 │
│  ───────────────────────────       ────────────                 │
│                                                                  │
│  Intent: open_app("spotify")  →  cmd.exe /c start spotify       │
│  Intent: lock()               →  rundll32 user32.dll,Lock...    │
│  Intent: set_volume(40)       →  nircmd setsysvolume 26214      │
│  Intent: mute()               →  PS SendKeys([char]173)         │
│  Intent: screenshot()         →  PS System.Drawing.Bitmap       │
│  Intent: open_url(url)        →  PS Start-Process '{url}'       │
│  Intent: sleep()              →  rundll32 powrprof.dll,SetSusp. │
│  Intent: shell(cmd)           →  subprocess (WSL-side only)     │
│                                                                  │
│  _cmd() bridge:                                                  │
│  subprocess.run([                                                │
│      "/mnt/c/Windows/System32/cmd.exe", "/c", command           │
│  ], capture_output=True, timeout=15)                            │
│                                                                  │
│  _ps() bridge:                                                   │
│  subprocess.run([                                                │
│      "/mnt/c/.../powershell.exe","-NoProfile","-Command",script  │
│  ], capture_output=True, timeout=20)                            │
│                                                                  │
│  URL injection prevention:                                       │
│  urllib.parse.urlparse() → scheme validation (http/https only)  │
│  → single-quote escaping before PS string interpolation         │
│  → Start-Process '{safe_url_ps}'                                │
└──────────────────────────────────────────────────────────────────┘
```
*Figure 5: System control bridge. WSL2 /mnt/c/ mount exposes Windows executables to the Linux backend.*

---

### Figure 6 — RAM Budget by System State

```
RAM (GB)
10 ┤                                    ┌─────────────────────────┐
   │                                    │  Peak: llava:7b loaded  │
 9 ┤                                    │  ~8.5 GB total          │
   │                                    │  (vision queries only)  │
 8 ┤                  ┌──────────────┐  └─────────────────────────┘
   │                  │qwen2.5:7b    │
 7 ┤                  │loaded ~7.8GB │
   │                  │(complex quer)│
 6 ┤                  └──────────────┘
   │
 5 ┤
   │
 4 ┤
   │
 3 ┤ ┌────────────────────────────────────────────────────────────┐
   │ │  BASELINE (llama3.2:3b warm):  ~3.3 GB                    │
 2 ┤ │  ─────────────────────────────────────────────────────     │
   │ │  llama3.2:3b:         2.2 GB                              │
 1 ┤ │  nomic-embed-text:    0.3 GB (always loaded, RAG)         │
   │ │  ChromaDB + Python:   0.5 GB                              │
 0 ┤ │  FastAPI + aiohttp:   0.3 GB                              │
   └─┴─────────────────────────────────────────────────────────
         Idle        Fast query     Complex query    Vision query
         (baseline)  (3b, warm)     (7b on-demand)  (llava, rare)

   7B models unload after 5min Ollama idle timeout.
   Simultaneous 7b + llava load (~8.5+) not supported.
```
*Figure 6: RAM consumption by system state. On-demand loading prevents simultaneous accumulation of multiple 7B models.*

---

### 3.1 Three-Stage Query Routing

The orchestrator's routing pipeline is the primary architectural contribution. It resolves queries at the cheapest available tier before escalating.

**Stage 1 — Vision Detection.** Ten keyword patterns trigger screen capture and LLaVA:7b inference. A PowerShell script captures a PNG of the primary display via .NET's `System.Drawing`, saves it to a WSL-accessible temp path, and the orchestrator encodes it as base64 for Ollama's multimodal generate endpoint. This path bypasses the intent router entirely.

**Stage 2 — Deterministic Intent Router.** The `IntentRouter` class applies 18 regex patterns across categories: time/date, system statistics, weather (with city group extraction), web search, YouTube, URL and application opening, volume (set/mute/up/down), power management (lock/sleep/shutdown/restart), screenshot, file operations (ls/read/shell), notes (save/read), second-brain ingestion, text typing, network info, and process listing. On any pattern match, the corresponding tool function executes synchronously and returns its result. No LLM tokens are consumed.

**Stage 3 — LLM Model Selection.** Unhandled queries are classified by structural string features:

```python
CODE_KW = ["code","function","script","debug","refactor",
           "implement","class","bug","error in","syntax",
           "algorithm","program","fix this"]

COMPLEX_KW = ["explain","analyse","analyze","compare","write",
              "summarise","research","essay","plan","strategy",
              "how does","why does","step by step"]

if any(k in query for k in CODE_KW):
    model = "codellama:7b"
elif any(k in query for k in COMPLEX_KW) or len(query) > 180:
    model = "qwen2.5:7b"
else:
    model = "llama3.2:3b"
```

Classification adds 1–3 ms of Python string matching. This avoids loading a 7B model for simple factual queries and avoids returning 3B responses for multi-step reasoning tasks. Known failure modes of this heuristic are discussed in Section 5.3.

### 3.2 Hybrid Memory

**Short-term memory (SQLite).** Every conversation turn is persisted across sessions. The last 40 messages are retrieved and injected as a `[RECENT CONVERSATION]` block in every LLM prompt. Retrieval latency is below 1 ms.

**Long-term memory (ChromaDB RAG).** Text ingested from files or voice commands is chunked (400-word chunks, 50-word overlap), embedded by `nomic-embed-text` running locally via Ollama, and upserted to a ChromaDB collection with content-hash IDs to prevent duplicates. On each LLM query, the query is embedded, the collection is searched for the top-4 most similar chunks, and chunks with cosine distance above 0.65 are filtered out. Surviving chunks are injected as a `[SECOND BRAIN]` block before the user query. Total RAG overhead is 55–62 ms regardless of collection size (HNSW indexing). Files in `data/second_brain/` are auto-ingested on startup.

### 3.3 Prompt Structure

Every LLM call assembles a prompt from four ordered blocks: persona (identity, rules, date), second brain (retrieved chunks, injected only when relevant chunks pass the distance filter), recent conversation (last 40 messages, injected when history exists), and query. The persona block enforces a 1–3 sentence default response length, which constrains TTS synthesis time.

### 3.4 Voice Pipeline

Voice input (`listener.py`) runs as an independent process, capturing 6-second audio windows at 16 kHz via `sounddevice`, transcribing via Whisper (`base` model), checking for the wake word "hey edith," and forwarding extracted commands to the backend WebSocket. A second capture is triggered if the wake word appears without a trailing command.

Voice output (`TTSEngine`) implements a three-tier fallback: Piper binary (180–220 ms, neural, highest quality) → Kokoro Python library → pyttsx3 system TTS (always available). All text is pre-cleaned before synthesis.

### 3.5 System Control Bridge and Automation

WSL2 exposes Windows executables via the `/mnt/c/` mount. Two bridge functions — `_cmd()` (cmd.exe) and `_ps()` (PowerShell) — enable 18 distinct system control operations from the Linux backend. URL opening uses PowerShell's `Start-Process` with URL scheme validation and single-quote escaping to prevent injection.

`APScheduler` drives a morning briefing (weather + RSS + due tasks → LLM summary → TTS), an evening reminder, and an hourly task check. The SQLite task manager parses natural language due dates (today, tomorrow, next week, named weekdays, "in N days," ISO dates) via regex.

---

## 4. Experiments and Results

### 4.1 Capability Comparison Against Existing Local Tools

Table 1 compares EDITH's feature set against the three primary user-facing local LLM tools as of early 2026. Capability data for GPT4All, Jan, and LM Studio is drawn from their respective documentation and the comparison reported in [13].

**Table 1: Capability comparison — EDITH vs. local LLM tools**

| Capability | GPT4All | Jan | LM Studio | EDITH V8 |
|---|---|---|---|---|
| Chat interface | ✓ | ✓ | ✓ | ✓ |
| Local RAG (file ingestion) | ✓ | ✗ | ✗ | ✓ |
| Voice input (STT) | ✗ | ✗ | ✗ | ✓ |
| Voice output (TTS) | ✗ | ✗ | ✗ | ✓ |
| OS-level system control | ✗ | ✗ | ✗ | ✓ |
| Scheduled automations | ✗ | ✗ | ✗ | ✓ |
| Persistent cross-session memory | ✓ | ✓ | ✗ | ✓ |
| Multi-model routing | ✗ | ✗ | ✗ | ✓ |
| Remote access (Telegram) | ✗ | ✗ | ✗ | ✓ |
| Hard RAM budget operation | ✗ | ✗ | ✗ | ✓ |

GPT4All offers local RAG through its document integration feature. Jan and LM Studio focus on model serving and chat. None of the three implement voice I/O, system automation, multi-model routing, or remote access. This comparison motivates the integration goal but does not constitute a performance benchmark — latency comparisons with these tools would require controlled shared-hardware testing outside the scope of this paper.

### 4.2 Experimental Setup

All measurements were taken on:
- **Device**: Samsung Galaxy Book 5 360
- **CPU**: Intel Core Ultra 7 155H (16-core, iGPU)
- **RAM**: 16 GB system; 10 GB allocated to WSL2
- **OS**: Windows 11 22H2 / WSL2 Ubuntu 24.04
- **Ollama**: 0.6.x; Q4\_K\_M quantization for all models
- **Python**: 3.11

All latency values are end-to-end wall-clock time from query submission to first character of response available. Reported values are means over 30 trials (first 5 discarded as warm-up). Standard deviation is reported where relevant to characterize variance.

### 4.3 Routing Latency by Stage

**Table 2: Intent router latency by category (Stage 2 only, 30 trials)**

| Category | Mean Latency | Std Dev | LLM Tokens |
|---|---|---|---|
| Time / date | 0.4 ms | 0.1 ms | 0 |
| System statistics (psutil) | 22 ms | 4.1 ms | 0 |
| App launch (cmd.exe) | 65 ms | 12 ms | 0 |
| Volume control (PowerShell) | 45 ms | 8 ms | 0 |
| Notes save | 3 ms | 0.5 ms | 0 |
| Weather (wttr.in HTTP) | 340 ms | 78 ms | 0 |
| DuckDuckGo search (HTTP) | 1,210 ms | 390 ms | 0 |
| Web scrape (HTTP) | 2,840 ms | 880 ms | 0 |
| **Median (non-network ops)** | **27 ms** | — | **0** |

Network-bound operations are dominated by external HTTP round-trip time and would vary with connection quality. All non-network tool calls resolve below 70 ms.

### 4.4 LLM Path Latency

**Table 3: LLM path end-to-end latency (30-trial average, includes RAG overhead)**

| Model | Warm Mean | Warm Std Dev | Cold Mean | Cold Penalty |
|---|---|---|---|---|
| llama3.2:3b | 1.82 s | 0.24 s | 4.10 s | +2.28 s |
| qwen2.5:7b | 4.35 s | 0.51 s | 8.20 s | +3.85 s |
| codellama:7b | 5.50 s | 0.68 s | 9.30 s | +3.80 s |
| llava:7b (vision) | 9.80 s | 1.20 s | 14.10 s | +4.30 s |

Cold-start penalties for 7B models (3.8–4.3 s) arise from disk-to-RAM model loading by Ollama. The fast model (llama3.2:3b) is maintained warm at all times; 7B models are loaded on demand and unloaded after 5 minutes of inactivity.

**Comparison with cloud baseline.** For reference, GPT-4o-mini API calls from a standard residential broadband connection in Pune, India average 1.2–2.0 s end-to-end (inference + network, excluding TTS). EDITH's fast model path (1.82 s warm, excluding capture) is within 0.6–1.0 s of this figure. This comparison excludes the 6-second Whisper capture window; post-capture latency (routing + inference + Piper TTS) on the tool path averages 0.2–0.6 s and on the LLM path averages 2.0–2.7 s. The voice capture bottleneck is acknowledged in Section 5.1.

### 4.5 Query Routing Distribution

**Table 4: Routing path distribution over 500 real daily queries**

| Path | Count | Percentage | Mean Latency |
|---|---|---|---|
| Stage 2: Deterministic tool | 318 | 63.6% | 27 ms (non-net.) |
| Stage 3: llama3.2:3b | 124 | 24.8% | 1.82 s |
| Stage 3: qwen2.5:7b | 41 | 8.2% | 4.35 s |
| Stage 3: codellama:7b | 11 | 2.2% | 5.50 s |
| Stage 1: llava:7b (vision) | 6 | 1.2% | 9.80 s |

The Stage 2 deterministic router handles 63.6% of queries without any LLM invocation. This figure is the empirical basis for the claim that routing strategy is the primary latency lever in this architecture.

### 4.6 RAG Retrieval Overhead

**Table 5: RAG pipeline overhead by ChromaDB collection size (30 trials)**

| Collection Size | Embed Time | Query Time | Total Overhead |
|---|---|---|---|
| 0 chunks (empty) | skipped | skipped | 0 ms |
| 100 chunks | 38 ms | 12 ms | 50 ms |
| 500 chunks | 41 ms | 15 ms | 56 ms |
| 2,000 chunks | 43 ms | 19 ms | 62 ms |

RAG overhead is approximately constant with collection size due to HNSW indexing. The embedding call dominates at ~40 ms. This scaling property makes the system suitable for users who accumulate large personal knowledge bases.

### 4.7 Ablation Studies

Three ablation conditions were evaluated to isolate the contribution of individual components. Each condition was measured over the same 500-query real-usage sample.

---

**Ablation A: Routing Disabled (all queries go to llama3.2:3b)**

In this condition, the intent router and vision detection are bypassed. Every query is sent directly to llama3.2:3b. This is the baseline behavior of tools such as GPT4All or Jan.

**Table 6: Impact of disabling the routing layer**

| Metric | Full System | No Routing | Change |
|---|---|---|---|
| Mean query latency | 0.63 s | 1.98 s | **+3.1×** |
| Queries resolved < 100ms | 63.6% | 0% | −63.6 pp |
| LLM token consumption (relative) | 1.0× | 3.8× | +280% |
| Response correctness (tool queries)¹ | 100% | 68% | −32 pp |

¹ *Tool queries (e.g., "what time is it," "open Spotify") were judged correct if the actual system action was performed. LLM responses to these queries were frequently plausible but non-actionable (e.g., "It appears to be around 3pm" rather than executing a time lookup).*

Disabling routing increases mean latency by 3.1× and reduces correct tool-action execution from 100% to 68%, as the LLM produces plausible but non-executable text responses to deterministic queries. This result quantifies the routing layer's contribution beyond latency alone.

---

**Ablation B: RAG Disabled (no second brain retrieval)**

In this condition, ChromaDB retrieval is disabled. The LLM prompt receives persona and conversation history but no retrieved personal knowledge.

The evaluation set for this ablation was 60 queries specifically constructed to require personal knowledge stored in the user's second brain (notes on academic subjects, project details, personal preferences). Each response was scored by the author as correct (accurate retrieval), partially correct (relevant but incomplete), or incorrect (hallucinated or absent information).

**Table 7: Impact of disabling RAG on personal-knowledge queries**

| Metric | With RAG | Without RAG | Change |
|---|---|---|---|
| Correct responses | 74% | 43% | −31 pp |
| Partially correct | 18% | 26% | +8 pp |
| Incorrect / hallucinated | 8% | 31% | +23 pp |
| Mean latency (LLM path) | 1.94 s | 1.82 s | +120ms |

RAG reduces incorrect responses from 31% to 8% on personal-knowledge queries, at a cost of 120 ms additional latency per query (the RAG pipeline overhead). This is consistent with the finding by Kiefer et al. [10] that RAG-augmented local LLMs show significantly reduced hallucination rates compared to baseline inference.

---

**Ablation C: Always 7B (llama3.2:3b replaced by qwen2.5:7b for all LLM-path queries)**

This condition evaluates whether substituting the fast model with the larger model improves quality enough to justify the latency increase.

**Table 8: Fast model vs. always-7B on the LLM path**

| Metric | llama3.2:3b (default) | qwen2.5:7b (always) | Difference |
|---|---|---|---|
| Mean LLM-path latency (warm) | 1.82 s | 4.35 s | +2.53 s |
| Mean LLM-path latency (cold) | 4.10 s | 8.20 s | +4.10 s |
| Response quality score¹ (1–5) | 3.8 | 4.2 | +0.4 |
| RAM in use (steady state) | 3.3 GB | 7.8 GB | +4.5 GB |

¹ *Quality scored by author on 50 non-tool queries using a 1–5 Likert scale across accuracy, completeness, and conciseness dimensions.*

The 7B model produces modestly better responses (+0.4 on a 5-point scale), but at 2.4× the latency cost on warm paths and 2× the RAM footprint. For the majority of the fast-path query types (factual, conversational, brief), the quality difference is perceptible but not substantial enough to warrant the latency penalty in a real-time assistant context. The routing architecture's value is precisely that it can serve the minority of complex queries with the 7B model while maintaining fast-path performance for the majority.

### 4.8 Summary of Results

The ablation studies produce three quantified claims:

1. **Routing layer**: Removing it increases mean query latency by 3.1× and reduces correct tool-action execution by 32 percentage points.
2. **RAG**: Removing it increases incorrect responses from 8% to 31% on personal-knowledge queries, while saving 120 ms per query.
3. **Fast model vs. 7B always**: Always using qwen2.5:7b adds 2.53 s per LLM-path query (warm) for a 0.4/5 quality gain — a tradeoff that favors the fast model for the majority of real-usage query types.

---

## 5. Limitations

### 5.1 Fixed-Window Voice Capture

The 6-second audio capture window is the single largest contributor to total voice pipeline latency. A user who speaks a 1-second command waits 5 additional seconds before transcription begins. Voice activity detection (VAD)-gated capture — recording until silence rather than until a fixed duration — would reduce effective capture time to approximately 300–500 ms for typical commands. The Silero VAD library is listed as a dependency but is not integrated into the main voice loop. All voice latency figures in this paper include the full 6-second window and should not be compared directly with cloud assistant latency figures that do not include this overhead.

### 5.2 RAG Threshold Not Empirically Calibrated

The cosine distance threshold of 0.65 was determined by manual inspection of retrieval quality on a small sample, not by systematic evaluation against annotated relevance judgments. A threshold too permissive injects off-topic chunks and degrades response quality; one too strict silently excludes relevant context. The current value should be treated as a reasonable initialization, not an optimized parameter.

### 5.3 Keyword-Based Model Routing Failures

The keyword routing heuristic produces known false positives. A query such as "what is the code of conduct for conferences?" incorrectly routes to codellama:7b due to the substring "code." Based on manual inspection of 500 queries, this misclassification occurs in approximately 4–6% of real-usage queries. A lightweight classifier trained on labeled examples would improve routing precision; the keyword approach was chosen for zero-latency overhead.

### 5.4 WSL2 Audio Routing Fragility

WSL2 audio requires PulseAudio routing between the Linux and Windows audio subsystems. Under WSLg (Windows 11), this is handled automatically. Under non-WSLg configurations, manual setup is required and is prone to breaking across Windows update cycles. This limits the voice pipeline to configurations where WSLg is available and functioning.

### 5.5 Absence of Formal User Study

The evaluation in Section 4 relies on the author's own query logs and qualitative scoring. No external user study was conducted. The 500-query usage sample reflects one user's usage patterns over approximately three weeks and may not generalize to different demographics, query distributions, or hardware configurations. A user study with a diverse participant pool, structured tasks, and validated metrics (e.g., Task Completion Rate, NASA-TLX cognitive load) is needed to substantiate the "practical daily-use" claim.

### 5.6 Response Quality Evaluation Subjectivity

The quality scores in Ablation C (Section 4.7, Table 8) are self-scored by the author using a Likert scale. This introduces evaluator bias. Future work should use blind evaluation by multiple raters or automated evaluation via a stronger judge model.

---

## 6. Conclusion

This paper described EDITH V8, an offline-first personal AI architecture designed for daily use within a 10 GB RAM constraint on consumer hardware. The primary empirical contributions are:

- The three-stage routing architecture resolves 63.6% of real daily queries with zero LLM inference, at a median latency of 27 ms for non-network operations.
- Removing the routing layer increases mean query latency by 3.1× — a result that quantifies routing as the dominant latency lever in this architecture.
- RAG reduces incorrect responses on personal-knowledge queries from 31% to 8%, at 120 ms additional latency per LLM-path query.
- The fast model (llama3.2:3b) provides adequate quality for 86.8% of LLM-path queries, with 7B models reserved for the 11.6% of queries where their quality benefit justifies the additional 2.5 s warm latency.
- A structured capability comparison shows that existing local LLM tools (GPT4All, Jan, LM Studio) do not implement voice I/O, system automation, multi-model routing, or scheduled tasks — capabilities that EDITH integrates within the 10 GB constraint.

The system's limitations are significant. The 6-second fixed capture window makes raw voice-to-response latency uncompetitive with cloud assistants; post-capture latency is more favorable. The evaluation lacks a formal user study. Quality scoring is self-reported. These are the primary obstacles to treating this as a mature research result rather than an engineering demonstration.

### 6.1 Future Work

**VAD-gated capture.** Replacing fixed windows with silence-triggered recording would reduce capture overhead from 6 s to 0.3–0.5 s for typical commands, making voice-path latency genuinely competitive with cloud systems.

**Learned routing classifier.** A DistilBERT-scale classifier trained on labeled query examples could reduce the estimated 4–6% misclassification rate of keyword routing with minimal latency overhead.

**Streaming LLM output.** Token-by-token response streaming to the frontend would allow TTS to begin synthesis before full response generation, reducing perceived latency on the LLM path.

**Formal user study.** A study with 10–20 participants over one week, measuring daily usage frequency, task completion rate, and subjective satisfaction (SUS scale), would provide the external validity currently missing.

**Ablation over quantization levels.** Comparing Q4\_K\_M, Q5\_K\_M, and Q8\_0 quantization for each model tier would characterize the quality/RAM/latency tradeoff surface and inform hardware-specific deployment recommendations.

**RAG threshold calibration.** A sweep over the cosine distance threshold against an annotated relevance judgment set would replace the current hand-tuned value with a data-driven parameter.

---

## References

[1] Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., et al. (2023). *Llama 2: Open foundation and fine-tuned chat models.* arXiv:2307.09288.

[2] Ggerganov. (2023). *llama.cpp: LLM inference in C/C++.* GitHub. https://github.com/ggerganov/llama.cpp

[3] Zheng, Y., Chen, Y., Qian, B., Shi, X., Shu, Y., and Chen, J. (2025). *A review on edge large language models: Design, execution, and applications.* ACM Computing Surveys. doi:10.1145/3719664. arXiv:2410.11845.

[4] Matsutani, H., Matsuda, N., and Sugiura, N. (2026). *Accelerating local LLMs on resource-constrained edge devices via distributed prompt caching.* Department of ICS, Keio University. arXiv:2602.22812.

[5] Yang, Z., Yang, Y., Zhao, C., Guo, Q., He, W., and Ji, W. (2024). *PerLLM: Personalized inference scheduling with edge-cloud collaboration for diverse LLM services.* Institute of Computing Technology, Chinese Academy of Sciences. arXiv:2405.14636.

[6] Chen, Y., et al. (2025). *RAGRouter: Learning to route queries to multiple retrieval-augmented language models.* arXiv:2505.23052.

[7] Wu, X., et al. (2025). *Self-routing RAG: Binding selective retrieval with knowledge verbalization.* arXiv:2504.01018.

[8] Gujarati, A., et al. (2025). *METIS: Fast quality-aware RAG systems with configuration adaptation.* In *Proceedings of SOSP 2025.* Microsoft Research.

[9] Ghamati, K., Banitalebi Dehkordi, M., and Zaraki, A. (2025). *Towards AI-powered applications: The development of a personalised LLM for HRI and HCI.* *Sensors,* 25(7), 2024. doi:10.3390/s25072024.

[10] Kiefer, B., et al. (2025). *Retrieval-augmented generation elevates local LLM quality in radiology contrast media consultation.* PMC12223273. doi:10.1038/s41598-025-05765-3.

[11] Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., et al. (2020). *Retrieval-augmented generation for knowledge-intensive NLP tasks.* In *NeurIPS 2020.* arXiv:2005.11401.

[12] Chroma. (2022). *Chroma: The AI-native open-source embedding database.* https://github.com/chroma-core/chroma.

[13] ToolHalla. (2026, March). *LM Studio vs Jan vs GPT4All: Best local LLM app in 2026.* https://toolhalla.ai/blog/lm-studio-vs-jan-vs-gpt4all-2026.

[14] Radford, A., Kim, J.W., Xu, T., Brockman, G., McLeavey, C., and Sutskever, I. (2022). *Robust speech recognition via large-scale weak supervision.* arXiv:2212.04356. Published ICML 2023.

[15] Rhasspy Project. (2023). *Piper: A fast, local, neural text-to-speech system.* https://github.com/rhasspy/piper.

---

## Appendix A: Configuration Parameters

| Parameter | Default | Description |
|---|---|---|
| `MODEL_FAST` | llama3.2:3b | Primary model; kept warm at all times |
| `MODEL_SMART` | qwen2.5:7b | For complex / long queries |
| `MODEL_CODE` | codellama:7b | For code-related queries |
| `MODEL_VISION` | llava:7b | For screen understanding |
| `MODEL_EMBED` | nomic-embed-text | Local embedding model for RAG |
| `CHUNK_SIZE` | 400 words | RAG ingestion chunk size |
| `CHUNK_OVERLAP` | 50 words | Overlap between adjacent chunks |
| `RETRIEVAL_K` | 4 | Max chunks retrieved per query |
| `RELEVANCE_CUTOFF` | 0.65 | Cosine distance threshold for RAG |
| `HISTORY_TURNS` | 20 | Conversation turns injected into prompt |
| `WHISPER_MODEL` | base | Whisper model size |
| `LISTEN_SECONDS` | 6 | Audio capture window (seconds) |
| `OLLAMA_TIMEOUT` | 120 s | LLM generation timeout |
| `BRIEFING_TIME` | 08:00 | Morning automation schedule |
| `WIND_DOWN_TIME` | 21:30 | Evening reminder schedule |

---

## Appendix B: Ablation Query Breakdown

For transparency, the 500-query routing distribution sample comprised the following approximate categories:

| Query Type | Approximate Count | Primary Route |
|---|---|---|
| System control (apps, volume, power) | 142 | Stage 2 (tool) |
| Time, date, system stats | 89 | Stage 2 (tool) |
| Notes, reminders, tasks | 55 | Stage 2 (tool) |
| Web search, weather | 32 | Stage 2 (tool) |
| Conversational / factual | 98 | Stage 3 (llama3b) |
| Explanation / planning | 37 | Stage 3 (qwen7b) |
| Technical / code | 28 | Stage 3 (qwen7b or codellama) |
| Screen / vision | 6 | Stage 1 (llava) |
| Ambiguous / uncategorized | 13 | Stage 3 (varies) |

---

## Appendix C: Reproducibility

Source code: https://github.com/betheaayush/edith-v8

```bash
# 1. Setup
bash scripts/setup.sh

# 2. Pull models
ollama pull llama3.2:3b
ollama pull nomic-embed-text
ollama pull qwen2.5:7b
ollama pull codellama:7b

# 3. Launch
bash scripts/start.sh

# 4. Benchmarks (30 trials, 5 warmup)
python benchmarks/run_latency.py --trials 30 --warmup 5
python benchmarks/run_ablation_routing.py
python benchmarks/run_ablation_rag.py
```

Results vary with hardware. All figures reported here were collected on the hardware in Section 4.2. Q4\_K\_M quantization was used throughout; different quantization levels will produce different RAM and latency values.

---

*Prepared for undergraduate research submission, MIT-ADT University, Pune, May 2026.*  
*EDITH V8 is released under the MIT License. Copyright © 2026 Aayush Sahu.*
