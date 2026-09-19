"""Regression checks for the focused product and preserved illustration library."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

from modelatlas.cli import build_parser
from modelatlas.common import read_json


ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("command", ["render", "gallery", "audit", "search", "add-card", "ingest", "evidence", "init", "draft2overview"])
def test_removed_cli_commands_are_not_advertised_or_executed(command):
    with pytest.raises(SystemExit) as error:
        build_parser().parse_args([command])
    assert error.value.code == 2


def test_overview_default_and_explicit_preserved_reference_roles():
    assert build_parser().parse_args(["styles"]).role == "overview"
    assert build_parser().parse_args(["styles", "--role", "all"]).role == "all"
    assert build_parser().parse_args(["paper2overview", "paper.pdf"]).path == "paper.pdf"


def test_real_cli_intake_preserves_existing_user_database(tmp_path):
    workspace = tmp_path / "local"
    workspace.mkdir()
    legacy = workspace / "library.sqlite3"
    legacy.write_bytes(b"Existing user data must remain untouched")
    paper = tmp_path / "test.md"
    paper.write_text("# Synthetic input\nModel A supplies B.", encoding="utf-8")
    result = subprocess.run([sys.executable, "-m", "modelatlas", "--workspace", str(workspace),
                             "paper2overview", str(paper), "--problem", "C"],
                            capture_output=True, text=True, encoding="utf-8", check=True)
    session = json.loads(result.stdout)
    assert session["status"] == "awaiting_agent_design" and session["image_generated"] is False
    assert Path(session["directory"]).parent == workspace / "papers"
    assert legacy.read_bytes() == b"Existing user data must remain untouched"
    assert all(c["role"] == "overview" for c in read_json(session["style_candidates_path"]))


def test_removed_backends_and_dependency_stack():
    for module in ("figures", "gallery", "library", "drafts"):
        assert importlib.util.find_spec("modelatlas." + module) is None
    config = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "numpy" not in config and "matplotlib" not in config
    result = subprocess.run([sys.executable, "-c",
                             "import sys; import modelatlas.server; assert 'numpy' not in sys.modules; assert 'matplotlib' not in sys.modules"],
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_readme_keeps_knowledge_links_and_link_targets_exist():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for path in ("knowledge-base/CATALOG.md", "knowledge-base/README.md", "src/modelatlas/knowledge/corpus.json",
                 "plugins/sivia-modelatlas/skills/paper2overview/references/production-contract.md"):
        assert path in readme and (ROOT / path).is_file()
    assert "scripts/demo.py" not in readme
