from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    project_name: str = "HomeHelp NC"
    raw_data_dir: str = "data/raw"
    processed_data_dir: str = "data/processed"
    eval_data_dir: str = "data/eval"
    generation_provider: str = os.getenv("GENERATION_PROVIDER", "gemini")
    generation_model: str = os.getenv("GENERATION_MODEL", "gemini-2.5-flash")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2",
    )
    top_k: int = int(os.getenv("TOP_K", "5"))


SETTINGS = Settings()
