from __future__ import annotations

from collections.abc import Iterable


def precision_at_k(retrieved_doc_ids: Iterable[str], relevant_doc_ids: set[str], k: int) -> float:
    top_ids = list(dict.fromkeys(retrieved_doc_ids))[:k]
    if not top_ids:
        return 0.0
    hits = sum(1 for doc_id in top_ids if doc_id in relevant_doc_ids)
    return hits / len(top_ids)


def recall_at_k(retrieved_doc_ids: Iterable[str], relevant_doc_ids: set[str], k: int) -> float:
    top_ids = list(dict.fromkeys(retrieved_doc_ids))[:k]
    if not relevant_doc_ids:
        return 0.0
    hits = sum(1 for doc_id in top_ids if doc_id in relevant_doc_ids)
    return hits / len(relevant_doc_ids)
