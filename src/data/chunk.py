from __future__ import annotations

from dataclasses import dataclass

from src.data.metadata import SourceDocument


@dataclass
class TextChunk:
    chunk_id: str
    doc_id: str
    title: str
    issue_category: str
    source_url: str
    text: str


def chunk_text(text: str, words_per_chunk: int = 200, overlap: int = 40) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = min(len(words), start + words_per_chunk)
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start = max(end - overlap, start + 1)
    return chunks


def chunk_documents(
    documents: list[SourceDocument],
    words_per_chunk: int = 200,
    overlap: int = 40,
) -> list[TextChunk]:
    output: list[TextChunk] = []
    for doc in documents:
        for idx, chunk in enumerate(
            chunk_text(doc.text, words_per_chunk=words_per_chunk, overlap=overlap)
        ):
            output.append(
                TextChunk(
                    chunk_id=f"{doc.doc_id}_chunk_{idx}",
                    doc_id=doc.doc_id,
                    title=doc.title,
                    issue_category=doc.issue_category,
                    source_url=doc.source_url,
                    text=chunk,
                )
            )
    return output
