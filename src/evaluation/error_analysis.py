from __future__ import annotations

import pandas as pd


def summarize_failures(results: pd.DataFrame) -> pd.DataFrame:
    return (
        results.groupby("failure_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
