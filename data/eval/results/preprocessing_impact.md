# Preprocessing Impact

This note documents how the preprocessing pipeline affected the usefulness of the dataset for retrieval.

## Where the preprocessing pipeline is implemented

- `src/data/pipeline.py`
- `src/data/clean.py`

## Data quality challenges addressed

The preprocessing work in this project mainly addressed:

1. domain-specific cleaning of legal and housing text
2. noisy-text and outlier handling

In practice, that included removing:

- repeated page chrome such as navigation text and boilerplate
- formatting noise from copied legal materials
- low-value filler text that did not help answer tenant-rights questions
- distracting source content that would otherwise produce weak or misleading chunks

## Why this mattered

The retriever works over chunked text, so noisy or repetitive source material can easily become noisy or repetitive chunks. If that noise is left in place, the system is more likely to:

- retrieve broad but unhelpful source fragments
- surface chunks with weak legal content
- dilute the value of issue-specific sources

Cleaning the source text improves the quality of the chunked corpus before retrieval even begins.

## Qualitative evidence of impact

The impact of preprocessing is easiest to see qualitatively.

After manual cleanup and normalization:

- retrieved snippets were easier to read and more focused on legal content
- broad boilerplate and page chrome were less likely to appear in retrieved context
- issue-specific sources such as repairs, lockout, and utility shutoff materials were more usable as retrieval targets

This mattered especially in a legal-information setting, where copied webpages and statutes often include extra structure, repeated headings, or clutter that does not help the model answer the tenant’s question.

## Example of why preprocessing helped

The repairs and habitability materials are a good example of this effect. Before cleanup, copied legal or web text can include repeated headings, formatting noise, and other material that does not express the actual tenant-rights rule clearly. After preprocessing, the core legal content is more concentrated, which makes the resulting chunks easier for retrieval to match and easier for the model to use in grounded answers.

## Summary

The preprocessing pipeline improved the retrieval corpus by making the raw legal source text cleaner, more focused, and easier to chunk effectively. The strongest evidence of impact in this project is qualitative: the cleaned corpus produces more legible and more relevant retrieved context than a noisier raw-text corpus would.
