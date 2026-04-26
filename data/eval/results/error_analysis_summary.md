# Error Analysis of Failure Cases Discussion

This analysis is based on error_analysis_by_mode.png and error_analysis_by_issue.png. The goal of this section is to describe the failure cases and explain why retrieval fails when it does and what kinds of questions are the hardest inputs for the model.

## Overall pattern

Straightforward questions about utility shutoffs and most security deposit questions are usually retrieved well. The harder cases are the ones that combine multiple legal issues or that contain broad tenant-law language that can match a general source just as easily as a focused one.

Across retrieval modes, BM25 had the most complete misses. Embedding and hybrid retrieval both improved coverage, but the remaining errors were usually partial retrieval errors rather than total misses. That means the system often finds at least one useful source, but still misses another source that would make the answer more complete.

## Why the model fails

The main reason the model fails is not that it retrieves nothing. The more common problem is that it retrieves a broad North Carolina landlord-tenant page when the better answer would come from a narrower source focused on one issue, such as lockouts, repairs, or eviction defense.

There are a few recurring causes behind that:

- broad legal vocabulary overlaps with broad court pages
- mixed-issue questions activate more than one category at once
- official statewide pages sometimes outrank narrower self-help sources even when the narrower source is more directly useful
- some questions include both procedural language and factual housing problems, which makes ranking harder

In other words, the system struggles most when a question is legally specific but phrased in a way that still resembles a general tenant-law question.

## What inputs are most challenging

The most challenging inputs are:

- mixed-issue questions, especially lockout plus habitability questions
- habitability questions phrased in broad terms like “what are my options?”
- eviction questions that should retrieve both official court procedure and practical self-help guidance

These are harder because the retriever has to balance more than one kind of relevance at once. A single broad source may look strong according to keyword overlap, even if it is not the most helpful source for the actual tenant problem.


## Which categories look strongest and weakest

Based on the current results:

- strongest categories: `utility_shutoff`, most `security_deposit` questions
- weakest categories: `lockout`, `habitability`, and especially mixed-issue questions

This lines up with the qualitative examples above. Questions with one narrow issue are easier. Questions that combine two issues or mix factual and procedural language are harder.

## What this analysis suggests

The main lesson from the error analysis is that retrieval quality now depends less on finding any source at all and more on ranking the right combination of sources high enough.

The most useful future improvements would be:

- stronger preference for issue-specific sources when the question contains clear issue terms
- better handling of mixed-issue questions
- continued tuning of broad-source penalties so general pages do not crowd out narrower ones

That is why the later retrieval changes in the project focused on hybrid ranking, issue-aware heuristics, and multi-label metadata rather than only adding more documents.
