"""README previews must render from tracked assets with preserved attribution."""
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pytest
from PIL import Image

from modelatlas.common import digest, read_json
from modelatlas.corpus import coverage, load_corpus


ROOT = Path(__file__).resolve().parents[1]
READMES = ("README.md", "README.en.md")


class ReadmeHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.links = []
        self.ids = set()
        self.link_stack = []
        self.details_depth = 0
        self.table_rows = []
        self.current_row = None

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
        if tag == "tr":
            self.current_row = []
        if tag == "img":
            self.images.append({
                **attrs,
                "link": self.link_stack[-1] if self.link_stack else None,
                "details_depth": self.details_depth,
            })
            if self.current_row is not None:
                self.current_row.append(attrs["src"])

    def handle_endtag(self, tag):
        if tag == "a" and self.link_stack:
            self.link_stack.pop()
        if tag == "details":
            self.details_depth -= 1
        if tag == "tr" and self.current_row is not None:
            if self.current_row:
                self.table_rows.append(self.current_row)
            self.current_row = None


def parse_readme(name="README.md"):
    text = (ROOT / name).read_text(encoding="utf-8")
    parsed = ReadmeHTML()
    parsed.feed(text)
    return text, parsed


def test_original_reference_assets_keep_integrity_and_licenses():
    directory = ROOT / "docs/assets/reference-overviews"
    manifest = read_json(directory / "manifest.json")
    cases = {c["id"]: c for c in load_corpus()["cases"]}
    for asset in manifest["assets"]:
        path = directory / asset["file"]
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


@pytest.mark.parametrize("name", READMES)
def test_showcase_pairs_each_paper_with_only_its_final_image(name):
    text, parsed = parse_readme(name)
    local = [image for image in parsed.images if not urlsplit(image["src"]).scheme]
    assert text.index('id="showcase"') < text.index("## Quick Start")
    for image in local:
        assert image["alt"].strip()
        assert image["link"] == image["src"]
        assert image.get("width") == "100%"
        assert "height" not in image  # Don't distort artwork to equalize card heights.
        assert image["details_depth"] == 0
        assert (ROOT / image["src"]).is_file()
    showcase = read_json(ROOT / "docs/examples/showcase.json")
    expected_images = set()
    expected_rows = []
    for case in showcase["cases"]:
        assert case["id"] in parsed.ids
        assert f'category-{case["problem"].lower()}' in parsed.ids
        latest = next(r for r in case["rounds"] if r["number"] == case["latest_round"])
        assert case["final_image"] == latest["image"]
        if case["presentation"] == "comparison":
            expected_rows.append([case["source_figure"], latest["image"]])
            expected_images.add(case["source_figure"])
        else:
            assert case["presentation"] == "standalone"
            assert case["source_figure"] is None
        expected_images.add(latest["image"])
        assert case["full_prompt"] in text
        for round_ in case["rounds"][:-1]:
            assert round_["image"] not in text  # History stays behind the case link.
    assert len(local) == len(expected_images) == 8
    assert len(expected_rows) == 2
    assert len(showcase["cases"]) == 6
    assert {c["year"] for c in showcase["cases"]} == {2024, 2025, 2026}
    assert {c["problem"] for c in showcase["cases"]} == set("ABCDEF")
    assert parsed.table_rows == expected_rows
    assert {image["src"] for image in local} == expected_images
    assert parsed.details_depth == 0


@pytest.mark.parametrize("name", READMES)
def test_readme_local_navigation_and_category_anchors_resolve(name):
    text, parsed = parse_readme(name)
    targets = parsed.links + re.findall(r"(?<!!)\[[^\]]*\]\(([^)]+)\)", text)
    for target in targets:
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            continue
        path = (ROOT / unquote(parts.path)) if parts.path else ROOT / name
        assert path.exists(), target
        if parts.fragment:
            document = ReadmeHTML()
            document.feed(path.read_text(encoding="utf-8"))
            assert unquote(parts.fragment) in document.ids, target
    assert {"showcase", "library", "quick-start", "setup"} <= parsed.ids


