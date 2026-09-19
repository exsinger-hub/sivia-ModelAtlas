"""Original composition guidance, kept separate from scientific source records."""
from copy import deepcopy
from importlib.resources import files
import json


def load_guidance():
    data = json.loads(files("modelatlas").joinpath("knowledge/visual-guidance.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or set(data["profiles"]) != set("ABCDEF"):
        raise ValueError("Invalid visual guidance schema")
    return data


def design_guidance(case, problem=None):
    """Return usable object-level advice without upgrading a generated example to a source."""
    data = load_guidance()
    target = problem if problem in case["problem_targets"] else case["problem_targets"][0]
    return deepcopy({
        "scope": data["scope"],
        "problem_profile": target,
        "profile": data["profiles"][target],
        "review_questions": data["global_review"],
        "case_notes": data["case_notes"].get(case["id"]),
        "style_provenance": data["sivia_reference"],
    })
