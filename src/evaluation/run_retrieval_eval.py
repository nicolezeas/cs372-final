from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
from pathlib import Path

import matplotlib
import pandas as pd

from src.data.chunk import chunk_documents
from src.data.clean import clean_documents
from src.data.collect import load_documents
from src.evaluation.retrieval_eval import precision_at_k, recall_at_k
from src.retrieval.bm25 import BM25Retriever
from src.retrieval.embeddings import EmbeddingRetriever
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.retrieval.hybrid import HybridRetriever


MODE_LABELS = {
    "bm25": "BM25",
    "embedding": "Embedding",
    "hybrid": "Hybrid",
    "bm25_reranked": "BM25 + Heuristics",
}

METRIC_COLORS = {
    "precision_at_k": "#5B7C99",
    "recall_at_k": "#A7B3C0",
    "hit_at_k": "#7C6A9E",
}


def load_eval_questions(base_dir: str | Path = ".") -> list[dict]:
    eval_path = Path(base_dir) / "data" / "eval" / "eval_questions.csv"
    with eval_path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_chunks(
    base_dir: str | Path = ".",
    words_per_chunk: int = 200,
    overlap: int = 40,
):
    documents = clean_documents(load_documents(base_dir=base_dir))
    return chunk_documents(
        documents,
        words_per_chunk=words_per_chunk,
        overlap=overlap,
    )


def get_retriever(chunks: list, mode: str):
    if mode == "bm25":
        return BM25Retriever(chunks)
    if mode == "embedding":
        return EmbeddingRetriever(chunks)
    if mode == "bm25_reranked":
        return HybridRetriever(
            chunks,
            use_embeddings=False,
            use_heuristics=True,
            max_chunks_per_doc=2,
        )
    if mode == "hybrid":
        return HybridRetriever(
            chunks,
            use_embeddings=True,
            use_heuristics=True,
            max_chunks_per_doc=2,
        )
    raise ValueError(f"Unsupported retrieval mode: {mode}")


