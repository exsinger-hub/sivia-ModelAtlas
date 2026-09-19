"""README previews must render from tracked assets with preserved attribution."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from PIL import Image

from modelatlas.common import digest, read_json
from modelatlas.corpus import load_corpus


ROOT = Path(__file__).resolve().parents[1]


class ReadmeHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.ids = set()
        self.link_stack = []
        self.details_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "details":
            self.details_depth += 1
        if tag == "a":
            self.link_stack.append(attrs.get("href"))
            if attrs.get("href"):
                self.links.append(attrs["href"])
        if tag == "img":
            self.images.append({
                **attrs,
                "link": self.link_stack[-1] if self.link_stack else None,
                "details_depth": self.details_depth,
            })

    def handle_endtag(self, tag):
        if tag == "a" and self.link_stack:
            self.link_stack.pop()
        if tag == "details":
            self.details_depth -= 1


def parse_readme():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    parsed = ReadmeHTML()
    parsed.feed(text)
    return text, parsed


def test_readme_embeds_real_reference_images_and_licenses():
    text, parsed = parse_readme()
    embedded = [image["src"] for image in parsed.images]
    embedded += re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
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


def test_showcase_is_first_visible_full_width_image_and_cards_keep_aspect_ratio():
    _, parsed = parse_readme()
    local = [image for image in parsed.images if not urlsplit(image["src"]).scheme]
    assert local[0]["src"] == "docs/examples/2025-e-paper2overview/overview.png"
    assert local[0]["width"] == "100%"
    assert local[0]["details_depth"] == 0
    for image in local:
        assert image["alt"].strip()
        assert image["link"] == image["src"]
        assert image.get("width") == "100%"
        assert "height" not in image  # Don't distort artwork to equalize card heights.
        assert (ROOT / image["src"]).is_file()
    visible = {image["src"] for image in local if image["details_depth"] == 0}
    assert "docs/assets/reference-overviews/2025-e-2515324-overview.jpg" in visible
    assert "docs/assets/reference-overviews/2026-c-2627351-overview.png" in visible
    assert parsed.details_depth == 0


def test_readme_local_navigation_and_category_anchors_resolve():
    text, parsed = parse_readme()
    targets = parsed.links + re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text)
    for target in targets:
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            continue
        path = (ROOT / unquote(parts.path)) if parts.path else ROOT / "README.md"
        assert path.exists(), target
        if parts.fragment:
            document = ReadmeHTML()
            document.feed(path.read_text(encoding="utf-8"))
            assert unquote(parts.fragment) in document.ids, target
    assert {"showcase", "library", "quick-start", "setup"} <= parsed.ids
