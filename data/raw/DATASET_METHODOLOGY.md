# Data Set Methodology

This project uses a custom-curated dataset focused on North Carolina tenant-rights and housing-law questions. The dataset was built manually rather than downloaded as a ready-made benchmark because the goal of the project was to answer a narrow set of North Carolina housing questions using trustworthy local sources.

## List of Sources

The raw source files and corpus metadata are stored in:

- `data/raw/`
- `data/raw/source_index.csv`

The corpus includes North Carolina court guidance, legal-aid resources, statutes, and a small number of carefully selected explanatory sources that were judged useful for tenant-rights retrieval.

## Custom Curation

The dataset was built through custom curation. I manually searched for North Carolina housing-law and tenant-rights sources, reviewed each source for relevance, and only kept sources that were useful for likely user questions such as eviction, lockouts, repairs, utility shutoffs, lease termination, and security deposits.

For each candidate source, I checked whether it:

- was actually relevant to North Carolina law or process
- contained useful legal or procedural information for tenants
- was not mostly repeated information already covered better by another source
- did not contain excessive ads, page chrome, navigation clutter, or low-value filler
- was specific enough to help retrieval instead of only adding broad noise

This means the dataset was not just collected; it was filtered and shaped for the specific RAG task.

## Manual Annotation and Labeling

The project also includes manual annotation and labeling.

For the source corpus, I manually labeled each source in `source_index.csv` with metadata such as:

- document ID
- title
- URL
- source type
- jurisdiction
- county when relevant
- issue category

For evaluation, I manually created and labeled the questions in `data/eval/eval_questions.csv`, including:

- issue category
- expected relevant document IDs
- key answer points

This manual labeling made it possible to evaluate retrieval quality in a controlled way instead of relying only on informal testing.

## Manual Cleaning and Editing

After collecting the raw sources, I manually cleaned and edited them so they would be easier for the model and retriever to use.

This manual editing included:

- removing ads, menus, navigation text, and repeated page elements
- removing irrelevant links and other non-content text
- trimming repeated or low-value information
- cleaning formatting issues from copied legal materials
- preserving the legal explanations, procedures, timelines, and rights information that were most useful for retrieval

This step mattered because many legal and housing webpages contain boilerplate, repeated headers, or distracting content that would make retrieval worse if left in the corpus unchanged.

## Processing Pipeline

After manual curation and editing, the documents were processed through the project pipeline:

1. raw source text was stored in `data/raw/`
2. metadata was recorded in `data/raw/source_index.csv`
3. sources were loaded through `src/data/collect.py`
4. source text was normalized and cleaned through `src/data/clean.py`
5. documents were chunked through `src/data/chunk.py`
6. processed chunks were written by `src/data/pipeline.py`

The final processed retrieval corpus is saved in `data/processed/chunks.json`.

## Why This Counts as Dataset Construction

This dataset was constructed through:

- custom curation of domain-specific North Carolina sources
- manual annotation and labeling of both sources and evaluation questions
- manual cleaning and editing of raw source text
- a repeatable preprocessing pipeline that converts the curated corpus into retrieval-ready chunks

Together, these steps document how the dataset was built and why it is appropriate for the project.
