"""Check the saved execution artifacts, not scientific validity or image quality."""
from pathlib import Path
import hashlib

from PIL import Image

from modelatlas.common import digest, read_json
from modelatlas.corpus import load_corpus
from modelatlas.prompting import check_prompt


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "docs/examples/2025-e-paper2overview"


def test_generated_example_preserves_real_images_and_source_binding():
    brief = read_json(EXAMPLE / "brief.json")
    design = read_json(EXAMPLE / "design-spec.json")
    paper = next(p for p in load_corpus()["papers"] if p["id"] == "icm-2025-e-2515324")
    assert design["source"]["pdf_sha256"] == paper["sha256"]
    assert brief["generation"]["backend"] == "built-in image_gen.imagegen"
    assert digest(EXAMPLE / "overview.png") == brief["generation"]["image_sha256"]
    assert brief["generation"]["actual_size"] == [1536, 1024]
    first, edit, scene, correction, final = brief["generation"]["chain"]
    assert first["operation"] == "generate"
    assert edit["operation"] == "edit"
    assert first["output"] == edit["input"] == "overview-v1.png"
    assert digest(EXAMPLE / first["output"]) == first["sha256"]
    assert edit["output"] == "overview-v2.png"
    assert scene["operation"] == "generate" and "input" not in scene
    assert scene["output"] == correction["input"] == "overview-scene-v1.png"
    assert correction["output"] == final["input"] == "overview-scene-v2.png"
    assert final["output"] == "overview.png"
    assert digest(EXAMPLE / "overview.png") == "5719c0af8dc5ba5b5fcb17f6fa053aa1e65d37a15fceebef10f37089ea12fa5f"
    for call in brief["generation"]["chain"]:
        name = call["output"]
        assert digest(EXAMPLE / name) == call["sha256"]
        with Image.open(EXAMPLE / name) as image:
            assert image.format == "PNG" and image.size == (1536, 1024)
            image.verify()
    assert digest(EXAMPLE / "overview.png") != digest(EXAMPLE / "overview-v1.png")


def test_generated_example_keeps_prompts_and_review_boundaries():
    brief = read_json(EXAMPLE / "brief.json")
    combined = (EXAMPLE / "full-prompt.md").read_text(encoding="utf-8")
    for call in brief["generation"]["chain"]:
        assert (EXAMPLE / call["prompt"]).read_text(encoding="utf-8").strip() in combined
    assert brief["generation"]["empirical_rerun"] is False
    assert brief["generation"]["native_editability"] is False
    assert brief["review"]["status"] == "needs_revision"
    assert brief["review"]["publication_gate"] == "approved_for_project_showcase"
    assert brief["review"]["user_approval"] == "approved"
    assert brief["review"]["scientific_publication_gate"] == "needs_revision"
    assert brief["review"]["knowledge_base_admission"] is False
    assert brief["review"]["approval_evidence"]["user_message"] == "这个很不错,可以推送"
    assert brief["review"]["issues"]
    assert len(brief["manuscript_evidence"]) >= 7
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/examples/2025-e-paper2overview/overview.png" in readme
    assert "阅读全文后重新设计" in readme
    assert "奖项属于来源论文" in readme


def test_scene_series_preserves_exact_submitted_text_and_local_edit_scope():
    brief = read_json(EXAMPLE / "brief.json")
    records = read_json(EXAMPLE / "scene-prompt-records.json")
    scene_calls = brief["generation"]["chain"][2:]
    assert len(records["calls"]) == len(scene_calls) == 3
    for record, call in zip(records["calls"], scene_calls):
        raw = (EXAMPLE / call["prompt"]).read_bytes()
        assert raw == record["submitted_prompt"].encode("utf-8")
        assert hashlib.sha256(raw).hexdigest() == call["prompt_sha256"]
        if call["operation"] == "generate":
            report = check_prompt(raw.decode("utf-8"))
            assert report["passed"]
            assert call["prompt_detail"]["template_bytes_verified"]
            for key in ("submitted_utf8_sha256", "total_characters", "non_whitespace_characters"):
                assert report[key] == call["prompt_detail"][key]
        else:
            assert call["prompt_scope"] == "localized_correction"
    old = read_json(EXAMPLE / "brief-before-scene.json")
    assert digest(EXAMPLE / "overview-v2.png") == old["generation"]["image_sha256"]
    assert old["review"]["user_approval"] == "not_recorded"
