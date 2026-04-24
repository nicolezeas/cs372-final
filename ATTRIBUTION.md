# Attribution

## AI Assistance

This project was developed with coding and writing assistance from OpenAI Codex/ChatGPT-style tooling. AI assistance was used for:

- code drafting and refactoring
- debugging support
- README and documentation drafting
- evaluation-script implementation support
- rubric-writeup drafting

All final code, organization choices, and project decisions were reviewed and integrated by the project author.

## External Libraries

Main Python dependencies include:

- `sentence-transformers`
- `transformers`
- `torch`
- `scikit-learn`
- `rank-bm25`
- `pandas`
- `matplotlib`
- `seaborn`
- `streamlit`
- `python-dotenv`
- `google-genai`

See `requirements.txt` for the dependency list used by the project.

## Models

The project uses:

- `sentence-transformers/all-MiniLM-L6-v2` for semantic retrieval embeddings
- Gemini (`gemini-2.5-flash` by default) for answer generation

## Dataset / Source Material

The corpus was custom curated from North Carolina housing-law and tenant-rights sources, including court, statute, and legal-aid materials stored under:

- `data/raw/`

These sources were manually collected, cleaned, and indexed for retrieval.

## Evaluation Data

The evaluation question set in:

- `data/eval/eval_questions.csv`

was manually created and labeled for this project.

## Notes

If this file needs to be more specific for your course policy, you can add:

- exact links to any external datasets or websites used
- which pieces of code were AI-assisted
- whether any generated text or plots were edited manually
