"""Paper-to-overview CLI; image generation belongs to the host agent."""
import argparse
import json
import os
import sys
from pathlib import Path

from .corpus import COLLECTIONS, ROLES, coverage, fetch_reference, search_styles
from .papers import audit_overview, pair_overview, prepare_paper


def build_parser():
    parser = argparse.ArgumentParser(prog="modelatlas", description="Paper → Overview with a verified illustration knowledge base")
    parser.add_argument("--workspace", default=os.environ.get("MODELATLAS_HOME", ".modelatlas"))
    sub = parser.add_subparsers(dest="command", required=True)
    command = sub.add_parser("paper2overview", help="Prepare a paper for host-agent overview design and generation")
    command.add_argument("path")
    command.add_argument("--problem", choices=list("ABCDEF"))
    command.add_argument("--query", default="")
    sub.add_parser("coverage", help="Report the preserved illustration knowledge base")
    command = sub.add_parser("styles", help="Search illustration references; overview is the default role")
    command.add_argument("query", nargs="?", default="")
    command.add_argument("--problem", choices=list("ABCDEF"))
    command.add_argument("--role", choices=[*ROLES, "all"], default="overview")
    command.add_argument("--collection", choices=COLLECTIONS, default="award")
    command.add_argument("--year", type=int, help="Filter by the source paper's year")
    command.add_argument("--limit", type=int, default=5)
    command = sub.add_parser("reference", help="Fetch a pinned PDF and its exact illustration page")
    command.add_argument("case_id")
    command.add_argument("--pdf-only", action="store_true")
    command = sub.add_parser("literature", help="Find papers with AnySearch; results are not curated references")
    command.add_argument("query")
    command.add_argument("--limit", type=int, default=5)
    command.add_argument("--mode", choices=["academic", "web"], default="academic")
    command = sub.add_parser("pair-overview", help="Archive an actual overview, full prompt and evidence brief")
    command.add_argument("session_dir")
    command.add_argument("--image", required=True)
    command.add_argument("--prompt", required=True)
    command.add_argument("--brief", required=True)
    command = sub.add_parser("audit-overview", help="Check paired overview file integrity, not visual quality")
    command.add_argument("directory")
    return parser


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args()
    try:
        workspace = Path(args.workspace).resolve()
        if args.command == "paper2overview":
            result = prepare_paper(args.path, workspace, args.problem, args.query)
        elif args.command == "coverage":
            result = coverage()
        elif args.command == "styles":
            role = None if args.role == "all" else args.role
            result = search_styles(args.query, args.problem, role, args.collection, args.limit, args.year)
        elif args.command == "reference":
            result = fetch_reference(args.case_id, workspace, render_page=not args.pdf_only)
        elif args.command == "literature":
            from .search import AnySearch
            result = AnySearch().search(args.query, args.limit, args.mode)
        elif args.command == "pair-overview":
            result = pair_overview(args.session_dir, args.image, args.prompt, args.brief)
        else:
            result = audit_overview(args.directory)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.command == "audit-overview" and not result["passed"]:
            raise SystemExit(2)
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(2, f"modelatlas: {error}\n")
