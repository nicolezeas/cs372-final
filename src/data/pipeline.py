from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from src.config import SETTINGS
from src.data.chunk import TextChunk, chunk_documents
from src.data.clean import clean_documents
from src.data.collect import load_documents
from src.utils.io import ensure_dir


def build_chunk_records(base_dir: str | Path = ".") -> list[TextChunk]:
    documents = load_documents(base_dir=base_dir)
    cleaned = clean_documents(documents)
    return chunk_documents(cleaned)


def save_processed_chunks(base_dir: str | Path = ".") -> Path:
    base_path = Path(base_dir)
    processed_dir = ensure_dir(base_path / SETTINGS.processed_data_dir)
    output_path = processed_dir / "chunks.json"
    chunk_records = [asdict(chunk) for chunk in build_chunk_records(base_dir=base_path)]
    output_path.write_text(json.dumps(chunk_records, indent=2), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    output = save_processed_chunks()
    print(f"Saved processed chunks to {output}")
