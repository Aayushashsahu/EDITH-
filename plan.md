1. Modify `backend/memory/brain.py` to optimize `_embed_all` by replacing the sequential list comprehension `[await self.llm.embed(t) for t in texts]` with concurrent batched execution using `asyncio.gather` (batch size 5).
2. Apply the identical optimization to the mirror file `edith/backend/memory/brain.py`.
3. Create/update `.jules/bolt.md` with a journal entry noting the performance optimization around sequential awaits vs local LLM limits.
4. Run tests: `python -m unittest discover tests/` to verify correctness.
5. Pre-commit step to ensure proper testing, verification, review, and reflection are done.
6. Submit the change.
