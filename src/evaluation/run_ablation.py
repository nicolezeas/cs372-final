from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
import pandas as pd

from src.data.chunk import chunk_documents
from src.data.clean import clean_documents
from src.data.collect import load_documents
from src.evaluation.run_retrieval_eval import load_eval_questions, run_eval, run_eval_with_retriever
from src.retrieval.hybrid import HybridRetriever


matplotlib.use("Agg")
import matplotlib.pyplot as plt


def run_chunk_ablation(
    base_dir: str | Path = ".",
    top_k: int = 5,
    chunk_sizes: list[int] | None = None,
    overlap: int = 40,
    retrieval_mode: str = "bm25_reranked",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    chunk_sizes = chunk_sizes or [150, 200, 250]

    detail_frames: list[pd.DataFrame] = []
    for chunk_size in chunk_sizes:
        detail_df, _ = run_eval(
            base_dir=base_dir,
            retrieval_mode=retrieval_mode,
            top_k=top_k,
            words_per_chunk=chunk_size,
            overlap=overlap,
        )
        detail_frames.append(detail_df)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = (
        detail_df.groupby(["retrieval_mode", "words_per_chunk", "overlap", "top_k"])[
            ["precision_at_k", "recall_at_k", "hit_at_k"]
        ]
        .mean()
        .reset_index()
        .sort_values("hit_at_k", ascending=False)
    )
    return detail_df, summary_df


def run_topk_ablation(
    base_dir: str | Path = ".",
    chunk_size: int = 200,
    overlap: int = 40,
    top_ks: list[int] | None = None,
    retrieval_mode: str = "bm25_reranked",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    top_ks = top_ks or [3, 5, 7]

    detail_frames: list[pd.DataFrame] = []
    for top_k in top_ks:
        detail_df, _ = run_eval(
            base_dir=base_dir,
            retrieval_mode=retrieval_mode,
            top_k=top_k,
            words_per_chunk=chunk_size,
            overlap=overlap,
        )
        detail_frames.append(detail_df)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = (
        detail_df.groupby(["retrieval_mode", "words_per_chunk", "overlap", "top_k"])[
            ["precision_at_k", "recall_at_k", "hit_at_k"]
        ]
        .mean()
        .reset_index()
        .sort_values("hit_at_k", ascending=False)
    )
    return detail_df, summary_df


def run_method_ablation(
    base_dir: str | Path = ".",
    top_k: int = 5,
    words_per_chunk: int = 200,
    overlap: int = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    documents = clean_documents(load_documents(base_dir=base_dir))
    chunks = chunk_documents(
        documents,
        words_per_chunk=words_per_chunk,
        overlap=overlap,
    )
    questions = load_eval_questions(base_dir=base_dir)

    configs = [
        {
            "label": "bm25_only",
            "use_embeddings": False,
            "use_heuristics": False,
        },
        {
            "label": "bm25_plus_heuristics",
            "use_embeddings": False,
            "use_heuristics": True,
        },
        {
            "label": "bm25_plus_embeddings",
            "use_embeddings": True,
            "use_heuristics": False,
        },
        {
            "label": "bm25_plus_embeddings_plus_heuristics",
            "use_embeddings": True,
            "use_heuristics": True,
        },
    ]

    detail_frames: list[pd.DataFrame] = []
    for config in configs:
        retriever = HybridRetriever(
            chunks,
            use_embeddings=config["use_embeddings"],
            use_heuristics=config["use_heuristics"],
            max_chunks_per_doc=2,
        )
        detail_df, _ = run_eval_with_retriever(
            retriever=retriever,
            questions=questions,
            retrieval_label=config["label"],
            top_k=top_k,
            words_per_chunk=words_per_chunk,
            overlap=overlap,
        )
        detail_df["use_embeddings"] = config["use_embeddings"]
        detail_df["use_heuristics"] = config["use_heuristics"]
        detail_frames.append(detail_df)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = (
        detail_df.groupby(["retrieval_mode", "use_embeddings", "use_heuristics", "words_per_chunk", "overlap", "top_k"])[
            ["precision_at_k", "recall_at_k", "hit_at_k"]
        ]
        .mean()
        .reset_index()
        .sort_values("hit_at_k", ascending=False)
    )
    return detail_df, summary_df


def save_ablation_outputs(
    detail_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    out_dir: Path,
    label: str,
    x_col: str,
) -> dict[str, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    detail_path = out_dir / f"{label}_detail.csv"
    summary_path = out_dir / f"{label}_summary.csv"
    plot_path = out_dir / f"{label}_plot.png"

    detail_df.to_csv(detail_path, index=False)
    summary_df.to_csv(summary_path, index=False)

    plt.figure(figsize=(7, 4))
    is_categorical = summary_df[x_col].dtype == "object"
    for metric in ["precision_at_k", "recall_at_k", "hit_at_k"]:
        if is_categorical:
            plt.plot(summary_df[x_col].astype(str), summary_df[metric], marker="o", label=metric)
        else:
            plt.plot(summary_df[x_col], summary_df[metric], marker="o", label=metric)
    plt.xlabel(x_col)
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.title(f"Ablation: {label}")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return {
        "detail": detail_path,
        "summary": summary_path,
        "plot": plot_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run ablation studies for HomeHelp NC retrieval.")
    parser.add_argument("--study", choices=["chunk_size", "top_k", "method"], required=True)
    parser.add_argument("--mode", choices=["bm25", "bm25_reranked", "hybrid"], default="bm25_reranked")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    base_dir = Path(".")
    out_dir = base_dir / "data" / "eval" / "results"

    if args.study == "chunk_size":
        detail_df, summary_df = run_chunk_ablation(
            base_dir=base_dir,
            retrieval_mode=args.mode,
        )
        paths = save_ablation_outputs(
            detail_df,
            summary_df,
            out_dir=out_dir,
            label=f"ablation_chunk_size_{args.mode}",
            x_col="words_per_chunk",
        )
    elif args.study == "top_k":
        detail_df, summary_df = run_topk_ablation(
            base_dir=base_dir,
            retrieval_mode=args.mode,
        )
        paths = save_ablation_outputs(
            detail_df,
            summary_df,
            out_dir=out_dir,
            label=f"ablation_top_k_{args.mode}",
            x_col="top_k",
        )
    else:
        detail_df, summary_df = run_method_ablation(
            base_dir=base_dir,
        )
        paths = save_ablation_outputs(
            detail_df,
            summary_df,
            out_dir=out_dir,
            label="ablation_method_retrieval",
            x_col="retrieval_mode",
        )

    print(summary_df.to_string(index=False))
    print()
    for name, path in paths.items():
        print(f"Saved {name}: {path}")
