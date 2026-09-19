"""Paper intake and actual overview/prompt pairing; the host agent performs design."""
from pathlib import Path
import shutil
from uuid import uuid4

from pypdf import PdfReader

from .common import digest, now, read_json, write_json
from .corpus import search_styles


def prepare_paper(path, workspace, problem=None, query=""):
    source = Path(path).resolve()
    source_hash = digest(source)
    suffix = source.suffix.lower()
    if suffix == ".pdf":
        pages = [(p.extract_text() or "") for p in PdfReader(source).pages]
        if not any(p.strip() for p in pages):
            raise ValueError("PDF has no extractable text; provide OCR text or a readable draft")
        text = "\n\n".join(f"## PDF page {i}\n\n{page}" for i, page in enumerate(pages, 1))
        empty_pages = [i for i, page in enumerate(pages, 1) if not page.strip()]
    elif suffix in (".md", ".txt", ".tex"):
        text = source.read_text(encoding="utf-8-sig")
        pages, empty_pages = [text], []
    else:
        raise ValueError("Paper must be PDF, Markdown, TXT or TeX; export DOCX to PDF first")
    if not text.strip():
        raise ValueError("Empty draft")
    styles = search_styles(query, problem, "overview", "award", 5)
    directory = Path(workspace).resolve() / "papers" / uuid4().hex
    directory.mkdir(parents=True, exist_ok=False)
    snapshot = directory / ("source" + suffix)
    shutil.copyfile(source, snapshot)
    if digest(snapshot) != source_hash:
        raise ValueError("Draft changed during intake; retry with a stable saved version")
    (directory / "manuscript.md").write_text(text, encoding="utf-8")
    write_json(directory / "style-candidates.json", styles)
    session = {"schema_version": 1, "created_at": now(), "directory": str(directory),
               "source_path": str(source), "source_snapshot": snapshot.name, "source_sha256": digest(snapshot),
               "text_path": str(directory / "manuscript.md"), "page_count": len(pages),
               "empty_text_pages": empty_pages, "problem": problem,
               "style_candidates_path": str(directory / "style-candidates.json"),
               "status": "awaiting_agent_design", "image_generated": False,
               "next_step": "Read the full paper; interpret model/evidence relationships; view relevant illustrations; follow paper2overview. This command does not design or generate an image."}
    write_json(directory / "session.json", session)
    return session


def pair_overview(session_dir, image_path, prompt_path, brief_path):
    """Archive an actual raster + full prompt + evidence brief, without claiming visual approval."""
    session_dir = Path(session_dir).resolve()
    session = read_json(session_dir / "session.json")
    snapshot = session_dir / Path(session["source_snapshot"]).name
    if digest(snapshot) != session["source_sha256"]:
        raise ValueError("Draft snapshot hash mismatch")
    image = Path(image_path).resolve()
    from PIL import Image
    with Image.open(image) as opened:
        size = opened.size
        if opened.format not in ("PNG", "JPEG", "WEBP"):
            raise ValueError("Overview must be an actual PNG, JPEG or WebP image")
        extension = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}[opened.format]
        opened.verify()
    prompt = Path(prompt_path).read_text(encoding="utf-8-sig")
    brief = read_json(brief_path)
    if len(prompt.strip()) < 100:
        raise ValueError("Full production prompt required, not a placeholder")
    for key in ("claim", "manuscript_evidence", "caption", "placement", "generation", "review"):
        if not brief.get(key):
            raise ValueError(f"Overview brief requires {key}")
    if not isinstance(brief["manuscript_evidence"], list):
        raise ValueError("Manuscript evidence must be a list")
    if not isinstance(brief["generation"], dict) or not brief["generation"].get("backend"):
        raise ValueError("Generation must record the actual backend")
    if not isinstance(brief["review"], dict):
        raise ValueError("Review must be a structured object")
    for entry in brief["manuscript_evidence"]:
        if not isinstance(entry, dict) or not entry.get("locator") or not entry.get("supports"):
            raise ValueError("Each manuscript evidence entry needs locator and supports")
    if not isinstance(brief.get("references"), list):
        raise ValueError("References must be a list")
    if not brief["references"] and not brief.get("reference_note"):
        raise ValueError("Empty references require an explicit reference_note")
    for reference in brief["references"]:
        if not isinstance(reference, dict) or not reference.get("case_id") or not reference.get("borrowed") or not reference.get("not_borrowed"):
            raise ValueError("References require case_id, borrowed and not_borrowed")
        if not any(c["id"] == reference["case_id"] for c in search_styles(collection="all", limit=100)):
            raise ValueError("Unknown style reference")
    if brief["review"].get("status") not in ("pending", "needs_revision", "passed"):
        raise ValueError("Review needs explicit pending/needs_revision/passed status")
    directory = session_dir / "overviews" / uuid4().hex
    directory.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(image, directory / ("overview" + extension))
    (directory / "prompt.md").write_text(prompt, encoding="utf-8")
    write_json(directory / "brief.json", brief)
    manifest = {"schema_version": 1, "created_at": now(), "directory": str(directory),
                "paper_sha256": session["source_sha256"], "image": "overview" + extension,
                "image_size": list(size), "status": "paired_artifact", "visual_review": brief["review"],
                "user_approval": "not_recorded", "semantic_fidelity": "host_review_required",
                "files": {p.name: digest(p) for p in directory.iterdir() if p.is_file()}}
    write_json(directory / "manifest.json", manifest)
    return manifest


def audit_overview(directory):
    """Check file integrity only. Do not upgrade a host review or claim scientific validity."""
    root = Path(directory).resolve()
    manifest = read_json(root / "manifest.json")
    required = {manifest["image"], "prompt.md", "brief.json"}
    checks = {}
    for name, expected in manifest.get("files", {}).items():
        if Path(name).name != name or name in (".", ".."):
            raise ValueError("Bundle manifest may only name local files")
        file = root / name
        checks[name] = file.is_file() and digest(file) == expected
    return {"passed": required <= set(checks) and all(checks.values()), "files": checks,
            "visual_review": manifest.get("visual_review"), "user_approval": manifest.get("user_approval"),
            "scope": "File integrity only; not source fidelity, image quality or award verification."}
