from __future__ import annotations

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.config import SETTINGS
from src.data.chunk import TextChunk


class EmbeddingRetriever:
    def __init__(self, chunks: list[TextChunk]) -> None:
        self.chunks = chunks
        self.model = SentenceTransformer(
            SETTINGS.embedding_model,
            local_files_only=True,
        )
        self.chunk_embeddings = self.model.encode(
            [chunk.text for chunk in chunks],
            normalize_embeddings=True,
        )

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_embedding = self.model.encode([query], normalize_embeddings=True)
        similarities = cosine_similarity(query_embedding, self.chunk_embeddings)[0]
        ranked_indices = similarities.argsort()[::-1][:top_k]
        return [
            {
                "chunk": self.chunks[idx],
                "score": float(similarities[idx]),
                "method": "embedding",
            }
            for idx in ranked_indices
        ]
