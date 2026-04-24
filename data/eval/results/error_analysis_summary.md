# Error Analysis Summary

This summary is based on the controlled retrieval comparison saved in:

- `compare_bm25_vs_reranked_detail.csv`
- `compare_bm25_vs_reranked_failures.csv`

## Failure counts

- `missed_relevant_source`: 6
- `partial_retrieval`: 2
- `none`: 4

## Main failure patterns

### 1. Lockout + habitability questions are under-retrieved

Example:

- `q_001`: "My landlord changed the locks after I complained about mold in Durham. What can I do?"

Expected source IDs:

- `nc_002`
- `nc_005`
- `nc_007`

Observed behavior:

- retrieval favored broad court help pages such as `NC Courts Landlord Tenant Issues`
- retrieval did **not** reliably surface the more direct lockout or habitability sources

Interpretation:

- the query mixes two issues, `lockout` and `habitability`
- general eviction vocabulary in court pages is dominating more specific lockout and repair sources

### 2. Habitability questions over-match broad eviction pages

Example:

- `q_004`: "My apartment has mold and my landlord keeps ignoring repair requests. What are my options in North Carolina?"

Expected source IDs:

- `nc_002`
- `nc_005`

Observed behavior:

- retrieved titles were mostly `NC Courts Landlord Tenant Issues` and `NC Courts Small Claims Landlord Tenant`
- the dedicated repairs/habitability source did not rank high enough

Interpretation:

- words like `options`, `North Carolina`, and general tenant-law language are pulling in broad background sources
- the repair/habitability signal still needs stronger weighting

### 3. Deposit deduction questions are still attracted to broad landlord-tenant pages

Example:

- `q_005`: "I moved out and my landlord kept my deposit for cleaning and repainting. Is that allowed?"

Expected source IDs:

- `nc_004`

Observed behavior:

- retrieval still preferred broad `NC Courts Landlord Tenant Issues` chunks instead of the dedicated security deposit source

Interpretation:

- the word `moved out` seems to pull in broader landlord-tenant and eviction context
- deposit-specific keywords need stronger matching when present

### 4. Eviction hearing questions partially retrieve the right materials

Example:

- `q_003`: "I got papers for eviction in Wake County and my hearing is soon. What should I do first?"

Expected source IDs:

- `nc_001`
- `nc_003`
- `nc_006`

Observed behavior:

- the system retrieved the two official court sources
- it did not reliably retrieve the Legal Aid eviction manual

Interpretation:

- the question is strongly procedural, so the official court sources dominate
- that behavior is partly desirable, but it means the system can miss a practical self-help guide that also belongs in the answer context

## What changed across iterations

### Iteration 1: Data cleaning

We manually cleaned several raw sources to remove:

- OCR/page-number artifacts
- form-template noise
- outdated material
- marketing-heavy third-party text

Impact:

- retrieval stopped surfacing obviously broken chunks from repairs and other sources
- retrieved snippets became more legible and on-topic

### Iteration 2: Retrieval heuristics and deduplication

We added:

- issue-category hints
- title-keyword boosts
- direct-answer phrase boosts such as `10 days`, `30 days`, and `7 days`
- source-priority bonuses for official NC sources
- document-level diversity limits

Impact:

- utility shutoff and security deposit questions became much cleaner
- duplicate chunks from the same source were reduced
- some broad small-claims pages were pushed lower

## Takeaways

- The strongest categories are now `utility_shutoff`, `security_deposit`, and straightforward `appeal` questions.
- The weakest categories are mixed-issue questions such as `lockout + mold` and questions where broad landlord-tenant pages outcompete more specific sources.
- The next best retrieval improvement is stronger source preference for dedicated topical documents when a query contains clear issue-specific terms such as `mold`, `repairs`, `deposit`, or `lockout`.
