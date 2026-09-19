# SIVIA ModelAtlas

Only product: Paper → Overview. Read an existing paper/manuscript, retrieve and view appropriate
illustrations, design a source-grounded overview, generate via the host ImageGen tool, inspect/correct,
and deliver actual image + full prompt + evidence/caption. Do not branch into contest solving,
paper writing, standalone data plotting, generic dashboards or editable deck construction.

One plugin skill: paper2overview. Runtime intake is atlas_prepare_paper / modelatlas paper2overview;
it snapshots/extracts a paper and suggests references, not a generated image.
Keep file-integrity audit, actual visual review and user acceptance separate.

Preserve the illustration knowledge base and README's knowledge-base section. corpus.json retains
all verified sources/cases, including supporting non-overview illustrations. These are references,
not extra renderer capabilities. Default user-facing retrieval to overview; preserve year/problem,
official O/F proof, pinned source SHA, PDF page and figure labels. Research is a separate collection.
Use AnySearch for public source discovery, not private manuscript disclosure.

Paper content governs every model/edge/result; references guide composition only. Never copy source
scientific claims or fabricate numerical evidence. A downloaded page is not a viewed illustration.
Do not claim execution from a prompt or intake JSON alone.

Keep .modelatlas, outputs, existing local SQLite files, PDFs and credentials untouched by cleanup.
User-requested feature deletion applies to tracked code, not private artifacts. Deleted code remains
recoverable in Git history. Do not modify adjacent Sivia checkouts.
