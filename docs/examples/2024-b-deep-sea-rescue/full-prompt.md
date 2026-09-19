# Complete ImageGen prompt record

## Call 1 · generate

Output: `overview-v1.png` · artifact `exec-a5a48898-6c3a-40ea-a4ac-b822eb854c7e.png`.

Use case: scientific-educational
Asset type: an English method overview for an MCM paper, landscape 3:2, white background.

Purpose and authority
Create a precise, visually engaging scientific plate titled "Locate, equip and search" based on "Unlocking the Abyss: A Dynamical Model for Deep-Sea Adventure Safety and Rescue Strategies", Team 2407038, 2024 MCM B. The figure explains how ocean dynamics predicts a lost submersible's position, how equipment is selected, and how searched cells update the next deployment. Use the paper's Sections 4–9 only. Intended at 180 mm text width. Depict a method schematic, not operational rescue advice or claimed empirical predictions. No invented coordinates, probabilities, Pareto scatter points, fitted curves or performance numbers.

Composition
Use an ocean cross-section as the main upper-left and center scene (roughly 55% of the canvas), a compact preparation branch in the upper-right (35%), and a broad time-updated search strip below. Keep white gutters and a quiet thin blue waterline; the ocean is an isolated illustration, not a dark full-page background. Rescue vessel above the water, small powerless submersible below, a pale seabed, two or three short current arrows, all crisp and legible. Use a distinct navy/sea-teal palette with restrained amber for uncertainty and search selection. No generic grid of rounded cards.

Region A: "Locate"
Beside the cross-section, three small data labels: "Currents", "Density", "Seafloor". Currents connects to "ARIMA + Monte Carlo"; currents and density connect to "Ridge regression". Both feed "Motion model" near the submersible. Seafloor connects directly to the motion model as a boundary constraint. A compact annotation under the vehicle reads "Gravity · buoyancy · drag". A short dotted conceptual path ending at a hollow locator symbol illustrates "Predicted position"; label the path "Schematic trajectory" so it cannot be confused with a computed result. Do not connect that path to the top vessel as a cable. Keep all data-processing arrows outside the illustrative water scene's small labels.

Region B: "Prepare"
Show five minimal instrument silhouettes in a tidy horizontal cluster, captioned collectively "Sonar · pinger · magnetometer · camera"; no fake brand names. Below them, three short objective labels stacked with good breathing room: "Cost ↓", "Availability ↑", "Readiness time ↓". These feed "Genetic algorithm" and then "Equipment allocation", illustrated by one larger host ship and two smaller rescue-boat silhouettes. This is a multi-objective selection branch; no ranking or numerical optimization result is drawn. A downward arrow from allocation joins the search strip at "Deploy".

Region C: "Search and update"
In the bottom strip, use a left-to-right sequence of four visually meaningful objects rather than four identical boxes: a small unnumbered cell grid labeled "Poisson grid prior"; a boat inspecting a selected amber cell labeled "Deploy"; a checked-off cell grid labeled "Search evidence"; and a redistributed grid labeled "Bayesian update". The grids are monochrome schematic partitions, NOT numerical heatmaps: use outline / hatch / highlight distinctions, no continuous color scale and no values. The "Predicted position" above feeds the first grid, not the equipment branch. Connect prior -> deploy -> evidence -> update with clear dark arrows. One curved return arrow from update back to deploy, routed along the strip's lower edge, is labeled "Next interval". A tiny note under searched cells: "Searched cells excluded in this model". This is the paper's search assumption, not a universal statement about real search and rescue. Label the region footer "Conceptual search cycle".

Evaluation and extension
Across the bottom margin, a separate light outlined band labeled "Checks and extensions" contains three short entries: "Search-interval sensitivity", "Other sea regions", "Multiple submersibles". Link the search strip to this band with one plain thin connector. No claims of perfect detection outside the explicitly modeled assumption and no new algorithms such as neural networks, RRT or Kalman filtering.

Visual grammar and typography
Strong hierarchy, fine consistent outlines, subdued seawater blue, generous white space. The submersible and equipment provide semantic imagery; keep icons restrained and distinct. Exact quoted labels only, no paragraphs. Dark readable sans-serif type, semibold region headings. Keep the title below 6% canvas height and scientific labels large enough for reduction. Data-flow connectors have arrowheads; illustrative current arrows are thin teal and confined underwater; feedback is dashed amber. Avoid connector crossings, especially between the preparation branch and localization inputs.

Reference adaptation and final checks
The inspected source overview (Figure 1, physical PDF p4) suggests separate locate/prepare/search tasks and a search-feedback loop. Preserve that narrative, not its screenshot, numerical example plots, tiny labels or dense ornamental outline boxes. No logos, watermarks, award badges, team numbers or source-author claims. Output only the finished complete overview. Check the two upstream branches merge only at search, feedback returns to deployment, and all charts remain explicitly schematic.

## Call 2 · edit

Input: `overview-v1.png`.

Output: `overview.png` · artifact `exec-8e193d2c-a800-4df8-b66a-6bb583147888.png`.

Use case: precise-object-edit
Asset: final manuscript overview, landscape 1536 x 1024.
Input image: edit target, the existing deep-sea rescue overview. Preserve the scientific panels, ocean scene, equipment, text typography, colors and legible grid cycle.

Make two narrowly scoped corrections:
1. Remove the two subtitle lines below "Locate, equip and search": remove the long paper title AND "Team 2407038 | 2024 MCM B". Leave just the main title with calm white space. No author, team, contest, award, branding or watermark anywhere.
2. The small extra orange "Deploy" box at the upper right of the Search and update region is disconnected from the real deployment and must disappear. Remove that duplicate box and the vertical equipment-to-box arrow. The actual boat step titled "Deploy" in the center-left of the search row is the ONLY deployment. Indicate the equipment allocation dependency via a small readable secondary label immediately below its existing "Deploy" heading: "Uses allocated equipment". Do not add a new long connecting arrow, new duplicate deployment or new boat. Keep the actual cycle: Poisson grid prior -> Deploy -> Search evidence -> Bayesian update, with dashed amber Next interval feedback from Bayesian update to the actual Deploy boat.

Invariants: currents -> ARIMA + Monte Carlo and ridge regression; density -> ridge regression; motion model bounded by seafloor; qualitative trajectory; three GA objectives cost down, availability up, readiness time down; equipment allocation; Poisson prior derived from predicted position; searched cells excluded in this model; Bayesian next-interval feedback. Keep conceptual search cycle label and checks/extensions strip. No new quantitative results. No other scientific edits, no flattening into a generic diagram. Read all labels before finishing.
