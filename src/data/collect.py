from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import SETTINGS
from src.data.metadata import SourceDocument
from src.utils.io import read_text


def load_source_index(base_dir: str | Path = ".") -> pd.DataFrame:
    index_path = Path(base_dir) / SETTINGS.raw_data_dir / "source_index.csv"
    return pd.read_csv(index_path)


def load_documents(base_dir: str | Path = ".") -> list[SourceDocument]:
    base_path = Path(base_dir)
    raw_dir = base_path / SETTINGS.raw_data_dir
    rows = load_source_index(base_dir=base_path)
    documents: list[SourceDocument] = []

    for row in rows.itertuples(index=False):
        text_path = raw_dir / row.file_name
        documents.append(
            SourceDocument(
                doc_id=row.doc_id,
                title=row.title,
                source_url=row.source_url,
                source_type=row.source_type,
                jurisdiction=row.jurisdiction,
                county=row.county,
                issue_category=row.issue_category,
                file_name=row.file_name,
                text=read_text(text_path),
            )
        )

    return documents
