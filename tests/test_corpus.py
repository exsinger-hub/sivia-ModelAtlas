import copy
import hashlib
import io
import json
from pathlib import Path
from unittest.mock import MagicMock, Mock

from PIL import Image, UnidentifiedImageError
from pypdf import PdfWriter
import pytest

from modelatlas.common import digest, read_json, write_json
from modelatlas.corpus import coverage, fetch_reference, load_corpus, search_styles, validate_corpus
from modelatlas.drafts import audit_overview, pair_overview, prepare_draft
from modelatlas.search import AnySearch


def test_core_coverage_and_award_proof():
    corpus = load_corpus()
    stats = coverage()
    assert stats["award_papers"] == 8
    assert stats["research_papers"] == 1
    assert stats["award_cases"] == 18
    assert stats["research_cases"] == 2
    assert all(c["award_papers"] >= 1 for c in stats["categories"])
    assert sum(c["own_problem_cases"] for c in stats["categories"]) == 18
    assert all(p["award_evidence"]["checked_at"] for p in corpus["papers"] if p["collection"] == "award")


@pytest.mark.parametrize("mutation,match", [
    (lambda d: d["papers"][0].pop("award_evidence"), "official"),
    (lambda d: d["papers"][-1].update(award="O"), "Research"),
    (lambda d: d["cases"][0].update(pdf_page=999), "page"),
    (lambda d: d["papers"][0].update(sha256="wrong"), "SHA"),
    (lambda d: d["cases"][0]["visual_review"].update(status="not_viewed"), "visually"),
    (lambda d: d["cases"][0].update(paper_id="unknown"), "Unknown"),
])
def test_corpus_rejects_false_provenance(mutation, match):
    data = copy.deepcopy(load_corpus())
    mutation(data)
    with pytest.raises(ValueError, match=match):
        validate_corpus(data)


def test_style_filters_preserve_original_problem_and_research_status():
    core = search_styles(limit=100)
    assert len(core) == 18 and all(c["paper"]["collection"] == "award" for c in core)
    extension = search_styles("SHAP", "F", collection="research")
    assert len(extension) == 1
    assert extension[0]["paper"]["award"] is None
    assert extension[0]["paper"]["problem"] is None
    ecological = search_styles("循环", "A", "mechanism")
    assert "e-nitrogen-cycle" in {c["id"] for c in ecological}
    assert next(c for c in ecological if c["id"] == "e-nitrogen-cycle")["paper"]["problem"] == "E"
    assert search_styles("zzzznomatch") == []
    assert all(c["paper"]["award"] == "O" for c in core if c["paper"]["problem"] == "F")


@pytest.mark.parametrize("options", [{"problem":"G"},{"collection":"winner"},{"role":"solution"},{"limit":0}])
def test_bad_retrieval_filters(options):
    with pytest.raises(ValueError):
        search_styles(**options)


def reference_fixture(monkeypatch):
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    output = io.BytesIO()
    writer.write(output)
    payload = output.getvalue()
    corpus = copy.deepcopy(load_corpus())
    paper = corpus["papers"][0]
    paper.update(sha256=hashlib.sha256(payload).hexdigest(), pdf_pages=1)
    corpus["cases"][0]["pdf_page"] = 1
    monkeypatch.setattr("modelatlas.corpus.load_corpus", lambda: corpus)
    response = MagicMock()
    response.__enter__.return_value = response
    response.iter_content.return_value = [payload]
    session = Mock()
    session.get.return_value = response
    return payload, session, response, paper


def test_pinned_reference_cache_and_tamper(tmp_path, monkeypatch):
    _, session, _, _ = reference_fixture(monkeypatch)
    result = fetch_reference("a-model-task-map", tmp_path, session, render_page=False)
    assert result["status"] == "source_verified"
    assert result["current_agent_visual_review"] == "not_performed"
    assert fetch_reference("a-model-task-map", tmp_path, session, render_page=False)["page_image"] is None
    assert session.get.call_count == 1
    Path(result["pdf_path"]).write_bytes(b"tampered test fixture")
    with pytest.raises(ValueError, match="Cached reference SHA"):
        fetch_reference("a-model-task-map", tmp_path, session, render_page=False)


def test_changed_source_not_promoted_to_cache(tmp_path, monkeypatch):
    _, session, response, _ = reference_fixture(monkeypatch)
    response.iter_content.return_value = [b"wrong source or HTML error"]
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        fetch_reference("a-model-task-map", tmp_path, session, render_page=False)
    assert not list(tmp_path.rglob("*.pdf"))
    assert not list(tmp_path.rglob("*.part"))


def test_missing_poppler_reports_cached_pdf(tmp_path, monkeypatch):
    _, session, _, _ = reference_fixture(monkeypatch)
    monkeypatch.setattr("modelatlas.corpus.shutil.which", lambda _: None)
    with pytest.raises(RuntimeError, match="pdftoppm required"):
        fetch_reference("a-model-task-map", tmp_path, session)
    assert len(list(tmp_path.rglob("*.pdf"))) == 1


