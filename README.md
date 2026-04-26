# HomeHelp NC

HomeHelp NC is a retrieval-augmented legal information assistant for low-income North Carolina tenants. It retrieves grounded housing-law sources, builds a constrained prompt from those sources, and generates structured answers through Gemini for issues such as eviction, lockouts, repairs, utility shutoffs, and security deposits.

## What it Does

HomeHelp NC answers North Carolina tenant-rights questions using a custom RAG pipeline built on a curated housing-law corpus. The system supports BM25, embedding-based, and hybrid retrieval, uses prompt-level grounding constraints, includes guardrails for unsafe or weakly supported requests, and supports both one-shot and multi-turn interactions with tracked user state. It also includes evaluation scripts for retrieval comparison, methodological ablations, guardrail testing, and error analysis.

## Quick Start

From the project root, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a local `.env` file:

```bash
cp .env.example .env
```

Then add your Gemini key:

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

Use the deployed web app:

- `https://cs372-final-homehe1p.streamlit.app/`

Or run the app locally with Streamlit:

```bash
streamlit run src/app.py
```

Optional local commands:

Run a one-shot terminal query:

```bash
python -m src.main --question "YOUR_QUESTION_HERE"
```

Run retrieval/debug mode:

```bash
python -m src.main --retrieval-only --question "YOUR_QUESTION_HERE"
```

Run prompt preview mode:

```bash
python -m src.main --prompt-only --question "YOUR_QUESTION_HERE"
```

Run the multi-turn chat mode:

```bash
python -m src.main --chat
```

Run the multi-turn retrieval-only chat mode:

```bash
python -m src.main --chat-retrieval-only
```

## Video Links

- Demo video: `ADD_LINK_HERE`
- Technical walkthrough video: `ADD_LINK_HERE`

## Evaluation

This section summarizes the main retrieval, ablation, guardrail, and qualitative evaluation results for the current system.

**Current `@5` comparison:**

- `embedding`: precision@5 = 0.399, recall@5 = 0.753, hit@5 = 0.920
- `hybrid`: precision@5 = 0.403, recall@5 = 0.847, hit@5 = 0.920
- `bm25`: precision@5 = 0.291, recall@5 = 0.420, hit@5 = 0.520

These `@5` results focus more on broader source coverage. At this cutoff, hybrid gives the strongest recall while tying the best hit rate, which means it is the most reliable option when the answer needs enough relevant support to stay grounded rather than just one strong document.

**Current `@3` comparison:**

- `embedding`: precision@3 = 0.437, recall@3 = 0.650, hit@3 = 0.860
- `hybrid`: precision@3 = 0.477, recall@3 = 0.710, hit@3 = 0.900
- `bm25`: precision@3 = 0.333, recall@3 = 0.400, hit@3 = 0.520

These `@3` results focus more on top-result quality. Since the model is most influenced by the first few retrieved passages, this view is helpful for judging whether the system is surfacing the most useful evidence early. Hybrid still performs best here, which strengthens the case for using it as the default retriever.

In practical terms, these results show that the hybrid retriever performs best overall on the current benchmark. At `@3`, it returns the cleanest top results, which matters because those are the sources most likely to shape the final answer. At `@5`, it also provides the strongest coverage of relevant documents, which is useful for grounded legal-information responses that may need more than one supporting source. BM25 remains a useful baseline, but it misses more relevant material and performs worse on both precision and recall.

**Methodological ablation over embeddings on/off and heuristics on/off:**

- `BM25 + Embeddings`: precision@5 = 0.381, recall@5 = 0.823, hit@5 = 0.940
- `BM25 + Embeddings + Heuristics`: precision@5 = 0.403, recall@5 = 0.847, hit@5 = 0.920
- `BM25 Only`: precision@5 = 0.314, recall@5 = 0.567, hit@5 = 0.720
- `BM25 + Heuristics`: precision@5 = 0.327, recall@5 = 0.573, hit@5 = 0.720

Looking across these variants makes it easier to separate what each design choice contributes. Embeddings produce the biggest gain, especially in recall, while heuristics help most when they are added to an already strong semantic retriever instead of used on their own.

This ablation suggests that embeddings provide the largest performance gain, while heuristics help most when they are layered on top of embeddings rather than used by themselves. In other words, the final hybrid design works best because it combines semantic retrieval with narrower issue-aware reranking instead of relying on keyword overlap alone.

**Quantitative guardrail results:**

- `Disclaimer Included`: with guardrails = 1.0, without guardrails = 0.0
- `Insufficient Support Fallback`: with guardrails = 1.0, without guardrails = 0.0
- `Unsafe Request Blocked`: with guardrails = 1.0, without guardrails = 0.0

This comparison is useful because it isolates the effect of the guardrail layer instead of only testing the final app as a whole. The difference between the guarded and unguarded versions is clear across all three behaviors.

Practically, this means the guardrail layer is doing visible work rather than just being described in the prompt. With guardrails enabled, the system includes the legal-information disclaimer, refuses clearly unsafe requests, and falls back when support is too weak. Without those mechanisms, it does none of those things on the evaluation set.

**Qualitative evaluation outcomes:**

- utility shutoff and most security deposit questions are among the strongest categories
- the hardest cases are mixed-issue questions, especially lockout plus habitability
- the most common failure mode is partial retrieval, where the system finds one useful source but misses another source needed for a fuller answer
- hybrid retrieval improved overall coverage and now performs best overall on the current benchmark, while BM25 remains the weakest baseline

These qualitative findings matter because they show where the system is dependable and where it still needs improvement. The current pipeline works best on narrower, well-scoped tenant questions, but mixed questions still create ranking problems because broad legal pages can compete with more targeted sources.


## Individual Contributions

This project was completed individually.
