"""
E.D.I.T.H. V8 — Second Brain
ChromaDB vector store with Ollama nomic-embed-text embeddings.
Drop files into data/second_brain/ and they auto-ingest on startup.
"""

import os
import asyncio
from pathlib import Path
import chromadb
from backend.agents.llm import LLMClient
from config.config import CHROMA_DIR, BRAIN_DIR, CHUNK_SIZE, CHUNK_OVERLAP, RETRIEVAL_K, RELEVANCE_CUTOFF


class SecondBrain:
    def __init__(self):
        os.makedirs(str(CHROMA_DIR), exist_ok=True)
        os.makedirs(str(BRAIN_DIR),  exist_ok=True)
        self.llm    = LLMClient()
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.col    = self.client.get_or_create_collection(
            "edith_brain", metadata={"hnsw:space": "cosine"}
        )

    async def init(self):
        """Auto-ingest new files from BRAIN_DIR on startup."""
        for f in Path(BRAIN_DIR).rglob("*"):
            if f.suffix.lower() in (".txt", ".md", ".pdf"):
                existing = self.col.get(where={"source": f.name}, limit=1)
                if not existing["ids"]:
                    print(f"  [Brain]  Auto-ingesting: {f.name}")
                    await self.ingest_file(str(f))

    def count(self) -> int:
        return self.col.count()

    # ── Ingestion ─────────────────────────────────────────────────────────────
    async def ingest_text(self, text: str, source: str = "manual") -> int:
        chunks = self._chunk(text)
        if not chunks:
            return 0
        embeddings = await self._embed_all(chunks)
        if not embeddings or not all(embeddings):
            return 0
        ids = [f"{source}_{abs(hash(c)) % 10**9}" for c in chunks]
        self.col.upsert(
            documents=chunks, embeddings=embeddings, ids=ids,
            metadatas=[{"source": source}] * len(chunks)
        )
        return len(chunks)

    async def ingest_file(self, filepath: str) -> int:
        p = Path(filepath)
        if not p.exists():
            return 0
        if p.suffix.lower() == ".pdf":
            text = self._read_pdf(filepath)
        else:
            text = p.read_text(errors="ignore")
        return await self.ingest_text(text, source=p.name)

    # ── Retrieval ─────────────────────────────────────────────────────────────
    async def retrieve(self, query: str, k: int = RETRIEVAL_K) -> str:
        if self.count() == 0:
            return ""
        emb = await self.llm.embed(query)
        if not emb:
            return ""
        k = min(k, self.count())
        res = self.col.query(
            query_embeddings=[emb], n_results=k,
            include=["documents", "distances"]
        )
        docs  = res["documents"][0]
        dists = res["distances"][0]
        hits  = [d for d, dist in zip(docs, dists) if dist < RELEVANCE_CUTOFF]
        return "\n---\n".join(hits)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _chunk(self, text: str) -> list:
        words  = text.split()
        chunks, i = [], 0
        while i < len(words):
            c = " ".join(words[i: i + CHUNK_SIZE])
            if len(c.strip()) > 60:
                chunks.append(c)
            i += CHUNK_SIZE - CHUNK_OVERLAP
        return chunks

    async def _embed_all(self, texts: list) -> list:
        # Avoid sequential execution; batch API calls concurrently to prevent local system overload
        results = []
        batch_size = 5
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            results.extend(await asyncio.gather(*(self.llm.embed(t) for t in batch)))
        return results

    def _read_pdf(self, path: str) -> str:
        try:
            import fitz
            return "\n".join(p.get_text() for p in fitz.open(path))
        except ImportError:
            return "[PDF support: pip install pymupdf]"
        except Exception as e:
            return f"[PDF error: {e}]"
