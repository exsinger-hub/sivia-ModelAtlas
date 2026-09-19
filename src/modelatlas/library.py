"""SQLite library: source records, page-bound evidence, figure cards and versions."""
from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path
from importlib.resources import files

from .common import digest, now


def tokens(text):
    words = re.findall(r"[a-z0-9]+|[\u4e00-\u9fff]", text.lower())
    return set(words)


class Library:
    def __init__(self, workspace):
        self.root = Path(workspace).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "library.sqlite3"
        with self.connect() as db:
            db.executescript("""
            CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY, record TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS cards(id TEXT PRIMARY KEY, record TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS pages(source_id TEXT, page INTEGER, text TEXT,
              PRIMARY KEY(source_id, page));
            CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY, record TEXT NOT NULL);
            """)

    def connect(self):
        return sqlite3.connect(self.path)

    def seed(self):
        for kind in ("sources", "cards"):
            entries = json.loads(files("modelatlas").joinpath(f"knowledge/{kind}.json").read_text(encoding="utf-8"))
            with self.connect() as db:
                for item in entries:
                    db.execute(f"INSERT OR IGNORE INTO {kind} VALUES (?, ?)", (item["id"], json.dumps(item, ensure_ascii=False)))
        return self.stats()

    def stats(self):
        with self.connect() as db:
            return {kind: db.execute(f"SELECT COUNT(*) FROM {kind}").fetchone()[0]
                    for kind in ("sources", "cards", "pages", "runs")}

    def all(self, kind):
        if kind not in {"sources", "cards", "runs"}:
            raise ValueError("Unknown collection")
        with self.connect() as db:
            return [json.loads(row[0]) for row in db.execute(f"SELECT record FROM {kind} ORDER BY id")]

    def put_source(self, record):
        if not record.get("id") or not record.get("title") or not record.get("url"):
            raise ValueError("Source needs id, title and url (local imports use file URI)")
        with self.connect() as db:
            db.execute("INSERT INTO sources VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET record=excluded.record",
                       (record["id"], json.dumps(record, ensure_ascii=False)))
        return record

    def add_card(self, card):
        required = ("id", "title", "claim", "figure_kind", "source_ids", "locator", "tags", "guidance")
        if any(not card.get(field) for field in required):
            raise ValueError("Card requires " + ", ".join(required))
        known = {s["id"] for s in self.all("sources")}
        if not set(card["source_ids"]) <= known:
            raise ValueError("Unknown source_id in card")
        card = {**card, "status": "curated", "updated_at": now()}
        with self.connect() as db:
            db.execute("INSERT INTO cards VALUES (?, ?)", (card["id"], json.dumps(card, ensure_ascii=False)))
        return card

    def search(self, query, kind="cards", limit=8):
        if not query.strip() or not 1 <= limit <= 100:
            raise ValueError("Nonempty query and limit 1..100 required")
        query_tokens = tokens(query)
        results = []
        for record in self.all(kind):
            text = json.dumps(record, ensure_ascii=False).lower()
            overlap = query_tokens & tokens(text)
            score = len(overlap) / max(len(query_tokens), 1)
            if query.lower() in text:
                score += 1
            if overlap:
                results.append({**record, "score": round(score, 4)})
        return sorted(results, key=lambda r: (-r["score"], r["id"]))[:limit]

    def ingest(self, path, title=None, url=None):
        path = Path(path).resolve()
        if path.suffix.lower() not in {".pdf", ".txt", ".md"}:
            raise ValueError("Supported paper formats: PDF, TXT, Markdown")
        sha = digest(path)
        source_id = "paper-" + sha[:16]
        if path.suffix.lower() == ".pdf":
            from pypdf import PdfReader
            texts = [page.extract_text() or "" for page in PdfReader(path).pages]
        else:
            texts = [path.read_text(encoding="utf-8-sig")]
        if not any(t.strip() for t in texts):
            raise ValueError("No text found; scanned PDFs need OCR before import")
        record = {"id": source_id, "title": title or path.stem, "url": url or path.as_uri(),
                  "status": "text_imported", "sha256": sha, "pages": len(texts), "imported_at": now(),
                  "note": "Extracted text; semantic review and figure-card curation still required."}
        with self.connect() as db:
            db.execute("INSERT INTO sources VALUES (?, ?) ON CONFLICT(id) DO UPDATE SET record=excluded.record",
                       (source_id, json.dumps(record, ensure_ascii=False)))
            db.executemany("INSERT OR REPLACE INTO pages VALUES (?, ?, ?)",
                           [(source_id, i + 1, text) for i, text in enumerate(texts)])
        return record

    def evidence(self, source_id, query="", limit=5):
        with self.connect() as db:
            pages = db.execute("SELECT page, text FROM pages WHERE source_id=? ORDER BY page", (source_id,)).fetchall()
        result = []
        for page, text in pages:
            pos = text.lower().find(query.lower()) if query else 0
            if pos >= 0:
                result.append({"source_id": source_id, "page": page, "text": text[max(0,pos-120):pos+1400]})
        return result[:limit]

    def record_run(self, record):
        with self.connect() as db:
            db.execute("INSERT INTO runs VALUES (?, ?)", (record["id"], json.dumps(record, ensure_ascii=False)))
