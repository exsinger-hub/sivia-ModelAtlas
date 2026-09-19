"""Versioned, visually reviewed references; separate from uncurated search records."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from importlib.resources import files
from pathlib import Path
from urllib.parse import urlparse

import requests
from pypdf import PdfReader

from .common import digest, write_json

ROLES = ("overview", "mechanism", "algorithm", "data_plot", "explanation")
COLLECTIONS = ("award", "research", "all")


def validate_corpus(data):
    """Reject untraceable award claims and figure/version ambiguity at load time."""
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported corpus schema")
    if {c["problem"] for c in data["categories"]} != set("ABCDEF"):
        raise ValueError("A–F categories required")
    papers = {}
    for paper in data["papers"]:
        key = paper["id"]
        if not re.fullmatch(r"[a-z0-9-]+", key) or key in papers:
            raise ValueError("Invalid or duplicate paper ID")
        if not re.fullmatch(r"[a-f0-9]{64}", paper["sha256"]):
            raise ValueError("Paper SHA-256 required")
        if not paper["pdf_url"].startswith("https://") or paper["pdf_pages"] < 1:
            raise ValueError("Pinned HTTPS PDF and page count required")
        if paper["collection"] == "award":
            proof = paper.get("award_evidence", {})
            if (paper.get("award") not in ("O", "F") or paper.get("problem") not in tuple("ABCDEF")
                    or not paper.get("team") or not proof.get("locator")
                    or urlparse(proof.get("url", "")).hostname not in ("www.contest.comap.com", "contest.comap.com")):
                raise ValueError("Award paper requires official COMAP team/problem/award evidence")
        elif paper["collection"] == "research":
            if paper.get("award") is not None or paper.get("award_evidence"):
                raise ValueError("Research extension must not assert a competition award")
        else:
            raise ValueError("Unknown paper collection")
        papers[key] = paper
    seen = set()
    for case in data["cases"]:
        if case["id"] in seen or not re.fullmatch(r"[a-z0-9-]+", case["id"]):
            raise ValueError("Invalid or duplicate case ID")
        seen.add(case["id"])
        if case["paper_id"] not in papers:
            raise ValueError("Unknown case paper")
        if not 1 <= case["pdf_page"] <= papers[case["paper_id"]]["pdf_pages"]:
            raise ValueError("Figure page outside pinned PDF")
        if case["role"] not in ROLES or not case["problem_targets"] or not set(case["problem_targets"]) <= set("ABCDEF"):
            raise ValueError("Invalid figure role or problem targets")
        for field in ("figure", "composition", "transfer", "do_not_transfer", "limitations"):
            if not case.get(field):
                raise ValueError(f"Figure case requires {field}")
        if case.get("visual_review", {}).get("status") != "reviewed":
            raise ValueError("Style corpus only accepts visually reviewed cases")
    return data


def load_corpus():
    return validate_corpus(json.loads(files("modelatlas").joinpath("knowledge/corpus.json").read_text(encoding="utf-8")))


def search_styles(query="", problem=None, role=None, collection="award", limit=5, year=None):
    """Transparent term matching after hard filters; does not invent semantic relevance."""
    if collection not in COLLECTIONS or role is not None and role not in ROLES:
        raise ValueError("Invalid collection or figure role")
    if problem is not None and problem not in tuple("ABCDEF"):
        raise ValueError("Problem must be one of A–F")
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be 1..100")
    if year is not None and (type(year) is not int or not 1900 <= year <= 2100):
        raise ValueError("Year must be an integer between 1900 and 2100")
    data = load_corpus()
    papers = {p["id"]: p for p in data["papers"]}
    terms = set(re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", query.lower()))
    result = []
    for case in data["cases"]:
        paper = papers[case["paper_id"]]
        if collection != "all" and paper["collection"] != collection:
            continue
        if year is not None and paper["year"] != year:
            continue
        if problem and problem not in case["problem_targets"] or role and role != case["role"]:
            continue
        searchable = json.dumps({k: case[k] for k in ("title", "tags", "composition", "transfer")}, ensure_ascii=False).lower()
        matched = sorted(term for term in terms if term in searchable)
        if terms and not matched:
            continue
        result.append({**case, "paper": paper, "matched_terms": matched, "score": len(matched)})
    # At equal text relevance, prefer the original contest category, then recent years.
    # Transfer targets remain eligible but do not displace own-category references by ID.
    return sorted(result, key=lambda c: (-c["score"],
                  bool(problem and c["paper"].get("problem") != problem),
                  -c["paper"]["year"], c["id"]))[:limit]


def coverage():
    data = load_corpus()
    papers = {p["id"]: p for p in data["papers"]}
    categories = []
    for category in data["categories"]:
        problem = category["problem"]
        own = [p for p in papers.values() if p["collection"] == "award" and p["problem"] == problem]
        categories.append({**category, "award_papers": len(own),
                           "O": sum(p["award"] == "O" for p in own),
                           "F": sum(p["award"] == "F" for p in own),
                           "own_problem_cases": sum(papers[c["paper_id"]].get("problem") == problem for c in data["cases"]),
                           "transferable_cases": sum(problem in c["problem_targets"] for c in data["cases"])})
    years = []
    for year in sorted({p["year"] for p in papers.values() if p["collection"] == "award"}, reverse=True):
        own = [p for p in papers.values() if p["collection"] == "award" and p["year"] == year]
        ids = {p["id"] for p in own}
        years.append({"year": year, "award_papers": len(own),
                      "award_cases": sum(c["paper_id"] in ids for c in data["cases"]),
                      "problems": {problem: sum(p["problem"] == problem for p in own) for problem in "ABCDEF"}})
    return {"categories": categories, "years": years, "papers": len(papers), "cases": len(data["cases"]),
            "award_papers": sum(p["collection"] == "award" for p in papers.values()),
            "research_papers": sum(p["collection"] == "research" for p in papers.values()),
            "award_cases": sum(papers[c["paper_id"]]["collection"] == "award" for c in data["cases"]),
            "research_cases": sum(papers[c["paper_id"]]["collection"] == "research" for c in data["cases"]),
            "note": data["taxonomy_note"]}


def fetch_reference(case_id, workspace, session=None, render_page=True):
    """Fetch one pinned PDF, verify bytes and page count, render the precise page locally.

    Public access does not grant permission to redistribute. Nothing is uploaded.
    A source changing at the same URL fails closed rather than silently replacing evidence.
    """
    data = load_corpus()
    case = next((c for c in data["cases"] if c["id"] == case_id), None)
    if case is None:
        raise ValueError("Unknown figure case ID")
    paper = next(p for p in data["papers"] if p["id"] == case["paper_id"])
    directory = Path(workspace).resolve() / "references" / paper["id"]
    directory.mkdir(parents=True, exist_ok=True)
    pdf = directory / (paper["sha256"] + ".pdf")
    if not pdf.exists():
        temp = None
        try:
            client = session or requests
            with client.get(paper["pdf_url"], timeout=(10, 45), stream=True) as response:
                response.raise_for_status()
                hasher = hashlib.sha256()
                total = 0
                with tempfile.NamedTemporaryFile(dir=directory, suffix=".part", delete=False) as output:
                    temp = Path(output.name)
                    for chunk in response.iter_content(64 * 1024):
                        total += len(chunk)
                        if total > 40 * 1024 * 1024:
                            raise ValueError("Reference exceeds 40 MiB limit")
                        output.write(chunk)
                        hasher.update(chunk)
                if hasher.hexdigest() != paper["sha256"]:
                    raise ValueError("Reference SHA-256 mismatch; source version changed, review required")
                # 'xb' prevents accidentally overwriting an existing validated reference.
                with pdf.open("xb") as destination, temp.open("rb") as source:
                    shutil.copyfileobj(source, destination)
        except requests.RequestException as error:
            raise RuntimeError(f"Reference download failed ({type(error).__name__})") from None
        finally:
            if temp is not None:
                temp.unlink(missing_ok=True)
    if digest(pdf) != paper["sha256"]:
        raise ValueError("Cached reference SHA-256 mismatch; preserve it for inspection")
    reader = PdfReader(pdf)
    if len(reader.pages) != paper["pdf_pages"]:
        raise ValueError("Reference PDF page count mismatch")
    result = {"case": case, "paper": paper, "pdf_path": str(pdf), "page_image": None,
              "page_text": reader.pages[case["pdf_page"] - 1].extract_text() or "",
              "status": "source_verified", "current_agent_visual_review": "not_performed"}
    if render_page:
        poppler = shutil.which("pdftoppm")
        if not poppler:
            raise RuntimeError(f"pdftoppm required to render reference; verified PDF cached at {pdf}")
        prefix = directory / f"page-{case['pdf_page']}"
        try:
            subprocess.run([poppler, "-f", str(case["pdf_page"]), "-l", str(case["pdf_page"]),
                            "-scale-to", "1800", "-singlefile", "-png", str(pdf), str(prefix)],
                           check=True, capture_output=True, timeout=60)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            raise RuntimeError("Reference page rendering failed; verified PDF retained") from None
        png = prefix.with_suffix(".png")
        if not png.is_file():
            raise RuntimeError("Renderer returned without a page image")
        result.update(page_image=str(png), page_image_sha256=digest(png), status="page_rendered_not_reviewed")
    write_json(directory / f"{case_id}.json", result)
    return result
