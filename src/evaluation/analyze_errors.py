from __future__ import annotations

from pathlib import Path

import matplotlib
import pandas as pd


matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _format_label(text: str) -> str:
    return str(text).replace("_", " ").title()


def run_error_analysis(base_dir: str | Path = ".") -> dict[str, Path]:
    base_dir = Path(base_dir)
    results_dir = base_dir / "data" / "eval" / "results"
    detail_path = results_dir / "compare_bm25_embedding_hybrid_detail.csv"

    detail_df = pd.read_csv(detail_path)

    by_mode = (
        detail_df.groupby(["retrieval_mode", "failure_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["retrieval_mode", "count"], ascending=[True, False])
    )
    by_issue = (
        detail_df.groupby(["issue_category", "failure_type"])
        .size()
        .reset_index(name="count")
        .sort_values(["issue_category", "count"], ascending=[True, False])
    )

    mode_csv = results_dir / "error_analysis_by_mode.csv"
    issue_csv = results_dir / "error_analysis_by_issue.csv"
    mode_plot = results_dir / "error_analysis_by_mode.png"
    issue_plot = results_dir / "error_analysis_by_issue.png"

    by_mode.to_csv(mode_csv, index=False)
    by_issue.to_csv(issue_csv, index=False)

    mode_pivot = (
        by_mode.pivot(index="retrieval_mode", columns="failure_type", values="count")
        .fillna(0)
        .sort_index()
    )
    issue_pivot = (
        by_issue.pivot(index="issue_category", columns="failure_type", values="count")
        .fillna(0)
        .sort_index()
    )

    mode_pivot.index = [_format_label(value) for value in mode_pivot.index]
    mode_pivot.columns = [_format_label(value) for value in mode_pivot.columns]
    issue_pivot.index = [_format_label(value) for value in issue_pivot.index]
    issue_pivot.columns = [_format_label(value) for value in issue_pivot.columns]

    palette = ["#5B7C99", "#A7B1BC", "#7B6D9C", "#4A5A6A", "#B39DDB"]

    plt.figure(figsize=(8, 4.5))
    mode_pivot.plot(kind="bar", stacked=True, ax=plt.gca(), color=palette)
    plt.xlabel("Retrieval Mode")
    plt.ylabel("Question Count")
    plt.title("Failure Types by Retrieval Mode")
    plt.xticks(rotation=0, ha="center")
    plt.legend(title="Failure Type", loc="lower left")
    plt.tight_layout()
    plt.savefig(mode_plot)
    plt.close()

    plt.figure(figsize=(8, 4.5))
    issue_pivot.plot(kind="bar", stacked=True, ax=plt.gca(), color=palette)
    plt.xlabel("Issue Category")
    plt.ylabel("Question Count")
    plt.title("Failure Types by Issue Category")
    plt.xticks(rotation=0, ha="center")
    plt.legend(title="Failure Type", loc="upper left")
    plt.tight_layout()
    plt.savefig(issue_plot)
    plt.close()

    return {
        "by_mode_csv": mode_csv,
        "by_issue_csv": issue_csv,
        "by_mode_plot": mode_plot,
        "by_issue_plot": issue_plot,
    }


if __name__ == "__main__":
    paths = run_error_analysis()
    for name, path in paths.items():
        print(f"Saved {name}: {path}")
