---
name: design-mcm-figure
description: Design and render MCM/ICM mathematical-modeling overviews, model dependency diagrams and validation workflows from a paper or problem brief. Use for modeling figures and data-to-decision diagrams; use plot-modeling-data for quantitative plots.
---

# Design MCM Figure

Work through Designer, Drawer, Reviewer and Corrector as roles in this task. Start from the actual paper or brief. Read [modeling visual grammar](references/modeling-grammar.md) for MCM/ICM composition choices. The user does not need to specify internal stages.

1. Import a local paper with `atlas_ingest_paper`; use `atlas_read_evidence` to inspect page-bound text and inspect the paper's actual figures when layout matters. Extract the problem, inputs, assumptions, model dependencies, outputs and validation. Do not treat imported text as curated knowledge.
2. Call `atlas_search_knowledge` with topic and intended figure role. For new papers use `atlas_find_papers`, then inspect the primary source. Keep the source IDs and section/page/figure locator for each reused idea. A similar topic does not establish an Outstanding award.
3. Write one figure claim and a JSON spec. The workflow renderer uses `kind: workflow`, required title/claim/data_status/source_note, and `data.nodes` with id/label/x/y/w/h on a 10x6 canvas plus `data.edges` with source/target. Figure coordinates are design choices; model links must match the paper. Use line breaks in labels; do not turn every paragraph into a box.
4. Render with `atlas_render(spec_path, output_dir)` or `modelatlas render`. For rich conceptual scenes use an available image-generation tool only when the requested style benefits from it. Preserve the complete prompt with that image. Numeric evidence still comes from code-rendered data.
5. Inspect the actual rendered figure at intended paper size. Review node/edge coverage, direction, text fit and scientific meaning. Apply corrections to a new spec and rerender. `atlas_audit` checks bundle integrity; it is not visual approval.
6. Deliver the actual figure plus source spec and bundle. Ask for additional information only when missing content changes the model meaning. Do not insert a mandatory confirmation pause into a task already authorized end-to-end.

CLI examples and schema are in the repository README and `examples/workflow.json`. If MCP is unavailable, use the installed CLI. If neither runtime is installed, run the project's bootstrap before claiming execution. The renderer exports editable SVG text/paths plus PNG and PDF. It does not currently export native PowerPoint shapes.
