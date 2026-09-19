---
name: audit-modeling-figure
description: Review modeling diagrams and quantitative figures for source fidelity, correct numerical semantics, readable axes and reproducible data bindings; inspect actual renders and return focused corrections.
---

# Audit Modeling Figure

Read spec.json, data.json, source notes and the actual figure. Call `atlas_audit` on a generated bundle. Integrity checks cannot establish scientific validity or visual acceptance.

Check the claim against the underlying inputs. Confirm units, axes, plotted subsets, prediction vs observation, interval meaning, baseline, optimization directions and attribution. For diagrams, compare model dependencies and feedback to the paper. For empirical plots, verify quantities were computed from actual supplied data; preserve demo labels.

Inspect readability at publication size, especially legends, long categories, mathematical notation and Chinese glyphs. Return findings as: affected object/field, evidence, minimal correction, verification needed. Apply corrections when requested, rerender into a new version and compare. Read-only audit requests do not authorize edits.

Mark machine audit, assistant visual review and user approval separately. A clean checksum or correct file format never implies a verified scientific conclusion.
