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

- `embedding`: precision@5 = 0.431, recall@5 = 0.750, hit@5 = 1.000
- `hybrid`: precision@5 = 0.333, recall@5 = 0.583, hit@5 = 0.667
- `bm25`: precision@5 = 0.278, recall@5 = 0.444, hit@5 = 0.500

The project also includes:

- hyperparameter ablations for chunk size and top-k retrieval
- methodological ablations over embeddings on/off and heuristics on/off
- guardrail evaluation on safe vs unsafe examples
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
