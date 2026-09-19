import argparse
import json
import os
import sys
from pathlib import Path

from .common import read_json
from .library import Library


def build_parser():
    parser=argparse.ArgumentParser(prog="modelatlas",description="MCM/ICM draft-to-overview, O/F figure references and data figures")
    parser.add_argument("--workspace",default=os.environ.get("MODELATLAS_HOME",".modelatlas"))
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("init",help="Initialize and seed the local library")
    sub.add_parser("status")
    sub.add_parser("coverage",help="Report verified O/F and research-extension coverage by A–F")
    command=sub.add_parser("styles",help="Search visually reviewed figure cases; award core by default")
    command.add_argument("query",nargs="?",default="")
    command.add_argument("--problem",choices=list("ABCDEF"))
    command.add_argument("--role",choices=["overview","mechanism","algorithm","data_plot","explanation"])
    command.add_argument("--collection",choices=["award","research","all"],default="award")
    command.add_argument("--limit",type=int,default=5)
    command=sub.add_parser("reference",help="Fetch pinned source PDF and render the exact reference page")
    command.add_argument("case_id")
    command.add_argument("--pdf-only",action="store_true")
    command=sub.add_parser("draft2overview",help="Prepare draft and reference candidates for host-agent design; not image generation")
    command.add_argument("path")
    command.add_argument("--problem",choices=list("ABCDEF"))
    command.add_argument("--query",default="")
    command=sub.add_parser("pair-overview",help="Archive actual overview, full prompt and evidence/review brief")
    command.add_argument("session_dir")
    command.add_argument("--image",required=True)
    command.add_argument("--prompt",required=True)
    command.add_argument("--brief",required=True)
    command=sub.add_parser("audit-overview",help="Verify paired overview file hashes, not visual quality")
    command.add_argument("directory")
    for name in ("search","literature"):
        command=sub.add_parser(name,help="Search local cards" if name=="search" else "Search AnySearch and import discovery records")
        command.add_argument("query")
        command.add_argument("--limit",type=int,default=5)
        if name=="search":
            command.add_argument("--kind",choices=["cards","sources","runs"],default="cards")
        else:
            command.add_argument("--mode",choices=["academic","web"],default="academic")
    command=sub.add_parser("ingest",help="Import local PDF/Markdown/TXT with page-bound text")
    command.add_argument("path")
    command.add_argument("--title")
    command.add_argument("--url")
    command=sub.add_parser("evidence")
    command.add_argument("source_id")
    command.add_argument("--query",default="")
    command=sub.add_parser("add-card")
    command.add_argument("path")
    command=sub.add_parser("render")
    command.add_argument("spec")
    command.add_argument("--output",default="outputs")
    command=sub.add_parser("audit")
    command.add_argument("directory")
    command=sub.add_parser("gallery")
    command.add_argument("--output",default="outputs/gallery.html")
    return parser


def main():
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser=build_parser()
    args=parser.parse_args()
    try:
        library=Library(args.workspace)
        library.seed()
        if args.command in {"init","status"}:
            result={"workspace":str(library.root),**library.stats()}
        elif args.command=="coverage":
            from .corpus import coverage
            result=coverage()
        elif args.command=="styles":
            from .corpus import search_styles
            result=search_styles(args.query,args.problem,args.role,args.collection,args.limit)
        elif args.command=="reference":
            from .corpus import fetch_reference
            result=fetch_reference(args.case_id,library.root,render_page=not args.pdf_only)
        elif args.command=="draft2overview":
            from .drafts import prepare_draft
            result=prepare_draft(args.path,library.root,args.problem,args.query)
        elif args.command=="pair-overview":
            from .drafts import pair_overview
            result=pair_overview(args.session_dir,args.image,args.prompt,args.brief)
        elif args.command=="audit-overview":
            from .drafts import audit_overview
            result=audit_overview(args.directory)
            if not result["passed"]:
                print(json.dumps(result,ensure_ascii=False,indent=2))
                return sys.exit(2)
        elif args.command=="search":
            result=library.search(args.query,args.kind,args.limit)
        elif args.command=="literature":
            from .search import AnySearch
            result=AnySearch().search(args.query,args.limit,args.mode)
            for record in result:
                library.put_source(record)
        elif args.command=="ingest":
            result=library.ingest(args.path,args.title,args.url)
        elif args.command=="evidence":
            result=library.evidence(args.source_id,args.query)
        elif args.command=="add-card":
            result=library.add_card(read_json(args.path))
        elif args.command=="render":
            from .figures import render
            path=Path(args.spec).resolve()
            result=render(read_json(path),args.output,path.parent)
            library.record_run(result)
            if not result["audit_passed"]:
                print(json.dumps(result,ensure_ascii=False,indent=2))
                return sys.exit(2)
        elif args.command=="audit":
            from .figures import verify_bundle
            result=verify_bundle(args.directory)
            if not result["passed"]:
                print(json.dumps(result,ensure_ascii=False,indent=2))
                return sys.exit(2)
        else:
            from .gallery import gallery
            result={"gallery":str(gallery(library.all("runs"),args.output))}
        print(json.dumps(result,ensure_ascii=False,indent=2))
    except (ValueError, OSError, RuntimeError) as error:
        parser.exit(2, f"modelatlas: {error}\n")
