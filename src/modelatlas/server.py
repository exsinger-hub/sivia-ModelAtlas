"""Focused paper-to-overview MCP transport; no plotting or legacy card services."""
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .corpus import coverage, fetch_reference, search_styles
from .papers import audit_overview, pair_overview, prepare_paper

server = FastMCP("SIVIA ModelAtlas · Paper to Overview", log_level="WARNING")


def workspace():
    return Path(os.environ.get("MODELATLAS_HOME", str(Path.home() / ".modelatlas"))).resolve()


@server.tool()
def atlas_prepare_paper(path: str, problem: str | None = None, query: str = "") -> dict:
    """Prepare PDF/MD/TXT/TeX for paper2overview. Read the returned manuscript, design, then use host ImageGen. Intake itself does not generate an image."""
    return prepare_paper(path, workspace(), problem, query)


@server.tool()
def atlas_search_styles(query: str = "", problem: str | None = None, role: str = "overview",
                        collection: str = "award", limit: int = 5) -> list[dict]:
    """Search preserved illustration references. Default overview + verified O/F core; role=all includes supporting visual references, collection=research selects extensions."""
    return search_styles(query, problem, None if role == "all" else role, collection, limit)


@server.tool()
def atlas_style_coverage() -> dict:
    """Report actual illustration knowledge-base coverage; categories do not imply new drawing capabilities."""
    return coverage()


@server.tool()
def atlas_fetch_reference(case_id: str, render_page: bool = True) -> dict:
    """Fetch a hash-pinned reference paper and render its precise page locally. Open the image to inspect it; this is not a generated overview."""
    return fetch_reference(case_id, workspace(), render_page=render_page)


@server.tool()
def atlas_find_papers(query: str, limit: int = 5, mode: str = "academic") -> list[dict]:
    """Find papers with AnySearch academic/web modes. Returns discovery metadata without auto-curation or persistent legacy cards."""
    from .search import AnySearch
    return AnySearch().search(query, limit, mode)


@server.tool()
def atlas_pair_overview(session_dir: str, image_path: str, prompt_path: str, brief_path: str) -> dict:
    """Archive actual overview + full prompt + paper evidence/review. Does not generate, approve or insert an image into a paper."""
    return pair_overview(session_dir, image_path, prompt_path, brief_path)


@server.tool()
def atlas_audit_overview(directory: str) -> dict:
    """Check overview bundle integrity; source fidelity, visual review and user approval remain separate."""
    return audit_overview(directory)


def main():
    server.run(transport="stdio")


if __name__ == "__main__":
    main()
