from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AblationConfig:
    words_per_chunk: int
    overlap: int
    top_k: int
    use_hybrid: bool
