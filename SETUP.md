# Setup

## Environment Setup

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then add a Gemini API key to `.env`:

```bash
GENERATION_PROVIDER=gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GENERATION_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
TOP_K=5
```

## Data Preparation

Run the preprocessing pipeline before testing the system:

```bash
python -m src.data.pipeline
```

This reads the curated sources in `data/raw`, cleans them, and prepares them for chunking and retrieval.

## Running the Project

### One-shot terminal usage

```bash
python -m src.main --question "Can my landlord lock me out without a court order in North Carolina?"
```

### Multi-turn terminal chat

```bash
python -m src.main --chat
```

### Retrieval debugging

```bash
python -m src.main --retrieval-only --question "How many days do I have to appeal an eviction in NC?"
```

### Prompt preview

```bash
python -m src.main --prompt-only --question "When does a landlord have to return a security deposit in North Carolina?"
```

### Local web app

```bash
streamlit run src/app.py
```

Then open the local URL printed by Streamlit, usually `http://localhost:8501`.

## Grader Notes

- The project uses Gemini for answer generation.
- If Gemini is temporarily unavailable or a key is not configured, the retrieval and prompt-debug modes still work.
- The most reliable fallback commands for testing core functionality are:

```bash
python -m src.main --retrieval-only --question "Can a landlord shut off utilities if I do not pay?"
python -m src.main --prompt-only --question "Can my landlord lock me out without a court order in North Carolina?"
```

## Evaluation Scripts

Run the main retrieval comparison:

```bash
MPLCONFIGDIR=/tmp .venv/bin/python -m src.evaluation.run_retrieval_eval --compare
```

Run methodological ablation:

```bash
MPLCONFIGDIR=/tmp .venv/bin/python -m src.evaluation.run_ablation --study method
```

Run guardrail evaluation:

```bash
MPLCONFIGDIR=/tmp .venv/bin/python -m src.evaluation.run_guardrail_eval
```
