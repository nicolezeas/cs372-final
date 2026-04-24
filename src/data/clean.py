from __future__ import annotations

import re
from typing import Iterable

from src.data.metadata import SourceDocument


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_repeated_boilerplate(text: str) -> str:
    patterns = [
        r"(?im)^skip to main content.*$",
        r"(?im)^back to top.*$",
        r"(?im)^copyright.*$",
    ]
    cleaned = text
    for pattern in patterns:
        cleaned = re.sub(pattern, "", cleaned)
    return cleaned


def clean_document_text(text: str) -> str:
    return normalize_whitespace(strip_repeated_boilerplate(text))


def clean_documents(documents: Iterable[SourceDocument]) -> list[SourceDocument]:
    cleaned_docs: list[SourceDocument] = []
    for doc in documents:
        cleaned_docs.append(
            SourceDocument(
                doc_id=doc.doc_id,
                title=doc.title,
                source_url=doc.source_url,
                source_type=doc.source_type,
                jurisdiction=doc.jurisdiction,
                county=doc.county,
                issue_category=doc.issue_category,
                file_name=doc.file_name,
                text=clean_document_text(doc.text),
                issue_tags=doc.issue_tags,
            )
        )
    return cleaned_docs
