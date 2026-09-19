"""Render every checked-in example through the production pipeline."""
from pathlib import Path
import argparse

from modelatlas.common import read_json, write_json
from modelatlas.figures import render, verify_bundle
from modelatlas.gallery import gallery
from modelatlas.library import Library


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="outputs/demo")
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    db=Library(root/".modelatlas")
    db.seed()
    runs=[]
    for path in sorted((root/"examples").glob("*.json")):
        record=render(read_json(path),args.output,path.parent)
        db.record_run(record)
        runs.append(record)
        if not record["audit_passed"] or not verify_bundle(record["directory"])["passed"]:
            raise SystemExit(f"Review required: {record['directory']}")
        print(f"PASS {path.stem}: {record['directory']}")
    output=Path(args.output).resolve()
    write_json(output/"runs.json",runs)
    print(gallery(runs,output/"gallery.html"))


if __name__=="__main__":
    main()
