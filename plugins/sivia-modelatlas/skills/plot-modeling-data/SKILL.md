---
name: plot-modeling-data
description: Create reproducible MCM/ICM and data-modeling charts from CSV/JSON or computed model outputs, including time series, forecasts, residuals, sensitivity, heatmaps and Pareto candidates. Export PNG, editable SVG and PDF with exact data bindings.
---

# Plot Modeling Data

Read the actual dataset and the user's intended comparison. Search `atlas_search_styles(role="data_plot", collection="award")` for reviewed O/F references and explicitly extend to research/explanation when appropriate. Fetch and view the relevant page before transferring its design. `atlas_search_knowledge` supplies secondary recipe guidance. Reuse communication principles, never the source paper's numbers; retain source locators.

Choose the recipe matching the question:

| kind | data | interpretation |
|---|---|---|
| line | x, y, optional y2 | ordered observations; x strictly increasing |
| forecast | x, y, predicted, optional lower/upper | supplied predictions, not automatic model fitting |
| scatter | x, y | observed association |
| residual | observed, predicted | residual = observed - predicted; computes RMSE/MAE |
| sensitivity | labels, low, high, baseline | outputs for low/high parameter scenarios; not Sobol |
| heatmap | rows, columns, values | matrix; correlation=true fixes [-1,1] |
| pareto | x, y; spec.directions = [min/max, min/max] | non-dominated provided candidates |

The JSON spec requires `kind`, `title`, `claim`, `data_status` (provided/empirical/demo), `source_note`, `x_label`, `y_label` and `data`. Include units and source_ids. A `data_file` may instead point to JSON or CSV relative to the spec; CSV needs a `columns` mapping such as `{x: day, y: observed, predicted: estimate}`. Missing/nonfinite values fail visibly; choose a justified cleaning step before rendering. Do not silently interpolate, sort, aggregate or discard data.

For forecast intervals, require `interval_label` describing their actual meaning. Do not invent a confidence level. A train/test marker is supplied as `split_x`. The backend accepts already computed outputs; fitting a model is a separate analysis step.

Call `atlas_render` or `modelatlas render <spec> --output <dir>`. Inspect the PNG and the saved audit, fix errors in a new spec and rerender. Each run contains figure.png/svg/pdf, spec.json, data.json, prompt.md, audit.json and manifest.json. Keep the data status visible, especially demo examples. Use `atlas_audit` for bundle integrity. Return the figure plus editable source and explain unresolved scientific ambiguity only when it affects interpretation.

For plots outside the implemented recipes, write and run a task-specific plotting script with the user's data, preserving the same case pairing. Do not claim unsupported map/network/SHAP/PPTX rendering exists in the built-in backend.