def test_draft_intake_does_not_generate_or_modify_original(tmp_path):
    path = tmp_path / "synthetic.md"
    path.write_text("# Synthetic test only\nA model with one stated dependency.", encoding="utf-8")
    before = digest(path)
    result = prepare_draft(path, tmp_path / "local", "C")
    assert result["status"] == "awaiting_agent_design"
    assert result["image_generated"] is False
    assert digest(path) == before == result["source_sha256"]
    assert Path(result["text_path"]).read_text(encoding="utf-8") == path.read_text(encoding="utf-8")
    assert read_json(result["style_candidates_path"])
    second = prepare_draft(path, tmp_path / "local", "C")
    assert result["directory"] != second["directory"]


def test_blank_pdf_is_not_a_read_draft(tmp_path):
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    path = tmp_path / "scanned.pdf"
    writer.write(path)
    with pytest.raises(ValueError, match="OCR"):
        prepare_draft(path, tmp_path / "local")


def pairing_fixture(tmp_path):
    draft = tmp_path / "fixture.md"
    draft.write_text("# Synthetic test fixture\nA feeds B.", encoding="utf-8")
    session = prepare_draft(draft, tmp_path / "local", "C")
    # A tiny synthetic raster tests packaging, not overview quality or generation.
    raster = tmp_path / "fixture.png"
    Image.new("RGB", (20, 20), "white").save(raster)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Synthetic packaging test prompt; this is not a generated paper figure. " * 4, encoding="utf-8")
    brief = tmp_path / "brief.json"
    write_json(brief, {"claim":"TEST ONLY", "manuscript_evidence":[{"locator":"fixture line 2","supports":"A feeds B"}],
                      "references":[{"case_id":"c-infer-compare-redesign","borrowed":"branch structure for test","not_borrowed":"all science"}],
                      "caption":"Synthetic fixture", "placement":"Not for publication",
                      "generation":{"backend":"test fixture, not ImageGen","status":"fixture"},
                      "review":{"status":"pending","checks":[],"issues":[]}})
    return session, raster, prompt, brief


def test_real_image_prompt_pair_and_tamper_detection(tmp_path):
    session, raster, prompt, brief = pairing_fixture(tmp_path)
    pair = pair_overview(session["directory"], raster, prompt, brief)
    assert pair["status"] == "paired_artifact"
    assert pair["visual_review"]["status"] == "pending"
    assert pair["user_approval"] == "not_recorded"
    root = Path(pair["directory"])
    assert (root / "prompt.md").read_text(encoding="utf-8") == prompt.read_text(encoding="utf-8")
    assert audit_overview(root)["passed"]
    (root / "prompt.md").write_text("tampered", encoding="utf-8")
    assert not audit_overview(root)["passed"]


def test_pair_requires_actual_image_full_prompt_and_evidence(tmp_path):
    session, raster, prompt, brief = pairing_fixture(tmp_path)
    prompt.write_text("draw a diagram", encoding="utf-8")
    with pytest.raises(ValueError, match="Full production prompt"):
        pair_overview(session["directory"], raster, prompt, brief)
    prompt.write_text("test full prompt " * 30, encoding="utf-8")
    data = read_json(brief)
    data["manuscript_evidence"] = []
    write_json(brief, data)
    with pytest.raises(ValueError, match="manuscript_evidence"):
        pair_overview(session["directory"], raster, prompt, brief)
    with pytest.raises(UnidentifiedImageError):
        pair_overview(session["directory"], prompt, prompt, brief)


def test_pair_rejects_changed_draft_snapshot(tmp_path):
    session, raster, prompt, brief = pairing_fixture(tmp_path)
    (Path(session["directory"]) / session["source_snapshot"]).write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="snapshot hash"):
        pair_overview(session["directory"], raster, prompt, brief)


def test_anysearch_web_mode_no_fabricated_vertical_tag():
    session = Mock()
    discovery, results = Mock(), Mock()
    discovery.json.return_value = {"code":0,"data":{"domains":[]}}
    results.json.return_value = {"code":0,"data":{"results":[{"url":"https://contest.comap.com/example","title":"Official record"}]}}
    session.request.side_effect = [discovery, results]
    records = AnySearch(session).search("team ID official results", mode="web")
    assert "tag" not in session.request.call_args_list[1].kwargs["json"]
    assert records[0]["status"] == "discovered"
    assert records[0]["search_mode"] == "web"
    assert "award" not in records[0]


def test_plugin_primary_entry_and_version():
    root = Path(__file__).resolve().parents[1]
    plugin = root / "plugins/sivia-modelatlas"
    assert read_json(plugin / ".codex-plugin/plugin.json")["version"] == "0.2.0"
    skill = (plugin / "skills/draft2overview/SKILL.md").read_text(encoding="utf-8")
    assert "ImageGen-first" in skill and "atlas_fetch_reference" in skill
    assert len(list((plugin / "skills").glob("*/SKILL.md"))) == 5
