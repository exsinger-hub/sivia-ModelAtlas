"""Retrieval must expose actionable design advice without changing source evidence."""
from pathlib import Path

from modelatlas.corpus import coverage, load_corpus, search_styles
from modelatlas.guidance import design_guidance, load_guidance


ROOT = Path(__file__).resolve().parents[1]


def test_guidance_does_not_inflate_award_or_research_collections():
    stats = coverage()
    assert (stats["papers"], stats["cases"]) == (29, 40)
    assert (stats["award_papers"], stats["award_cases"]) == (26, 36)
    assert (stats["research_papers"], stats["research_cases"]) == (3, 4)
    data = load_guidance()
    assert set(data["profiles"]) == set("ABCDEF")
    for profile in data["profiles"].values():
        assert all(profile[k] for k in ("use_when", "carriers", "layout", "avoid", "checks"))
    cases = {c["id"] for c in load_corpus()["cases"]}
    for case_id, notes in data["case_notes"].items():
        assert case_id in cases
        assert (ROOT / notes["prompt_example"]).is_file()
        assert notes["scientific_guards"]
        assert notes["status"] == "user_approved_showcase"
        assert notes["approved_on"] == "2026-09-20"
        assert (ROOT / notes["evidence"]).is_file()


def test_retrieval_returns_different_objects_and_actual_paper_guards():
    targets = {"C": "c-infer-compare-redesign", "D": "d-wins-to-value-chain",
               "F": "f-cyber-policy-evidence-map"}
    layouts = set()
    for problem, case_id in targets.items():
        case = next(c for c in search_styles(problem=problem, limit=100) if c["id"] == case_id)
        advice = case["design_guidance"]
        assert advice["problem_profile"] == problem
        assert advice["case_notes"]["scientific_guards"]
        assert advice["review_questions"]
        assert advice["style_provenance"]["installed_version"] == "1.1.0+codex.20260909060506"
        layouts.add(advice["profile"]["layout"])
        # Advice cannot silently modify pinned paper evidence or award membership.
        source = next(c for c in load_corpus()["cases"] if c["id"] == case_id)
        assert all(case[k] == value for k, value in source.items())
    assert len(layouts) == 3


def test_guidance_is_fresh_and_cannot_be_mutated_through_a_previous_result():
    case = load_corpus()["cases"][0]
    first = design_guidance(case)
    first["profile"]["carriers"].clear()
    assert design_guidance(case)["profile"]["carriers"]


def test_pdf_reread_guidance_keeps_source_conflicts_and_model_boundaries():
    notes = load_guidance()["case_notes"]
    assert len(notes) == 5
    guards = {key: " ".join(value["scientific_guards"]) for key, value in notes.items()}
    assert "Eq.12" in guards["a-typed-ecological-relations"]
    assert "no re-entry" in guards["b-rescue-multiscale-overview"]
    assert "argmax" in guards["c-infer-compare-redesign"]
    assert "E[min(d,K)|x]" in guards["d-wins-to-value-chain"]
    assert "weighted" in guards["d-wins-to-value-chain"]
    assert "excludes GDP" in guards["f-cyber-policy-evidence-map"]
