# Architecture

Primary path: manuscript → evidence/figure claim → O/F visual retrieval → actual page inspection →
host-agent design/full production prompt → host ImageGen → review/correction → paired artifact.

The Python runtime provides reliable source retrieval and artifact handling, not an LLM or image model.
Intake explicitly returns awaiting_agent_design and image_generated=false. It snapshots the draft,
extracts PDF/MD/TXT/TeX text and retrieves award-core overview candidates; the host interprets the draft.

## Data boundaries

- Versioned corpus.json: reviewed figures, pinned papers, official award evidence, A–F navigation and
  original style-transfer notes. Research extensions are separate and cannot assert awards.
- SQLite: ordinary discovery/import records, legacy general cards and quantitative render runs.
- Ignored references cache: hash-verified third-party PDFs and rendered page images. Not redistribution.
- Ignored draft sessions: original snapshot and full extracted text, candidate references and independently
  versioned overview pairs. Never auto-uploaded or committed.

Term matching follows hard problem/role/collection filters. Transfer targets do not change original
problem provenance. Coverage distinguishes original-category counts from reusable cross-category counts.
Reference download is bounded and checksum-pinned; changed bytes require review. Poppler renders only
the requested physical page. A rendered reference page is not a new overview or a current visual review.

## Runtime and host responsibilities

CLI and 14 MCP tools share Python implementation. Six added tools cover style search, coverage,
reference fetching, draft preparation, actual image/prompt pairing and integrity audit.
The plugin has five skills, with draft2overview primary and design-mcm-figure a compatibility route.
MCP uses the official SDK stdio transport, without an HTTP daemon.

AnySearch 3.1.1-compatible REST discovers academic capabilities, then searches academic or general web.
The full installed AnySearch skill supports batch/hybrid discovery. Only normalized records persist;
secret-bearing response envelopes never do. Search hits never automatically become curated cases.

Conceptual overview generation uses the host's available image tool. Full prompt and evidence brief
must accompany the actual image. Pairing validates a raster artifact and its source snapshot; it cannot
establish image-model provenance, scientific fidelity or whether visual review really occurred.
Host review and user acceptance are not inferred from checksums.

The auxiliary Matplotlib renderer validates data shapes, alignment, finite values, time ordering and
interval meaning before creating PNG/SVG/PDF bundles. It never fits arbitrary models. Workflow SVG is
a constrained node/edge fallback. Native PowerPoint, OCR, SHAP calculation and automatic manuscript
insertion are not provided by this runtime. Real data plots never come from image generation.

Tests use explicitly synthetic fixtures; engineering success is not a claim about contest performance.
