import asyncio
from datetime import timedelta
import json
import os
from pathlib import Path
import sys

from PIL import Image
import pytest

pytest.importorskip("mcp")
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from modelatlas.common import write_json


def payload(result):
    assert not result.isError, result.content
    data = result.structuredContent
    if data is None:
        data = json.loads(next(block.text for block in result.content if block.type == "text"))
    # FastMCP wraps generic list outputs in the declared {result: ...} schema.
    return data["result"] if isinstance(data, dict) and set(data) == {"result"} else data


@pytest.mark.parametrize("entrypoint", ["runtime", "plugin"])
def test_real_stdio_paper_overview_contract(tmp_path, entrypoint):
    async def scenario():
        project = Path(__file__).resolve().parents[1]
        arguments = (["-m", "modelatlas.server"] if entrypoint == "runtime" else
                     [str(project / "plugins/sivia-modelatlas/scripts/launch.py")])
        parameters = StdioServerParameters(command=sys.executable, args=arguments,
                                           env={**os.environ, "MODELATLAS_HOME": str(tmp_path / "workspace")})
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write, read_timeout_seconds=timedelta(seconds=20)) as session:
                await session.initialize()
                tool_list = await session.list_tools()
                assert {t.name for t in tool_list.tools} == {
                    "atlas_prepare_paper", "atlas_search_styles", "atlas_style_coverage",
                    "atlas_fetch_reference", "atlas_find_papers", "atlas_pair_overview", "atlas_audit_overview"}
                styles = payload(await session.call_tool("atlas_search_styles", {"problem": "E"}))
                assert "e-model-inheritance-overview" in {c["id"] for c in styles}
                assert all(c["role"] == "overview" for c in styles)
                stats = payload(await session.call_tool("atlas_style_coverage", {}))
                assert stats["cases"] == 20

                paper = tmp_path / "synthetic-paper.md"
                paper.write_text("# TEST FIXTURE\nA synthetic model A feeds B; not a real contest paper.", encoding="utf-8")
                prepared = payload(await session.call_tool("atlas_prepare_paper", {"path": str(paper), "problem": "C"}))
                assert prepared["status"] == "awaiting_agent_design"
                assert prepared["image_generated"] is False
                assert Path(prepared["text_path"]).is_file()

                # A raster fixture exercises actual transport/pairing; it is not an ImageGen test.
                image = tmp_path / "fixture.png"
                Image.new("RGB", (20, 20), "white").save(image)
                prompt = tmp_path / "prompt.md"
                prompt.write_text("Synthetic pairing test only, not a paper figure. " * 5, encoding="utf-8")
                brief = tmp_path / "brief.json"
                write_json(brief, {
                    "claim": "Packaging test only", "manuscript_evidence": [
                        {"locator": "Fixture line 2", "supports": "A feeds B"}],
                    "references": [], "reference_note": "No scientific drawing performed in this transport test",
                    "caption": "Synthetic fixture", "placement": "Not for publication",
                    "generation": {"backend": "test fixture"},
                    "review": {"status": "pending"}})
                paired = payload(await session.call_tool("atlas_pair_overview", {
                    "session_dir": prepared["directory"], "image_path": str(image),
                    "prompt_path": str(prompt), "brief_path": str(brief)}))
                audit = payload(await session.call_tool("atlas_audit_overview", {"directory": paired["directory"]}))
                assert audit["passed"] and audit["visual_review"]["status"] == "pending"
                assert not list((tmp_path / "workspace").glob("*.sqlite*"))
                invalid = await session.call_tool("atlas_search_styles", {"problem": "G"})
                assert invalid.isError
    asyncio.run(asyncio.wait_for(scenario(), timeout=40))
