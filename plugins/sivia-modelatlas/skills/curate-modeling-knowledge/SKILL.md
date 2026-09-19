---
name: curate-modeling-knowledge
description: Build the A–F classified MCM/ICM O/F figure-style knowledge base with verified awards and visually inspected pages; extend separately with research papers using AnySearch.
---

# Curate Modeling Knowledge

Core: figures in **Outstanding/Finalist papers**, not contest solutions or generic chart recipes.
Organize by original year/problem plus transferable categories, figure role, model relationship and
method. A–F profiles are retrieval aids, not fixed descriptions of every year's problem.

Use AnySearch for discovery. Discover academic subdomains/required parameters first; use batch/hybrid
queries for research papers, official results and author sources. Exact team-number web searches
supplement weak academic-index coverage. `atlas_find_papers` supports academic and web modes.
Search records are discovered, not reviewed/award-verified. Never send private manuscript text.

For award-core sources:

1. Read the actual paper's title, team ID, problem and year.
2. Match team/year/problem to official COMAP results. O = Outstanding Winner; F = Finalist. Problem F
   is not an award. A repository README alone is not verification.
3. Record official evidence URL and row/PDF page plus the actual paper URL. Prefer author versions,
   label mirrors, pin commits/publication versions and SHA-256.
4. Read figure, caption and context; render and **view** the actual page. Record physical PDF page,
   figure label and version, separately from printed labels.
5. Write original visual analysis: composition, useful transfer, non-transferable content, defects
   and print-size cautions. Winning an award does not make every design choice good.

Research extensions use collection research, publication status, DOI/version where available, and
award null. Their problem_targets are editorial transfer choices, not contest participation claims.

Reviewed cases live in `src/modelatlas/knowledge/corpus.json`. Validate the corpus, run tests and
coverage, and fetch a new reference page. Never add unviewed cases. General sources and legacy numeric
recipes stay in sources.json/cards.json and SQLite; `atlas_add_card` writes that legacy library, not
the verified style corpus.

A certificate named after a team is not the paper. Author revisions with changed figures or anonymized
headers are not interchangeable with submitted PDFs. Changed hashes require human/agent inspection,
not silent repinning.

Keep PDFs/pages in ignored caches. Public availability is not permission to redistribute. Repository
content is metadata and original analysis. Actual production examples separately pair image, full
prompt, draft evidence and review. Do not auto-publish private drafts, data or source images.
