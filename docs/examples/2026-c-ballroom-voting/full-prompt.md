# Complete ImageGen prompt record

## Call 1 · generate

Output: `overview-v1.png` · artifact `exec-1868dfcd-e20a-4848-adb5-4e3def5f43d1.png`.

Use case: infographic-diagram
Asset: English paper-to-overview illustration, landscape 1536 x 1024, intended180mm full-text width before assumptions.
Purpose: Explain "Behind the Ballroom Scores: Reconstructing Fan Voting and Designing Fairer Rules for DWTS". Hidden fan SHARE is inferred under a rule, then supports two parallel analyses and a redesigned weekly voting mechanism. Votes are not directly observed; never claim the true vote totals are recovered. Draw no empirical result values.

Composition: clean PURE WHITE (#FFFFFF) page with crisp navy sans-serif text, no dark background, no blurred glow, no shadows or vignette. Refined editorial, flat vector-like scientific illustration with muted teal, violet and warm amber accents. Main short title "Behind the ballroom scores". Organize into upper shared inference (45%), middle two parallel analysis scenes (30%), lower targeted rule design (25%). Meaningful ballroom, judge, fan and ballot motifs integrated with methods, no cluttered unrelated icons.

Top-left compact input scene titled "Observed weekly data": a small stylized dancing pair (no real people), beside a judge scorecard WITHOUT numbers, an elimination roster with neutral check/cross symbols. Exact input labels "Judge scores", "Eliminations", "Contestant traits". Small clean preprocessing label "Clean + normalize".

Top-right dominant region titled "Infer hidden fan support": two complementary side-by-side units, not a serial chain. Unit A "Feasible set" with a simple convex polygon schematic and short label "Share intervals"; Unit B "Plackett–Luce likelihood" with small abstract contestant probability tokens and short label "Point estimates". One shared bracket beneath: "Rule-conditional fan shares". A small nearby note "Not observed vote totals". Below, a narrow diagnostics band: "Feasibility · consistency · uncertainty". No fake confidence interval values, fake distributions, axis ticks or percentages. Connect cleaned judge scores and eliminations to BOTH units via clean splitter. Contestant traits remain available to the lower-right analysis.

Middle-left region title "Compare voting rules": three mini ballot cards labeled "Rank", "Percentage", "Judges' Save". Same judge scores and inferred shares feed all three through one input bar. Beneath, text "Same contestants · same week". Bottom label "Cross-inference audit". Use symbols and routes to convey alternative rule applications, NOT a sequence Rank->Percentage->Judges'Save. Avoid full-season replay imagery. Direct down-arrow from shared inference output into this region.

Middle-right region title "Separate contestant and partner effects": a dancer-pair glyph beside "Mixed-effects models", branching to two outcomes "Judges" and "Fans". Small two-line annotations "Traits + season effects" and "Pro + celebrity intercepts". Direct down-arrow from shared inference output into this region; an independent small input "Contestant traits" at its side. Do not draw an arrow from rule comparison into mixed-effects, because these are parallel analyses, not serial dependencies. Do not imply fully propagated inference uncertainty: use label "Fan point estimates" on the input to the Fans analysis if space permits.

Bottom central wide rule-design band title "MARS-Soft+Disagreement". Main three-step sequence "Rank-sum baseline" -> "Targeted soft protection" -> "Weekly elimination". Under the middle protection step place a legible AND gate text: "High judge rank + weaker fan rank". Show this as the necessary condition for protection, not universal rescue. Two evidence arrows merge from the middle analysis regions into this bottom region, each ending clearly at the band boundary.

Bottom-most slim separated evaluation strip: "Tune: seasons1–17" -> "Test: seasons18–34"; four short metric labels alongside: "Rescue", "Balance", "Fan impact", "Changes". These are source-defined train/test groups, not fabricated outcome numbers. One tiny footer: "Method overview · schematic".

Visual grammar: teal observed/inferred data, violet comparative analysis, blue hierarchical effects, warm amber proposed mechanism. Dark consistent connectors, no connector through words or dancer art; separate clean gutters. Short titles, readable text, ample padding. Use en dash in seasons only if legible. Do not place full paper title, sources/page numbers, awards, team ID, institution or watermark inside image.

Evidence authority (instructions ONLY, do not print these sections): PDFphysicalpp7–10 section4 feasible-set/likelihood and nonunique rule-conditional relative support; pp11–14 section5 week-level counterfactual Rank/Percentage/Save and cross-inference; pp14–18 section6 mixed-effects uses estimated fan shares as point inputs and does not model measurement error; pp18–20 section7 gated rank-based MARS and temporal split; pp21–22 sensitivity. This is a method map, not evidence of reproduced results or a full-season simulation.

Reference adaptation: inspected source Figure1 at PDFp5. Retain shared inference, fork into rule audit and trait effects, converge on redesign. Replace generic rounded-box inventories with meaningful scenes. Do not copy source image pixels or its ambiguous lateral arrow.
Final checks: feasible-set and likelihood complementary; fan shares not actual vote totals; rule comparison and mixed-effects parallel; judge-elite AND fan disagreement gate visible; weekly not season-long counterfactual; tuning earlier seasons, testing later; no generated quantitative results; white background and sharply legible typography.

## Call 2 · edit

Input: `overview-v1.png`.

Output: `overview.png` · artifact `exec-de79de9c-1d90-41d5-ac61-b0eced737788.png`.

Use case: precise-object-edit. Edit the supplied ballroom overview; keep scientific labels, icons, two complementary inference units, two middle analysis panels and bottom MARS mechanism. Fix only contrast and critical connector routing.
1. Replace ALL blurred, smoky, dark gradient background outside panels with solid pure white (#FFFFFF). No halos, no vignette, no dark areas. Main title "Behind the ballroom scores" is solid navy on pure white. Keep panel interiors very light. Match clean flat journal style.
2. The current long connector running from observed data to Compare voting rules is misleading. Remove that downward branch entirely. Observed data -> inference only, as one arrow that clearly terminates at the LEFT BORDER OF THE WHOLE "Infer hidden fan support" container (not at Feasible set alone). Both inference units share that input.
3. Draw a SINGLE output fork from the center bottom of the "Infer hidden fan support" region, at the "Rule-conditional fan shares" output level, through an unobstructed horizontal gutter between top and middle panels. LEFT branch ends at TOP CENTER BORDER of "Compare voting rules". RIGHT branch ends at TOP CENTER BORDER of "Separate contestant and partner effects". Route both branches in the gap; make no line through text or drawings. Remove the two old parallel downward arrows that currently feed only the right panel. Each middle panel gets exactly one inference input arrow.
4. On the right panel replace the small text "Fan point estimates" beside the Fans outcome with "Inferred fan signal". This is an outcome constructed from inferred shares, not directly observed votes.
Preserve the lower analysis-to-MARS convergence, conditional protection "High judge rank + weaker fan rank (AND)", rank-sum -> soft protection -> weekly elimination, temporal Tune1–17 / Test18–34 and four evaluation metrics. Preserve "Not observed vote totals", feasibility/consistency/uncertainty and cross-inference audit. No team ID, author name, badges or new numerical results. All method text must be clearly readable against white.
