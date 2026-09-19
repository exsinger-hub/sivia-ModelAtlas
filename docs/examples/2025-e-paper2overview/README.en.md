# From Forest to Farm · 2025 ICM E

[中文](README.md) · [All examples](../../../README.en.md#showcase)

Source paper: *From Forest to Farm: Modeling Nitrogen Dynamics for Sustainable Agriculture*.
Team **2515324**, **Finalist**. The award belongs to the paper, not to the generated figures.

## Original and current redesign

| Authors’ original · Figure 2, PDF p4 | ModelAtlas · Round 2 |
| :---: | :---: |
| [![Original overview](../../assets/reference-overviews/2025-e-2515324-overview.jpg)](../../assets/reference-overviews/2025-e-2515324-overview.jpg) | [![Current redesign](overview.png)](overview.png) |

## Generation rounds

| Round 1 · Initial draft | Round 2 · Revision |
| :---: | :---: |
| [![Round 1](overview-v1.png)](overview-v1.png) | [![Round 2](overview.png)](overview.png) |
| [Generation prompt](prompt.md) | [Correction prompt](correction-prompt.md) |

Round 2 moves the harvest arrow to the crop canopy, connects the food web to scenario analysis,
and continues right to left along the bottom. Forest decoration is simplified.
These are two consecutive ImageGen calls, not independent style candidates.

### Current image

![Current overview, round 2](overview.png)

[Full prompt history](full-prompt.md) · [Evidence & caption](brief.json) · [Initial design](design-spec.json)

## Source

- [Author repository](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model).
- [Pinned paper](https://github.com/LUKEQ420/MCM-ICM-2025-E-Nitrogen-Cycling-Model/blob/fb579acd7107706e055c8a10f921f9f56498a06a/paper/2515324.pdf), 25 pages.
- [COMAP award results](https://www.contest.comap.com/undergraduate/contests/mcm/contests/2025/results/2025_ICM_Problem_E_Results.pdf), physical page 6: Team 2515324, E, Finalist.
- PDF SHA-256: `2c566c95c1d4a1b4292176805253ad4f09ccfe9154e8809beb86f399347a8cdc`.
- Original figure: [source and MIT attribution](../../assets/reference-overviews/README.md).

The complete paper was read, including equations, results and the letter to farmers. The original
overview, nitrogen-cycle diagram and seven-node food web were inspected. Source PDFs remain local.
This is a redesign of a known reference paper, not a held-out benchmark or an empirical simulation rerun.

## Paper-to-figure mapping

| Figure content | Paper evidence |
| --- | --- |
| Conserved forest nitrogen cycle | pp4–8, §§2 and 4, Eqs2–5 |
| Crops, weeds, seasons and farm management | pp9–15, §5, Eqs6–14 |
| Seven-node food web, nine trophic edges | pp16–18, Figure 9, Eqs15–20 |
| Euler simulation, scenarios and nitrogen metrics | pp18–21, §§6.1.3–6.3.1 |
| Crop–weed sensitivity | pp22–23, §8 |
| Rhizobia, legumes and straw reuse | pp21–22, §7; literature-supported recommendations |

No numerical results were generated. Nitrogen turnover remains the authors’ stability proxy;
recommendations supported by literature are separated from simulated scenarios. The uptake-term
notation in Eq5 conflicts with nearby text/Eq2; the figure follows the stated compartment mechanism
without claiming to correct the equation or validate the numerical results.

## Review and delivery

Both actual outputs are **1536 × 1024 PNGs**, generated and edited with the host ImageGen tool.
The source relationships and nine food-web edges were checked in a visual self-review. The current
image, full prompt and evidence are paired; [file integrity checks](integrity-audit.json) passed.

Print-size proof, independent review and user approval remain pending. The PNG is not natively editable.
Suggested placement: §1.3 Our Work, at full text width (180 mm, pending print-size verification).
The English caption and detailed review record are in [brief.json](brief.json).

Scientific content belongs to the source authors. These workflow examples do not imply their endorsement.
