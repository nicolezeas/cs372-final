# HomeHelp NC

HomeHelp NC is a retrieval-augmented legal information assistant for low-income North Carolina tenants. It retrieves grounded housing-law sources, builds a constrained prompt from those sources, and generates structured answers through Gemini for issues such as eviction, lockouts, repairs, utility shutoffs, and security deposits.

## What it Does

HomeHelp NC answers North Carolina tenant-rights questions using a custom RAG pipeline built on a curated housing-law corpus. The system supports BM25, embedding-based, and hybrid retrieval, uses prompt-level grounding constraints, includes guardrails for unsafe or weakly supported requests, and supports both one-shot and multi-turn interactions with tracked user state. It also includes evaluation scripts for retrieval comparison, methodological ablations, guardrail testing, and error analysis.

## Quick Start

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Add your Gemini key to `.env`:

```bash
GENERATION_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GENERATION_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=5
```

Run the preprocessing pipeline:

```bash
python -m src.data.pipeline
```

Run a one-shot terminal query:

```bash
python -m src.main --question "Can my landlord lock me out without a court order in North Carolina?"
```

Run the multi-turn chat mode:

```bash
python -m src.main --chat
```

Run the local web app:

```bash
streamlit run src/app.py
```

For detailed setup, testing, and grader instructions, see `SETUP.md`.

## Video Links

- Demo video: `ADD_LINK_HERE`
- Technical walkthrough video: `ADD_LINK_HERE`

## Evaluation

The main controlled retrieval comparison is saved in:

- `data/eval/results/compare_bm25_embedding_hybrid_summary.csv`
- `data/eval/results/compare_bm25_embedding_hybrid_summary.png`

Current summary:

- `embedding`: precision@5 = 0.399, recall@5 = 0.753, hit@5 = 0.920
- `hybrid`: precision@5 = 0.403, recall@5 = 0.847, hit@5 = 0.920
- `bm25`: precision@5 = 0.291, recall@5 = 0.420, hit@5 = 0.520

Additional top-result comparison:

- `embedding`: precision@3 = 0.437, recall@3 = 0.650, hit@3 = 0.860
- `hybrid`: precision@3 = 0.477, recall@3 = 0.710, hit@3 = 0.900
- `bm25`: precision@3 = 0.333, recall@3 = 0.400, hit@3 = 0.520

The project also includes:

- methodological ablations over embeddings on/off and heuristics on/off
- guardrail comparison of unsafe-request blocking, disclaimer inclusion, and insufficient-support fallback with vs without guardrails
- written and visual error analysis

Important evaluation artifacts:

- `data/eval/results/ablation_method_retrieval_summary.csv`
- `data/eval/results/ablation_method_retrieval_plot.png`
- `data/eval/results/guardrail_eval_summary.csv`
- `data/eval/results/error_analysis_summary.md`
- `data/eval/results/error_analysis_by_mode.png`
- `data/eval/results/error_analysis_by_issue.png`

For a more detailed rubric-oriented summary, see `RUBRIC_WRITEUP.md`.

## Individual Contributions

This project was completed individually.