@pytest.mark.parametrize("name", READMES)
def test_quick_start_has_checkout_runtime_and_actual_skill_entry(name):
    text, _ = parse_readme(name)
    quick = text.split("## Quick Start", 1)[1].split('id="library"', 1)[0]
    assert "git clone https://github.com/exsinger-hub/sivia-ModelAtlas.git" in quick
    assert "cd sivia-ModelAtlas" in quick
    assert "python -m venv .venv" in quick
    assert 'pip install -e ".[mcp]"' in quick
    skill = "plugins/sivia-modelatlas/skills/paper2overview/SKILL.md"
    assert skill in quick and (ROOT / skill).is_file()
    assert "ImageGen" in quick
    assert ("单独运行 CLI 只会准备论文与参考资料" in quick
            or "The CLI only prepares the paper and references" in quick)
    assert (ROOT / "docs/USAGE.md").is_file()


def test_library_documentation_matches_actual_records_and_year_gaps():
    text, _ = parse_readme()
    stats = coverage()
    assert f'{stats["award_papers"]} 篇 O/F 论文、{stats["award_cases"]} 个图例' in text
    assert f'{stats["research_papers"]} 篇科研论文、{stats["research_cases"]} 个扩展图例' in text
    english, _ = parse_readme("README.en.md")
    assert f'{stats["award_papers"]} O/F papers with {stats["award_cases"]} figure cases' in english
    assert f'{stats["research_papers"]} research papers with {stats["research_cases"]} additional cases' in english
    for document in (text, english):
        library = document.split('<a id="library"></a>', 1)[1].split("\n---", 1)[0]
        assert len(library.splitlines()) <= 7
        assert "<img" not in library and "<table" not in library
        assert "knowledge-base/SOURCES.md" in library
    catalog = (ROOT / 'knowledge-base/CATALOG.md').read_text(encoding='utf-8')
    for case in load_corpus()['cases']:
        assert catalog.count(f'`{case["id"]}`') == 1
    for year in stats['years']:
        row = f'| {year["year"]} | ' + ' | '.join(str(year['problems'][p] or '—') for p in 'ABCDEF') + ' |'
        assert row in catalog


def test_quick_start_documents_optional_editable_ppt_handoff():
    text, _ = parse_readme()
    quick = text.split("## Quick Start", 1)[1].split('id="library"', 1)[0]
    assert "转为可编辑 PPT 矢量图（可选）" in quick
    assert "使用 Sivia" in quick
    assert "仅安装 ModelAtlas 不包含此能力" in quick
    assert "Node.js" in quick and "PowerPoint / WPS" in quick
    assert "overview-editable.pptx" in quick
    assert "原生可编辑对象" in quick and "保留为位图" in quick
    assert "docs/USAGE.md#editable-ppt" in quick

    usage = (ROOT / "docs/USAGE.md").read_text(encoding="utf-8")
    assert "ModelAtlas 不内置 PNG → PPTX 转换器" in usage
    assert "从该 PPTX 导出的预览图" in usage
    assert "没有实际生成 PPTX 时，不标记转换完成" in usage


def test_english_readme_has_language_switch_and_optional_ppt_instructions():
    chinese, _ = parse_readme()
    english, _ = parse_readme("README.en.md")
    assert 'href="README.en.md">English' in chinese
    assert 'href="README.md">中文' in english
    assert "Installing ModelAtlas alone does not provide this capability" in english
    for term in ("Node.js", "PowerPoint / WPS", "overview-editable.pptx", "native editable objects",
                 "raster images", "docs/USAGE.md#editable-ppt"):
        assert term in english


