# Qualitative Evaluation Notes

This file captures qualitative observations from the saved retrieval outputs in:

- `compare_bm25_embedding_hybrid_detail.csv`
- `compare_bm25_embedding_hybrid_summary.csv`

## Example 1: Illegal lockout mixed with repair issues

Question:

- `My landlord changed the locks after I complained about mold in Durham. What can I do?`

Observations:

- `bm25` retrieved broad court and Legal Aid pages and missed the dedicated repairs source.
- `embedding` retrieved the lockout source and achieved a hit, but still included broad statute pages multiple times.
- `hybrid` improved balance somewhat, but still did not capture all expected sources.

Takeaway:

- Mixed-issue questions remain difficult because procedural eviction language competes with topical repair and lockout sources.

## Example 2: Security deposit deduction

Question:

- `Can my landlord keep my security deposit for repainting in North Carolina?`

Observations:

- `embedding` consistently surfaced the dedicated deposit source and reached full recall on this example.
- `bm25` and `hybrid` were more likely to include broad landlord-tenant pages alongside the focused deposit source.

Takeaway:

- Deposit questions now work reasonably well, especially when the source wording closely matches the user’s phrasing.

## Example 3: Utility shutoff

Question:

- `My landlord shut off utilities after I was late on rent. What should I do?`

Observations:

- All approaches usually retrieved the utility shutoff statute or a closely related source.
- `embedding` performed especially well on this category because the statute text and the user’s phrasing are semantically close.

Takeaway:

- Utility-shutoff questions are one of the strongest categories in the current system.

## Overall qualitative conclusion

- `bm25` is a reasonable lexical baseline but misses some semantically phrased questions.
- `embedding` is strongest on this small evaluation set, especially for direct fact questions.
- `hybrid` offers a more interpretable retrieval path and stronger control knobs, even though its current heuristics do not yet beat pure embeddings on every metric.
- The main remaining weakness is mixed-issue retrieval, especially where broad court guidance competes with more specific topical sources.
