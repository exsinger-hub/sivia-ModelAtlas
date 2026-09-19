---
name: paper2overview
description: Turn an existing MCM/ICM paper or manuscript into an overview figure using SIVIA's source-to-scene workflow and verified O/F illustration references. Use for paper 2 overview, paper-to-overview, Our Work and 美赛论文总览图. Not problem solving, paper writing or standalone data plotting.
---

# Paper → Overview

One product: an actual overview image, its complete drawing prompt and source-grounded caption.
The paper controls scientific content; reference illustrations guide composition, not models/results.

## Read and establish the figure claim

Use `atlas_prepare_paper(path, problem, query)` or `modelatlas paper2overview` for PDF/MD/TXT/TeX.
Read the full manuscript returned, not only its abstract. Inspect original equations/figures where
text extraction is inadequate; intake is not OCR or scientific interpretation. For pasted text,
save a local paper snapshot. A contest problem alone is not a paper: request model notes/manuscript
rather than inventing a solution. A project-development request without a paper needs no fictional demo.

Record one figure claim, intended placement, print width and language. Map the paper's core question,
shared models, inputs/outputs, dependencies, validation and decisions to section/page evidence.
Distinguish stated results, planned work and unresolved relationships. Do not force a fixed model count.
Preserve the actual year/problem; A–F is a retrieval profile, and problem F is not award F (Finalist).

## Retrieve and view illustration references

`atlas_search_styles` defaults to overview + award core. Search by model relationship as well as
problem class. `atlas_fetch_reference(case_id)` checks the pinned PDF and renders its exact page:
open that image and read caption/context before borrowing its design. A download is not visual review.
Choose a few relevant cases; broader mechanism/algorithm/data illustrations remain supporting references,
not additional drawing products. Use collection research explicitly for research extensions.

For new source discovery use AnySearch: discover academic subdomains/required parameters, supplement
with exact team IDs, official results and author-repository web queries. `atlas_find_papers` returns
discovery only. Do not send private manuscript text in queries or infer awards from snippets.
Record case/page/figure, borrowed visual principles and excluded source-specific models/results/defects.
If references are unavailable, state the limitation and proceed from the paper when feasible.

## Design and draw

Read [production contract](references/production-contract.md) before writing the complete prompt.
Choose a paper-specific scene structure: shared-inference branches, model-to-task mapping, actor
relations, feedback, spatial organization or process cycles. Neither dense box inventories nor sparse
pipelines are universal overview templates. Specify region hierarchy, exact labels, connections and
their meanings, semantic colors, meaningful objects and reading order. Preserve interpretation-changing
boundaries and conditions; omit detail only with a stated source-grounded reason.

Use SIVIA's **ImageGen-first** route with the host's available image tool and applicable image skill.
Preserve the full prompt and actual image. Do not pass off source-page screenshots as new output.
This runtime does not include an image model. If generation is unavailable, report prompt/design-only
status rather than claiming the overview is complete.

Any quantitative evidence included must be supplied, not invented by image generation. Conceptual
mini-panels must be explicitly schematic. Do not expand into data analysis, standalone plots, editable
PowerPoint reconstruction or writing the paper. User requests for those are separate scope decisions.

## Review, pair and deliver

View the actual image full-size and at intended print size. Check labels, model boundaries, all
connection directions, equations and scientific assertions against the paper. Inspect hierarchy,
contrast, collisions, connector routing and reduction readability; correct and inspect again.
Successful generation is not visual approval.

Use `atlas_pair_overview` for actual local image + full prompt.md + evidence/review brief.json;
use `atlas_audit_overview` for file integrity. Record assistant review and user approval separately.
If the tool returns no local artifact, show the native image and report local pairing pending.

Deliver the actual figure inline when possible, prompt/bundle links and a concise caption/placement
suggestion. Do not insert into or rewrite the source paper without authorization. Keep revisions
separate; do not force a planning approval round before an authorized drawing task. Only actually
rendered and accepted image–prompt pairs become production examples. Keep source PDFs, source-page
images and private manuscripts out of automatic Git publication.
