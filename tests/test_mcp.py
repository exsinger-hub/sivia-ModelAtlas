import asyncio
import json
import os
from pathlib import Path
import sys
from datetime import timedelta

import pytest

pytest.importorskip("mcp")
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.parametrize("entrypoint", ["runtime", "plugin"])
def test_real_stdio_discovery_search_render(tmp_path, entrypoint):
    async def scenario():
        project = Path(__file__).resolve().parents[1]
        arguments = (["-m", "modelatlas.server"] if entrypoint == "runtime" else
                     [str(project / "plugins/sivia-modelatlas/scripts/launch.py")])
        parameters=StdioServerParameters(command=sys.executable,args=arguments,env={**os.environ,"MODELATLAS_HOME":str(tmp_path/"db")})
        async with stdio_client(parameters) as (read,write):
            async with ClientSession(read,write,read_timeout_seconds=timedelta(seconds=20)) as session:
                await session.initialize()
                tool_list=await session.list_tools()
                assert len(tool_list.tools)==14
                styles=await session.call_tool("atlas_search_styles",{"problem":"E","role":"overview"})
                assert not styles.isError
                assert "e-model-inheritance-overview" in str(styles.content)
                assert "Outstanding Winner" in str(styles.content)
                draft=tmp_path/"synthetic-draft.md"
                draft.write_text("# TEST FIXTURE\nA synthetic model description, not a contest submission.",encoding="utf-8")
                prepared=await session.call_tool("atlas_prepare_draft",{"path":str(draft),"problem":"C"})
                assert not prepared.isError
                assert "awaiting_agent_design" in str(prepared.content)
                result=await session.call_tool("atlas_search_knowledge",{"query":"网球 动量"})
                assert not result.isError
                assert "mcm-c-match-flow" in str(result.content)
                path=Path(__file__).resolve().parents[1]/"examples/residual.json"
                result=await session.call_tool("atlas_render",{"spec_path":str(path),"output_dir":str(tmp_path/"runs")})
                assert not result.isError
                assert list((tmp_path/"runs").glob("*/figure.svg"))
                invalid=await session.call_tool("atlas_search_knowledge",{"query":"x","kind":"bad"})
                assert invalid.isError
    asyncio.run(asyncio.wait_for(scenario(),timeout=40))