def test_showcase_classification_matches_source_and_all_actual_generation_rounds():
    showcase = read_json(ROOT / "docs/examples/showcase.json")
    papers = {p["id"]: p for p in load_corpus()["papers"]}
    assets = read_json(ROOT / "docs/assets/reference-overviews/manifest.json")["assets"]
    indexed_images = set()
    for case in showcase["cases"]:
        paper = papers[case["paper_id"]]
        for key in ("year", "contest", "problem", "team"):
            assert case[key] == paper[key]
        assert case["source_award"] == {"O": "Outstanding Winner", "F": "Finalist"}[paper["award"]]
        reference = next(c for c in load_corpus()["cases"] if c["id"] == case["source_case_id"])
        assert reference["paper_id"] == case["paper_id"]
        if case["presentation"] == "comparison":
            original = next(a for a in assets if a["case_id"] == case["source_case_id"])
            assert original["paper_id"] == case["paper_id"]
            assert case["source_figure"] == "docs/assets/reference-overviews/" + original["file"]
        else:
            assert case["source_figure"] is None
        brief = read_json(ROOT / case["brief"])
        assert len(case["rounds"]) == len(brief["generation"]["chain"])
        assert case["latest_round"] == max(r["number"] for r in case["rounds"])
        for number, (round_, call) in enumerate(zip(case["rounds"], brief["generation"]["chain"]), 1):
            assert round_["number"] == number
            assert round_["operation"] == call["operation"]
            assert Path(round_["image"]).name == call["output"]
            assert Path(round_["prompt"]).name == call["prompt"]
            assert (ROOT / round_["image"]).is_file()
            assert (ROOT / round_["prompt"]).is_file()
            indexed_images.add(round_["image"])
        for notes in case["notes"].values():
            assert (ROOT / notes).is_file()
        assert (ROOT / case["full_prompt"]).is_file()
    published_images = {p.relative_to(ROOT).as_posix() for p in (ROOT / "docs/examples").rglob("*")
                        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}}
    assert indexed_images == published_images


def test_every_final_has_actual_generation_history_evidence_and_hashes():
    """These are integrity checks, not a substitute for scientific/visual review."""
    showcase = read_json(ROOT / "docs/examples/showcase.json")
    for case in showcase["cases"]:
        brief = read_json(ROOT / case["brief"])
        directory = (ROOT / case["brief"]).parent
        final = ROOT / case["final_image"]
        generation = brief["generation"]
        assert generation["backend"] == "built-in image_gen.imagegen"
        assert generation["status"] == "generated"
        assert digest(final) == generation["image_sha256"]
        assert generation["empirical_rerun"] is False
        assert generation["native_editability"] is False
        with Image.open(final) as image:
            assert list(image.size) == generation["actual_size"] == [1536, 1024]
            image.verify()
        full_prompt = (ROOT / case["full_prompt"]).read_text(encoding="utf-8")
        for call in generation["chain"]:
            assert (directory / call["prompt"]).read_text(encoding="utf-8").strip() in full_prompt
            if "sha256" in call:
                assert digest(directory / call["output"]) == call["sha256"]
        if "approval" in case:
            assert brief["review"]["status"] == case.get("review_status", "passed")
            if brief["review"]["status"] == "needs_revision":
                assert brief["review"]["issues"]
                assert brief["review"]["scientific_publication_gate"] == "needs_revision"
                assert brief["review"]["knowledge_base_admission"] is False
            assert brief["review"]["user_approval"] == "approved"
            assert brief["review"]["publication_gate"] == "approved_for_project_showcase"
            assert brief["review"]["approval_evidence"] == case["approval"]
            assert brief["review"]["physical_print_proof"] == "not performed"
            assert brief["review"]["independent_review"] == "not performed"
            assert brief["source"]["reread"]["physical_pages_visually_inspected"]
        else:
            assert case["paper_id"] == "icm-2025-e-2515324"
            assert brief["review"]["status"] == "pending"
            assert brief["review"]["user_approval"] == "not_recorded"
        assert brief["manuscript_evidence"] and brief["model_relationships"]
        audit = read_json(directory / "integrity-audit.json")
        assert audit["passed"] is True
        assert all(audit["files"].values())
        if "hashes" in audit:
            for name, checksum in audit["hashes"].items():
                path = directory / name
                assert digest(path) == checksum
        if "source" in brief:
            paper = next(p for p in load_corpus()["papers"] if p["id"] == case["paper_id"])
            assert brief["source"]["pdf_sha256"] == paper["sha256"]
            assert brief["source"]["full_manuscript_read"] is True
            assert brief["source"]["pdf_pages"] == paper["pdf_pages"]


def test_case_pages_display_only_final_images_and_have_working_local_links():
    for case in read_json(ROOT / "docs/examples/showcase.json")["cases"]:
        for notes in case["notes"].values():
            path = ROOT / notes
            text = path.read_text(encoding="utf-8")
            images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
            expected = 2 if case["presentation"] == "comparison" else 1
            assert len(images) == expected
            assert images.count("overview.png") == 1
            assert not any("overview-v" in target for target in images)
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                parts = urlsplit(target)
                if not parts.scheme and parts.path:
                    assert (path.parent / unquote(parts.path)).exists(), (notes, target)
