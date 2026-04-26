# Rubric Writeup

This document maps the HomeHelp NC project to the rubric items discussed during development. Every item below points to concrete evidence in the codebase or saved evaluation artifacts.

## Clearly completed items

### Completed project individually without a partner

- This repository contains a single-user local workflow and no partner scaffolding.
- Development history and local project structure are consistent with solo implementation.

### Developed a retrieval-augmented generation system with a custom retrieval pipeline

Evidence:

- `src/main.py`
- `src/retrieval/bm25.py`
- `src/retrieval/embeddings.py`
- `src/retrieval/hybrid.py`

Why this counts:

- The project uses a custom chunking and retrieval stack rather than a hosted black-box retriever.
- The retrieval pipeline includes hybrid search, heuristic reranking, source-priority boosting, and document diversity controls.
- This satisfies the “at least two of: custom chunking strategy, embedding model selection with comparison, reranking, hybrid search” expectation through custom chunking, reranking, and hybrid search.

### Collected or constructed original dataset through substantial engineering effort

Evidence:

- `data/raw/*.txt`
- `data/raw/source_index.csv`
- `src/data/collect.py`
- `src/data/clean.py`
- `src/data/pipeline.py`

Why this counts:

- The dataset was manually assembled from North Carolina housing sources and then cleaned into a usable corpus.
- Significant engineering effort went into source indexing, normalization, OCR cleanup, form-noise removal, and pipeline execution.

### Built multi-turn conversation system with context management and history tracking

Evidence:

- `src/main.py`
- `src/conversation/memory.py`
- `src/conversation/state_tracker.py`

Why this counts:

- `LexAINCSession` keeps conversation history, tracked case state, and a persistent retriever across turns.
- `ConversationMemory` stores prior user and assistant turns, and `UserCaseState` stores structured facts such as county, issue category, urgency, and follow-up facts like possible lockout or repair issues.
- `--chat` exposes a working multi-turn CLI workflow that generates full answers on every turn rather than only retrieval output.
- follow-up retrieval is contextual: the system builds a retrieval query from recent user messages plus tracked state and facts, so a vague follow-up like `What should I do next?` can still retrieve sources using earlier turns.

### Implemented preprocessing pipeline addressing at least two substantive data quality challenges

Evidence:

- `src/data/clean.py`
- `src/data/pipeline.py`
- cleaned raw files in `data/raw/`

Substantive challenges addressed:

- OCR and page-number artifacts
- legal-form/template noise
- duplicate and broken source text
- outdated or non-substantive third-party material

### System guardrails against inappropriate use employing at least two techniques with evidence of impact

Evidence:

- `src/safety/guardrails.py`
- `src/main.py`
- `src/evaluation/run_guardrail_eval.py`
- `data/eval/results/guardrail_eval_summary.csv`

Two techniques:

- unsafe-request pattern detection
- prompt-level legal-information and disclaimer constraints

Impact evidence:

- `guardrail_eval_summary.csv` shows a with-vs-without comparison across three guardrail behaviors:
  - unsafe-request blocking
  - disclaimer inclusion
  - insufficient-support fallback
- the current controlled test set shows `1.0` accuracy for all three behaviors with guardrails enabled and `0.0` without guardrails.

### Performed error analysis with visualization and discussion of failure cases

Evidence:

- `data/eval/results/error_analysis_summary.md`
- `data/eval/results/error_analysis_by_mode.csv`
- `data/eval/results/error_analysis_by_issue.csv`
- `data/eval/results/error_analysis_by_mode.png`
- `data/eval/results/error_analysis_by_issue.png`
- `src/evaluation/analyze_errors.py`

Why this counts:

- The project includes written failure analysis, grouped counts, and saved plots showing how failure types vary by retrieval mode and issue category.

### Compared multiple model architectures or approaches quantitatively with controlled setup

Evidence:

- `src/evaluation/run_retrieval_eval.py`
- `data/eval/results/compare_bm25_embedding_hybrid_summary.csv`
- `data/eval/results/compare_bm25_embedding_hybrid_detail.csv`

Approaches compared under the same eval set:

- BM25
- sentence-embedding retrieval
- hybrid retrieval

Saved summary:

- `embedding`: precision@5 `0.399`, recall@5 `0.753`, hit@5 `0.920`
- `hybrid`: precision@5 `0.403`, recall@5 `0.847`, hit@5 `0.920`
- `bm25`: precision@5 `0.291`, recall@5 `0.420`, hit@5 `0.520`

### Conducted ablation study varying at least two design choices

Evidence:

- `src/evaluation/run_ablation.py`
- `data/eval/results/ablation_method_retrieval_summary.csv`

Design choices varied:

- embeddings enabled vs disabled
- reranking heuristics enabled vs disabled

Why this counts:

- The methodological ablation isolates two independent retrieval-design choices: whether semantic embeddings are used and whether domain-specific reranking heuristics are used.
- Results are saved in a summary table and figure for controlled comparison across the four retrieval variants.

### Used sentence embeddings for semantic similarity or retrieval

Evidence:

- `src/retrieval/embeddings.py`
- `src/retrieval/hybrid.py`

Why this counts:

- The project uses `sentence-transformers/all-MiniLM-L6-v2` to compute chunk embeddings and retrieve semantically similar sources.

### Made API calls to a state-of-the-art model with meaningful integration

Evidence:

- `src/generation/answer_generator.py`
- `src/main.py`
- `src/app.py`

Why this counts:

- The Gemini API is integrated into the live answer-generation path through the official Google GenAI SDK.
- The integration is meaningful and wired into both the CLI and Streamlit app flows.

### Applied in-context learning with few-shot examples or chain-of-thought prompting

Evidence:

- `src/prompting/fewshot.py`
- `src/prompting/templates.py`

Why this counts:

- Few-shot examples are not just stored; they are injected into the live prompt used for generation.

### Conducted both qualitative and quantitative evaluation with thoughtful discussion

Evidence:

- Quantitative:
  - `data/eval/results/compare_bm25_embedding_hybrid_summary.csv`
- `data/eval/results/ablation_method_retrieval_summary.csv`
  - `data/eval/results/guardrail_eval_summary.csv`
- Qualitative:
  - `data/eval/results/qualitative_eval_notes.md`
  - `data/eval/results/error_analysis_summary.md`

### Documented at least two iterations of model improvement driven by evaluation results

Evidence:

- `README.md`
- `data/eval/results/error_analysis_summary.md`

Iterations documented:

- Iteration 1: dataset cleanup
- Iteration 2: reranking, deduplication, and source-priority heuristics

### Modular code design with reusable functions and classes

Evidence:

- `src/data/`
- `src/retrieval/`
- `src/evaluation/`
- `src/conversation/`
- `src/prompting/`
- `src/safety/`
- `src/generation/`

Why this counts:

- The system is split into reusable modules for collection, cleaning, chunking, retrieval, prompting, generation, evaluation, and conversation state.

## Practical note

The strongest remaining caveat is not rubric coverage but runtime setup: end-to-end answer generation depends on a valid Gemini API key and local installation of the Gemini SDK. The retrieval, evaluation, conversation, guardrail, and prompt-construction pieces are all runnable locally without generation enabled.
