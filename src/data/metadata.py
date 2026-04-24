from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceDocument:
    doc_id: str
    title: str
    source_url: str
    source_type: str
    jurisdiction: str
    county: str
    issue_category: str
    file_name: str
    text: str