def run_eval_with_retriever(
    retriever,
    questions: list[dict],
    retrieval_label: str,
    top_k: int = 5,
    words_per_chunk: int = 200,
    overlap: int = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows: list[dict] = []
    for question in questions:
        expected_doc_ids = set(question["expected_doc_ids"].split("|"))
        results = retriever.search(question["question_text"], top_k=top_k)
        normalized = normalize_results(results)
        retrieved_doc_ids = [item["doc_id"] for item in normalized]
        unique_retrieved_doc_ids = list(dict.fromkeys(retrieved_doc_ids))
        top_doc_ids = "|".join(retrieved_doc_ids)
        top_titles = " | ".join(item["title"] for item in normalized)
        p_at_k = precision_at_k(unique_retrieved_doc_ids, expected_doc_ids, top_k)
        r_at_k = recall_at_k(unique_retrieved_doc_ids, expected_doc_ids, top_k)
        hit_at_k = 1.0 if any(doc_id in expected_doc_ids for doc_id in unique_retrieved_doc_ids[:top_k]) else 0.0
        rows.append(
            {
                "question_id": question["question_id"],
                "question_text": question["question_text"],
                "issue_category": question["issue_category"],
                "retrieval_mode": retrieval_label,
                "top_k": top_k,
                "words_per_chunk": words_per_chunk,
                "overlap": overlap,
                "expected_doc_ids": question["expected_doc_ids"],
                "retrieved_doc_ids": top_doc_ids,
                "retrieved_titles": top_titles,
                "precision_at_k": p_at_k,
                "recall_at_k": r_at_k,
                "hit_at_k": hit_at_k,
                "failure_type": classify_failure(unique_retrieved_doc_ids, expected_doc_ids, top_k),
            }
        )

    detail_df = pd.DataFrame(rows)
    summary_df = (
        detail_df.groupby("retrieval_mode")[["precision_at_k", "recall_at_k", "hit_at_k"]]
        .mean()
        .reset_index()
        .sort_values("hit_at_k", ascending=False)
    )
    return detail_df, summary_df


def normalize_results(results: list[dict]) -> list[dict]:
    normalized: list[dict] = []
    for item in results:
        normalized.append(
            {
                "doc_id": item["chunk"].doc_id,
                "title": item["chunk"].title,
                "url": item["chunk"].source_url,
                "issue_category": item["chunk"].issue_category,
                "score": float(item.get("score", 0.0)),
                "methods": ",".join(item.get("methods", [item.get("method", "unknown")])),
            }
        )
    return normalized


def classify_failure(retrieved_doc_ids: list[str], expected_doc_ids: set[str], top_k: int) -> str:
    top_ids = list(dict.fromkeys(retrieved_doc_ids))[:top_k]
    if any(doc_id in expected_doc_ids for doc_id in top_ids):
        if all(doc_id in top_ids for doc_id in expected_doc_ids):
            return "none"
        return "partial_retrieval"
    return "missed_relevant_source"


def run_eval(
    base_dir: str | Path = ".",
    retrieval_mode: str = "hybrid",
    top_k: int = 5,
    words_per_chunk: int = 200,
    overlap: int = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    chunks = build_chunks(base_dir=base_dir, words_per_chunk=words_per_chunk, overlap=overlap)
    retriever = get_retriever(chunks, retrieval_mode)
    questions = load_eval_questions(base_dir=base_dir)
    return run_eval_with_retriever(
        retriever=retriever,
        questions=questions,
        retrieval_label=retrieval_mode,
        top_k=top_k,
        words_per_chunk=words_per_chunk,
        overlap=overlap,
    )


def save_outputs(
    detail_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    base_dir: str | Path = ".",
    label: str = "hybrid",
) -> dict[str, Path]:
    out_dir = Path(base_dir) / "data" / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)

    detail_path = out_dir / f"{label}_detail.csv"
    summary_path = out_dir / f"{label}_summary.csv"
    plot_path = out_dir / f"{label}_summary.png"
    failure_path = out_dir / f"{label}_failures.csv"

    detail_df.to_csv(detail_path, index=False)
    summary_df.to_csv(summary_path, index=False)

    failure_df = (
        detail_df.groupby("failure_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )
    failure_df.to_csv(failure_path, index=False)

    plot_df = summary_df.copy()
    plot_df["retrieval_mode"] = plot_df["retrieval_mode"].map(lambda mode: MODE_LABELS.get(mode, mode.replace("_", " ").title()))
    plot_df["mode_order"] = plot_df["retrieval_mode"].map(
        {
            "BM25": 0,
            "Embedding": 1,
            "Hybrid": 2,
            "BM25 + Heuristics": 3,
        }
    )
    plot_df = plot_df.sort_values("mode_order")

    metrics = ["precision_at_k", "recall_at_k", "hit_at_k"]
    top_k_value = int(detail_df["top_k"].iloc[0]) if not detail_df.empty else 5
    metric_labels = {
        "precision_at_k": f"Precision @ {top_k_value}",
        "recall_at_k": f"Recall @ {top_k_value}",
        "hit_at_k": f"Hit @ {top_k_value}",
    }
    x_positions = range(len(plot_df))
    bar_width = 0.24

    plt.figure(figsize=(8.2, 4.8))
    for index, metric in enumerate(metrics):
        offsets = [x + (index - 1) * bar_width for x in x_positions]
        plt.bar(
            offsets,
            plot_df[metric],
            width=bar_width,
            label=metric_labels[metric],
            color=METRIC_COLORS[metric],
        )
    plt.ylim(0, 1)
    plt.xticks(list(x_positions), plot_df["retrieval_mode"])
    plt.ylabel("Score")
    plt.xlabel("Retrieval Mode")
    plt.title("Retrieval Evaluation Summary")
    plt.legend(title="Metric")
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    return {
        "detail": detail_path,
        "summary": summary_path,
        "failures": failure_path,
        "plot": plot_path,
    }


def run_comparison(
    base_dir: str | Path = ".",
    modes: list[str] | None = None,
    top_k: int = 5,
    words_per_chunk: int = 200,
    overlap: int = 40,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    modes = modes or ["bm25", "hybrid"]
    detail_frames: list[pd.DataFrame] = []
    summary_frames: list[pd.DataFrame] = []

    chunks = build_chunks(base_dir=base_dir, words_per_chunk=words_per_chunk, overlap=overlap)
    questions = load_eval_questions(base_dir=base_dir)

    for mode in modes:
        retriever = get_retriever(chunks, mode)
        rows: list[dict] = []
        for question in questions:
            expected_doc_ids = set(question["expected_doc_ids"].split("|"))
            results = retriever.search(question["question_text"], top_k=top_k)
            normalized = normalize_results(results)
            retrieved_doc_ids = [item["doc_id"] for item in normalized]
            unique_retrieved_doc_ids = list(dict.fromkeys(retrieved_doc_ids))
            rows.append(
                {
                    "question_id": question["question_id"],
                    "question_text": question["question_text"],
                    "issue_category": question["issue_category"],
                    "retrieval_mode": mode,
                    "top_k": top_k,
                    "words_per_chunk": words_per_chunk,
                    "overlap": overlap,
                    "expected_doc_ids": question["expected_doc_ids"],
                    "retrieved_doc_ids": "|".join(retrieved_doc_ids),
                    "retrieved_titles": " | ".join(item["title"] for item in normalized),
                    "precision_at_k": precision_at_k(unique_retrieved_doc_ids, expected_doc_ids, top_k),
                    "recall_at_k": recall_at_k(unique_retrieved_doc_ids, expected_doc_ids, top_k),
                    "hit_at_k": 1.0 if any(doc_id in expected_doc_ids for doc_id in unique_retrieved_doc_ids[:top_k]) else 0.0,
                    "failure_type": classify_failure(unique_retrieved_doc_ids, expected_doc_ids, top_k),
                }
            )
        detail_frames.append(pd.DataFrame(rows))

    detail_df = pd.concat(detail_frames, ignore_index=True)
    summary_df = (
        detail_df.groupby("retrieval_mode")[["precision_at_k", "recall_at_k", "hit_at_k"]]
        .mean()
        .reset_index()
        .sort_values("hit_at_k", ascending=False)
    )
    return detail_df, summary_df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run retrieval evaluation for HomeHelp NC.")
    parser.add_argument("--mode", choices=["bm25", "embedding", "bm25_reranked", "hybrid"], default="bm25_reranked")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--words-per-chunk", type=int, default=200)
    parser.add_argument("--overlap", type=int, default=40)
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Run a controlled comparison between bm25, embedding, and hybrid on the same eval set.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    base_dir = Path(".")

    if args.compare:
        detail_df, summary_df = run_comparison(
            base_dir=base_dir,
            modes=["bm25", "embedding", "hybrid"],
            top_k=args.top_k,
            words_per_chunk=args.words_per_chunk,
            overlap=args.overlap,
        )
        paths = save_outputs(detail_df, summary_df, base_dir=base_dir, label="compare_bm25_embedding_hybrid")
        print(summary_df.to_string(index=False))
        print()
        for name, path in paths.items():
            print(f"Saved {name}: {path}")
    else:
        detail_df, summary_df = run_eval(
            base_dir=base_dir,
            retrieval_mode=args.mode,
            top_k=args.top_k,
            words_per_chunk=args.words_per_chunk,
            overlap=args.overlap,
        )
        label = f"{args.mode}_k{args.top_k}_w{args.words_per_chunk}_o{args.overlap}"
        paths = save_outputs(detail_df, summary_df, base_dir=base_dir, label=label)
        print(summary_df.to_string(index=False))
        print()
        for name, path in paths.items():
            print(f"Saved {name}: {path}")
