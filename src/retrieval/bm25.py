from __future__ import annotations

from rank_bm25 import BM25Okapi

from src.data.chunk import TextChunk


class BM25Retriever:
    def __init__(self, chunks: list[TextChunk]) -> None:
        self.chunks = chunks
        self.tokenized_corpus = [chunk.text.lower().split() for chunk in chunks]
        self.index = BM25Okapi(self.tokenized_corpus)

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        scores = self.index.get_scores(query.lower().split())
        ranked = sorted(
            zip(self.chunks, scores),
            key=lambda item: item[1],
            reverse=True,
        )[:top_k]
        return [
            {"chunk": chunk, "score": float(score), "method": "bm25"}
            for chunk, score in ranked
        ]
