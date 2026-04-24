from __future__ import annotations

from collections import defaultdict
import re

from src.retrieval.bm25 import BM25Retriever
from src.retrieval.embeddings import EmbeddingRetriever


class HybridRetriever:
    def __init__(
        self,
        chunks: list,
        use_embeddings: bool = True,
        use_heuristics: bool = True,
        max_chunks_per_doc: int = 2,
    ) -> None:
        self.bm25 = BM25Retriever(chunks)
        self.use_embeddings = use_embeddings
        self.use_heuristics = use_heuristics
        self.max_chunks_per_doc = max_chunks_per_doc
        self.embedding = None
        self.embedding_error: str | None = None
        if self.use_embeddings:
            try:
                self.embedding = EmbeddingRetriever(chunks)
            except Exception as exc:  # pragma: no cover - fallback for offline/dev environments
                self.embedding_error = str(exc)

    def _normalize(self, text: str) -> str:
        return re.sub(r"\s+", " ", text.lower()).strip()

    def _query_keywords(self, query: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", self._normalize(query)))

    def _infer_issue_hints(self, query: str) -> set[str]:
        q = self._normalize(query)
        hints: set[str] = set()

        if any(word in q for word in {"appeal", "appeals", "appealing"}):
            hints.add("eviction")
        if any(word in q for word in {"evict", "eviction", "lockout", "padlock", "writ"}):
            hints.update({"eviction", "lockout"})
        if any(word in q for word in {"deposit", "security deposit"}):
            hints.add("security_deposit")
        if any(word in q for word in {"utility", "utilities", "water", "power", "electric", "gas", "shut off", "shutoff"}):
            hints.add("utility_shutoff")
        if any(word in q for word in {"repair", "repairs", "habitability", "mold", "heat", "plumbing"}):
            hints.add("habitability")
        if any(word in q for word in {"month-to-month", "month to month", "notice", "lease termination", "terminate lease"}):
            hints.add("lease_termination")

        return hints

    def _source_priority_bonus(self, source_url: str) -> float:
        url = source_url.lower()
        if "nccourts.gov" in url or "ncleg.gov" in url or "ncleg.net" in url:
            return 2.4
        if "legalaidnc.org" in url:
            return 1.1
        if "hemlane.com" in url or "turbotenant.com" in url:
            return -0.5
        return 0.0

    def _heuristic_bonus(self, query: str, chunk) -> float:
        q = self._normalize(query)
        q_keywords = self._query_keywords(query)
        title = self._normalize(chunk.title)
        text = self._normalize(chunk.text[:600])
        issue = (chunk.issue_category or "").lower()

        bonus = 0.0

        issue_hints = self._infer_issue_hints(query)
        if issue and issue in issue_hints:
            bonus += 2.5
        if issue == "housing_general":
            bonus -= 0.4

        title_keyword_hits = sum(1 for word in q_keywords if len(word) > 3 and word in title)
        bonus += min(title_keyword_hits * 0.45, 1.8)

        if "appeal" in q and "10 days" in text:
            bonus += 1.8
        if "security deposit" in q and ("30 days" in text or "60 days" in text):
            bonus += 1.8
        if any(term in q for term in {"utilities", "utility", "water", "power", "gas"}) and (
            "may not disconnect" in text or "cannot force tenants out" in text
        ):
            bonus += 2.0
        if any(term in q for term in {"lockout", "lock me out", "court order", "locks"}) and (
            "cannot lock out" in text or "cannot force tenants out" in text or "changing the locks" in text
        ):
            bonus += 2.0
        if "month-to-month" in q or "month to month" in q:
            if "7 days" in text and "42-14" in text:
                bonus += 2.6
            elif "7 days" in text:
                bonus += 1.2
        if "security deposit" in q and ("42-52" in text or "tenant security deposit act" in text):
            bonus += 1.2
        if "appeal" in q and ("notice of appeal" in text or "district court" in text):
            bonus += 1.0

        if "small claims" in title and not any(term in q for term in {"small claims", "magistrate", "court", "hearing"}):
            bonus -= 0.9

        bonus += self._source_priority_bonus(chunk.source_url)
        return bonus

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        bm25_results = self.bm25.search(query, top_k=top_k)
        embedding_results: list[dict] = []
        if self.embedding is not None:
            embedding_results = self.embedding.search(query, top_k=top_k)

        merged: dict[str, dict] = defaultdict(dict)

        for result in bm25_results + embedding_results:
            chunk = result["chunk"]
            chunk_id = chunk.chunk_id
            if not merged[chunk_id]:
                merged[chunk_id] = {"chunk": chunk, "score": 0.0, "methods": []}
            merged[chunk_id]["score"] += result["score"]
            merged[chunk_id]["methods"].append(result["method"])

        if self.use_heuristics:
            for item in merged.values():
                item["score"] += self._heuristic_bonus(query, item["chunk"])

        ranked = sorted(merged.values(), key=lambda item: item["score"], reverse=True)

        # Encourage source diversity so one document does not take over the result set.
        selected: list[dict] = []
        per_doc_counts: dict[str, int] = defaultdict(int)

        for item in ranked:
            chunk = item["chunk"]
            if per_doc_counts[chunk.doc_id] >= self.max_chunks_per_doc:
                continue
            selected.append(item)
            per_doc_counts[chunk.doc_id] += 1
            if len(selected) == top_k:
                break

        return selected
