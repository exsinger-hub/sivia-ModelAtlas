"""Check the saved execution artifacts, not scientific validity or image quality."""
from pathlib import Path

from PIL import Image

from modelatlas.common import digest, read_json
from modelatlas.corpus import load_corpus


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
    first, edit = brief["generation"]["chain"]
    assert first["operation"] == "generate"
    assert edit["operation"] == "edit"
    assert first["output"] == edit["input"] == "overview-v1.png"
    assert digest(EXAMPLE / first["output"]) == first["sha256"]
    assert edit["output"] == "overview.png"
    for name in ("overview.png", "overview-v1.png"):
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
    assert brief["review"]["status"] == "pending"
    assert brief["review"]["publication_gate"] == "pending"
    assert brief["review"]["user_approval"] == "not_recorded"
    assert len(brief["manuscript_evidence"]) >= 7
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/examples/2025-e-paper2overview/overview.png" in readme
    assert "这张图由 ModelAtlas 阅读论文后生成" in readme
