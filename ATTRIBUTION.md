# Attribution

## External Libraries and APIs

Main Python libraries used in the project include:

- `sentence-transformers`
- `scikit-learn`
- `rank-bm25`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `streamlit`
- `python-dotenv`
- `google-genai`

See `requirements.txt` for the full dependency list used by the project.

The project also uses:

- Gemini through the Google GenAI API for answer generation
- `sentence-transformers/all-MiniLM-L6-v2` for semantic retrieval embeddings

## Dataset and Source Material

The source corpus was custom curated by the project author from North Carolina housing-law and tenant-rights materials, including legal-aid pages, court guidance, and statutory materials.

Relevant files:

- `data/raw/source_index.csv`
- `data/raw/`
- `data/raw/DATASET_METHODOLOGY.md`

These sources were manually selected, reviewed, cleaned, and indexed for retrieval use.

## AI Assistance Overview

This project was developed with some assistance from GitHub Copilot and minor aid from Claude Code. AI assistance was used mainly as a coding and writing support tool.

AI assistance was used for:

- creating appropriate repo structure
- debugging support
- Streamlit app setup support
- evaluation-script implementation and revision
- retrieval-pipeline tuning support
- documentation drafting and revision
- wording help for README, setup instructions, and self-assessment materials

All final code, file organization, evaluation choices were ultimately made myself with AI being used as a debugger and guide when I was confused.

## Evaluation Data

The evaluation question set in:

- `data/eval/eval_questions.csv`

which contained a 50-question set even issue-category coverage was drafted by AI, and the final version was reviewed and edited by myself to correct labels and manually change those I did not find helpful.

Qualitative and quantitative evaluation outputs were generated from those manually labeled questions using the project’s evaluation scripts.

## Documentation and Writeup Files

AI assistance helped revise writing in these files by making formatting better and correcting grammatical errors:

- `README.md`
- `SETUP.md`
- `RUBRIC_WRITEUP.md`
- `ATTRIBUTION.md`
- `data/raw/DATASET_METHODOLOGY.md`
- `data/eval/results/preprocessing_impact.md`
- `data/eval/results/error_analysis_summary.md`
- `data/eval/results/qualitative_eval_notes.md`

These files were ultimately comprised of my ideas and analysis but edited to be made 'prettier' by AI. 

## Python Files

### `src/app.py`

I needed guidance on configuring the Streamlit web interface because I had not built a web page like this before. AI helped me with the general app structure, session-state handling, sidebar controls, and a few retrieval/debug display revisions.

### `src/config.py`

I mainly used AI here to check that the environment-variable configuration made sense and to slightly clean up the structure.

### `src/conversation/memory.py`

I used a little AI help here to think through and revise the conversation-memory helpers, including recent-turn and recent-user-message accessors.

### `src/conversation/state_tracker.py`

I needed some help thinking through the keyword-based state tracking logic. AI also helped me build parts of the issue-keyword mapping by parsing themes from the curated dataset.

### `src/data/chunk.py`

I used some AI help here for the chunking logic and later debugging, especially around preserving the metadata needed downstream.

### `src/data/clean.py`

I needed help thinking through parts of the cleaning logic and debugging, especially for domain-specific text cleanup and noisy-text handling.

### `src/data/collect.py`

I used AI for some guidance on the collection and loading logic and later debugging, including metadata parsing and issue-tag support.

### `src/data/metadata.py`

I used a small amount of AI help here to define the metadata structure and later revise it for multi-label issue tags and field cleanup.

### `src/data/pipeline.py`

I needed some help organizing the preprocessing pipeline logic that links collection, cleaning, and chunking, and I also used AI for debugging support.

### `src/evaluation/analyze_errors.py`

AI helped me guide this script, but the main use here was formatting the plots the way I wanted. I used AI to help make the graphs more readable and understandable through label cleanup, legend placement, and other presentation changes.

### `src/evaluation/retrieval_eval.py`

I used minor AI guidance here for the retrieval-metric helper logic used by the evaluation pipeline.

### `src/evaluation/run_ablation.py`

I used AI for some guidance on the ablation-study script, but especially for revising the plots so they were more readable and better formatted.

### `src/evaluation/run_guardrail_eval.py`

I used AI for some guidance on the guardrail evaluation script, and I also used it to help revise how the output plots were formatted and presented.

### `src/evaluation/run_retrieval_eval.py`

I used AI for some guidance on the controlled retrieval-comparison script, and I also used it to help revise the comparison plots so the formatting, labels, and metric presentation were more readable and understandable.

### `src/generation/answer_generator.py`

I needed some help here with Gemini API integration and cleaning up the generation wrapper.

### `src/main.py`

I needed debugging help in `main.py` because this file pulls a lot of pieces together. AI helped me check that the retrieval flow, generation flow, CLI modes, and multi-turn orchestration were all working together correctly.

### `src/prompting/fewshot.py`

I used a small amount of AI help here to draft or revise few-shot prompt examples and formatting support.

### `src/prompting/templates.py`

I needed some help building the grounded prompt template, especially around the legal-information constraints, disclaimer wording, and overall prompt structure.

### `src/retrieval/bm25.py`

I used minor AI help here to check the BM25 retrieval structure and how it fit into the shared retrieval interface.

### `src/retrieval/embeddings.py`

I used minor AI help here to check the semantic-retrieval integration using sentence embeddings.

### `src/retrieval/hybrid.py`

I needed guidance here on how to make the hybrid retriever more efficient and better tuned for the tenant-rights domain. AI helped with ideas around score combination, reranking heuristics, multi-label issue-tag support, and later retrieval-tuning revisions.

### `src/safety/guardrails.py`

I mainly used AI here to check the rule-based unsafe-request detection and low-support fallback support.

### `src/utils/io.py`

I used minor AI help here for utility-function cleanup or checking if applicable.


