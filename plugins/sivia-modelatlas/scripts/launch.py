"""Resolve project venv in a checkout, or a configured Python in an installed plugin."""
import json
import os
from pathlib import Path
import subprocess
import sys

root=Path(__file__).resolve().parents[1]
runtime=root/"runtime.json"
configured=json.loads(runtime.read_text(encoding="utf-8")) if runtime.is_file() else {}
python=os.environ.get("MODELATLAS_PYTHON") or configured.get("python")
if not python:
    project=root.parents[1]
    candidate=project/".venv"/("Scripts/python.exe" if os.name=="nt" else "bin/python")
    python=str(candidate) if candidate.is_file() else sys.executable
environment=dict(os.environ)
if configured.get("workspace"):
    environment.setdefault("MODELATLAS_HOME",configured["workspace"])
raise SystemExit(subprocess.call([python,"-m","modelatlas.server"],env=environment))
