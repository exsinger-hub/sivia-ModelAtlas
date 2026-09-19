import argparse
import json
import os
import sys
from pathlib import Path

from .common import read_json
from .library import Library


def build_parser():
    parser=argparse.ArgumentParser(prog="modelatlas",description="MCM/ICM papers, knowledge cards and data figures")
    parser.add_argument("--workspace",default=os.environ.get("MODELATLAS_HOME",".modelatlas"))
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("init",help="Initialize and seed the local library")
    sub.add_parser("status")
    for name in ("search","literature"):
        command=sub.add_parser(name,help="Search local cards" if name=="search" else "Search AnySearch and import discovery records")
        command.add_argument("query")
        command.add_argument("--limit",type=int,default=5)
        if name=="search":
            command.add_argument("--kind",choices=["cards","sources","runs"],default="cards")
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
        elif args.command=="search":
            result=library.search(args.query,args.kind,args.limit)
        elif args.command=="literature":
            from .search import AnySearch
            result=AnySearch().search(args.query,args.limit)
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
