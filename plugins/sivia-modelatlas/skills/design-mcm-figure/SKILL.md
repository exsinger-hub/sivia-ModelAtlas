---
name: design-mcm-figure
description: Compatibility entry for SIVIA ModelAtlas manuscript figures. Route MCM/ICM draft-to-overview and Our Work figures to draft2overview; use simple vector workflows only when that format is requested.
---

# Design MCM Figure

Read and follow [draft2overview](../draft2overview/SKILL.md) for manuscript overview requests.
Input is a draft or explicit model notes, not a problem to solve. Default conceptual drawing is host
ImageGen following source-grounded design; numeric plots use real data. Do not default to the legacy
workflow-node JSON renderer for every overview.

For an explicitly requested simple editable SVG flowchart, read
[modeling grammar](references/modeling-grammar.md), create a source-grounded workflow spec, run
`atlas_render`, inspect the actual result and preserve its spec/data/prompt/output. This constrained
node/edge renderer is not native PowerPoint. Respect the requested format.
