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
        assert brief["design_revision"]["status"] == "candidate_awaiting_user_feedback"
        assert brief["review"]["user_approval"] == "not_recorded"
        for call in brief["generation"]["chain"][2:]:
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
