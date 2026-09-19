# Paper → Overview architecture

A single pipeline: full paper → source-linked figure claim → illustration references → scene design
and full prompt → host ImageGen → visual review/correction → actual image/prompt/evidence bundle.

## Runtime

- papers.py snapshots/extracts PDF/MD/TXT/TeX, returns overview candidates and awaiting_agent_design.
  Image generation remains a host capability, not a hidden Python service.
- corpus.py loads the preserved reviewed illustration library, applies transparent filtered term
  matching, verifies source bytes/page counts and renders exact reference pages with Poppler.
- search.py uses AnySearch academic/web discovery and returns normalized metadata. Search results
  do not acquire award or curated status automatically.
- CLI and seven MCP tools call the same functions. One paper2overview skill coordinates the workflow.

The runtime has no standalone plot renderer, numerical modeling stack, generic HTML gallery or
SQLite card service. NumPy and Matplotlib are not dependencies.

## Data boundaries

corpus.json remains the complete 9-paper/20-case reference library. Original year/problem provenance,
official award evidence, transfer targets, visual review notes and research status remain unchanged.
Supporting mechanism, algorithm and data-plot references can guide part of an overview without
expanding product scope.

.modelatlas/references holds private local PDF/page caches. New paper sessions go into
.modelatlas/papers; each overview pair has a new child directory with actual image, prompt, evidence,
caption, review and hashes. Existing .modelatlas/drafts sessions can still be paired by supplying
their directory because the session contract is unchanged. Old databases and outputs are not deleted,
migrated, opened or reseeded automatically.

Only the host can interpret the full paper, perform generation and inspect scientific/visual
fidelity. Hash checks cannot prove scientific correctness, image-tool provenance or user acceptance.
No automatic manuscript insertion, original-paper redistribution or Git upload of private material.

## 0.3.0 migration

Use paper2overview instead of draft2overview, atlas_prepare_paper instead of atlas_prepare_draft,
and modelatlas.papers instead of modelatlas.drafts. Removed legacy commands/tools intentionally fail
rather than silently route into another product. Feature removal is recoverable from Git history.
