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

### Public web app

The deployed Streamlit app is available at:

- `https://cs372-final-homehe1p.streamlit.app/`

### One-shot terminal usage

```bash
python -m src.main --question "YOUR_QUESTION_HERE"
```

### Multi-turn terminal chat

```bash
python -m src.main --chat
```

### Multi-turn retrieval-only chat

```bash
python -m src.main --chat-retrieval-only
```

### Retrieval debugging

```bash
python -m src.main --retrieval-only --question "YOUR_QUESTION_HERE"
```

### Prompt preview

```bash
python -m src.main --prompt-only --question "YOUR_QUESTION_HERE"
```

### Local web app

```bash
streamlit run src/app.py
```

Then open the local URL printed by Streamlit.

## Grader Notes

- The project uses Gemini for answer generation, but retrieval and prompt-debug modes work without keys.
- The deployed Streamlit app uses the same retrieval and generation pipeline as the local app.

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

This evaluation compares the guarded and unguarded system on unsafe-request blocking, disclaimer inclusion, and insufficient-support fallback behavior.
