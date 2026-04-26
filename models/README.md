# Models

This project does not include locally trained model weights.

Instead, it uses:

- Gemini for answer generation via API
- `sentence-transformers/all-MiniLM-L6-v2` for sentence embeddings used in retrieval

Relevant code:

- model configuration: `src/config.py`
- generation model loading and invocation: `src/generation/answer_generator.py`
- embedding model loading: `src/retrieval/embeddings.py`
