"""Length checks validate exact input only, never scientific/visual acceptance."""
import hashlib
import json
from pathlib import Path

import pytest

from modelatlas.prompting import check_prompt, count_detail


ROOT = Path(__file__).resolve().parents[1]


def test_count_uses_unicode_code_points_without_whitespace():
    assert count_detail(" A\t中\r\n😀\u3000B ") == 4
    assert count_detail("\n\r\t ") == 0


def test_frozen_floor_and_backend_ceiling_are_both_enforced():
    assert not check_prompt("x" * 15355)["passed"]
    assert check_prompt("x" * 15356)["passed"]
    report = check_prompt("x" * 15356 + " " * 16645)
    assert report["length_pass"] and not report["tool_limit_pass"]
    assert not report["passed"]
    assert "visual review" in report["scope"]
    assert not report["template_bytes_verified"]


def test_binding_cannot_silently_change_or_shorten():
    with pytest.raises(ValueError, match="Template hash"):
        check_prompt("x" * 16000, template_bytes=b"shortened template")
    with pytest.raises(ValueError, match="Unknown prompt profile"):
        check_prompt("example", profile="invented-short-profile")


def test_new_call_records_check_each_exact_prompt_not_aggregate_history():
    checked = 0
    for directory in ("2026-c-ballroom-voting", "2026-d-wins-to-worth", "2025-f-cyber-policy"):
        root = ROOT / "docs/examples" / directory
        brief = json.loads((root / "brief.json").read_text(encoding="utf-8"))
        assert brief["design_revision"]["status"] == "user_approved_showcase"
        assert brief["review"]["user_approval"] == "approved"
        for call in brief["generation"]["chain"][2:5]:
            assert call["status"] == "superseded_history"
            raw = (root / call["prompt"]).read_bytes()
            text = raw.decode("utf-8-sig")
            actual = check_prompt(text)
            recorded = call["prompt_detail"]
            for field in ("total_characters", "non_whitespace_characters", "submitted_utf8_sha256",
                          "profile", "binding", "length_pass", "tool_limit_pass", "passed"):
                assert actual[field] == recorded[field]
            assert actual["passed"]
            assert recorded["template_bytes_verified"]  # Actual execution verified installed template.
            assert actual["submitted_utf8_sha256"] == hashlib.sha256(text.encode("utf-8")).hexdigest()
            checked += 1
    assert checked == 9


def test_approved_redraws_keep_exact_full_prompts_and_scoped_corrections():
    showcase = json.loads((ROOT / "docs/examples/showcase.json").read_text(encoding="utf-8"))
    designs = corrections = 0
    for case in showcase["cases"]:
        if "approval" not in case:
            continue
        root = (ROOT / case["brief"]).parent
        brief = json.loads((root / "brief.json").read_text(encoding="utf-8"))
        assert case["approval"] == brief["review"]["approval_evidence"]
        for call in brief["generation"]["chain"]:
            if call.get("series") != "pdf-reread-20260920":
                continue
            raw = (root / call["prompt"]).read_bytes()
            if call["prompt_scope"] == "full_redesign":
                report = check_prompt(raw.decode("utf-8"))
                assert report["passed"]
                assert call["prompt_detail"]["template_bytes_verified"]
                for field in ("total_characters", "non_whitespace_characters", "submitted_utf8_sha256", "binding"):
                    assert report[field] == call["prompt_detail"][field]
                designs += 1
            else:
                assert call["operation"] == "edit"
                assert call["prompt_scope"] == "localized_correction"
                assert hashlib.sha256(raw).hexdigest() == call["prompt_sha256"]
                assert raw.strip()
                corrections += 1
    assert (designs, corrections) == (5, 8)
