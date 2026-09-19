# MCM/ICM visual grammar

Choose the organizing relation from the problem. An optimization question often needs constraints → feasible candidates → objectives → decision. A time-series question needs observation → feature window → model → forecast → held-out validation. A systems question benefits from state, transition and feedback. These are options, not universal templates.

Use one shared visual language: input/data, transformation/model, diagnostic/evidence, recommendation. Label feedback by what changes (parameter, assumption or data). Show shared inputs as shared inputs rather than suggesting sequential dependence. Preserve parallel models when they are compared or ensembled.

For MCM C, make the data-to-prediction and prediction-to-evaluation links explicit. For B/D, show objectives, constraints and candidate solutions. For A/E, preserve physical units, conservation assumptions and scenario boundaries. For F, keep model-derived implications distinct from policy choices. These are figure-planning heuristics, not official scoring rules.

Data graphics use exact values from data/model outputs. Prediction bands need a supplied statistical or scenario definition. Importance is not causality; a non-dominated candidate set is not proof of a global Pareto frontier. ACF, Sobol or SHAP labels require the corresponding computed quantities.

Conceptual illustrations may use scenes and icons. Color has a semantic role and is reinforced with line style or labels. At publication size, the main message and branch direction should be readable before small annotations. Keep full source locators and long explanations in the paired case record.
