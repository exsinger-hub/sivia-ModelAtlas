"""README previews must render from tracked assets with preserved attribution."""
import re
from pathlib import Path

from PIL import Image

from modelatlas.common import digest, read_json
from modelatlas.corpus import load_corpus


ROOT = Path(__file__).resolve().parents[1]


def test_readme_embeds_real_reference_images_and_licenses():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    embedded = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
    directory = ROOT / "docs/assets/reference-overviews"
    manifest = read_json(directory / "manifest.json")
    cases = {c["id"]: c for c in load_corpus()["cases"]}
    assert len(embedded) >= 2
    assert "不是 ModelAtlas 生成结果" in text
    for asset in manifest["assets"]:
        path = directory / asset["file"]
        assert path.relative_to(ROOT).as_posix() in embedded
        assert digest(path) == asset["sha256"]
        with Image.open(path) as image:
            assert image.size == (asset["width"], asset["height"])
            image.verify()
        case = cases[asset["case_id"]]
        assert (case["paper_id"], case["pdf_page"], case["figure"]) == (
            asset["paper_id"], asset["pdf_page"], asset["figure"])
        license_text = (directory / asset["license_file"]).read_text(encoding="utf-8")
        assert asset["copyright"] in license_text and "Permission is hereby granted" in license_text
        assert asset["kind"] == "reference_not_generated"
        assert asset["source_url"].startswith("https://github.com/")
