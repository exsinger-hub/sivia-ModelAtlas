"""Data-bound plotting. No eval, generated data or implicit model fitting."""
from __future__ import annotations

import csv
import io
import json
import platform
import re
import threading
import warnings
from pathlib import Path
from uuid import uuid4

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

from . import __version__
from .common import digest, now, read_json, slug, write_json

KINDS = {"line", "forecast", "scatter", "residual", "sensitivity", "heatmap", "pareto", "workflow"}
COLORS = ["#007C91", "#E58A2B", "#7466AF", "#429977", "#C95D6D"]
RENDER_LOCK = threading.Lock()


def vector(data, name, minimum=1):
    try:
        arr = np.asarray(data[name], dtype=float)
    except (KeyError, TypeError, ValueError):
        raise ValueError(f"{name}: required numeric array") from None
    if arr.ndim != 1 or len(arr) < minimum or not np.isfinite(arr).all():
        raise ValueError(f"{name}: expected >= {minimum} finite numbers")
    return arr


def same_length(*arrays):
    if len({len(a) for a in arrays}) != 1:
        raise ValueError("Data arrays must have equal lengths")


def resolve_data(spec, base_dir):
    if "data" in spec and "data_file" in spec:
        raise ValueError("Specify data or data_file, not both")
    if "data_file" not in spec:
        if not isinstance(spec.get("data"), dict):
            raise ValueError("data object required")
        return spec["data"], None
    path = (Path(base_dir) / spec["data_file"]).resolve()
    if path.suffix.lower() == ".json":
        return read_json(path), {"filename": path.name, "sha256": digest(path)}
    if path.suffix.lower() != ".csv":
        raise ValueError("data_file supports JSON or CSV")
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        headers = reader.fieldnames or []
    mapping = spec.get("columns", {})
    if not mapping or not rows:
        raise ValueError("CSV requires nonempty rows and a columns mapping")
    if len(headers) != len(set(headers)):
        raise ValueError("CSV contains duplicate column names")
    data = {}
    for key, column in mapping.items():
        if column not in headers:
            raise ValueError(f"CSV column not found: {column}")
        values = [row[column] for row in rows]
        if key in {"labels", "categories"}:
            data[key] = values
        else:
            try:
                data[key] = [float(v) for v in values]
            except (ValueError, TypeError):
                raise ValueError(f"Missing/non-numeric CSV value in {column}; clean explicitly before rendering") from None
    return data, {"filename": path.name, "sha256": digest(path)}


def validate(spec, data):
    kind = spec.get("kind")
    if kind not in KINDS:
        raise ValueError("kind must be one of " + ", ".join(sorted(KINDS)))
    for name in ("title", "claim", "data_status", "source_note"):
        if not isinstance(spec.get(name), str) or not spec[name].strip():
            raise ValueError(f"{name} is required")
    if spec["data_status"] not in {"demo", "provided", "empirical", "conceptual"}:
        raise ValueError("data_status must be demo, provided, empirical or conceptual")
    if kind != "workflow" and spec["data_status"] == "conceptual":
        raise ValueError("Numeric figures require demo, provided or empirical data_status")
    if not 3 <= spec.get("width", 7.2) <= 20 or not 2 <= spec.get("height", 4.5) <= 20:
        raise ValueError("Canvas must be 3..20 inches wide and 2..20 high")
    if kind != "workflow":
        if not spec.get("x_label") or not spec.get("y_label"):
            raise ValueError("x_label and y_label required (include units where applicable)")
    if kind in {"line", "forecast", "scatter", "pareto"}:
        x, y = vector(data, "x", 2), vector(data, "y", 2)
        same_length(x, y)
        if kind in {"line", "forecast"} and np.any(np.diff(x) <= 0):
            raise ValueError("Ordered curves require strictly increasing x; sort/aggregate explicitly")
        if "y2" in data:
            same_length(x, vector(data, "y2"))
        if kind == "forecast":
            same_length(x, vector(data, "predicted"))
            if ("lower" in data) != ("upper" in data):
                raise ValueError("Supply both lower and upper bounds")
            if "lower" in data:
                lo, hi, pred = vector(data, "lower"), vector(data, "upper"), vector(data, "predicted")
                same_length(x, lo, hi)
                if np.any(lo > hi) or np.any(pred < lo) or np.any(pred > hi):
                    raise ValueError("Interval must contain the prediction and lower <= upper")
                if not spec.get("interval_label"):
                    raise ValueError("interval_label must identify the supplied interval; no default CI claim")
        if kind == "pareto" and spec.get("directions", ["min", "min"]) not in [["min","min"],["min","max"],["max","min"],["max","max"]]:
            raise ValueError("directions needs two min/max entries")
    elif kind == "residual":
        same_length(vector(data, "observed", 2), vector(data, "predicted", 2))
    elif kind == "sensitivity":
        lo, hi = vector(data, "low"), vector(data, "high")
        labels = data.get("labels", [])
        same_length(lo, hi, labels)
        if not labels or len(labels) > 30 or not np.isfinite(float(data.get("baseline", np.nan))):
            raise ValueError("Sensitivity needs <=30 labels and a finite baseline")
    elif kind == "heatmap":
        values = np.asarray(data.get("values", []), dtype=float)
        if values.ndim != 2 or min(values.shape) < 1 or max(values.shape) > 30 or not np.isfinite(values).all():
            raise ValueError("Heatmap needs a finite 2D matrix, at most 30x30")
        if values.shape != (len(data.get("rows", [])), len(data.get("columns", []))):
            raise ValueError("Heatmap row/column labels must match matrix shape")
        if spec.get("correlation"):
            if values.shape[0] != values.shape[1] or not np.allclose(values, values.T) or np.any(abs(values) > 1):
                raise ValueError("Correlation matrix must be square, symmetric and within [-1,1]")
    else:
        nodes = data.get("nodes", [])
        ids = [n.get("id") for n in nodes]
        if not nodes or len(nodes) > 24 or any(not i for i in ids) or len(set(ids)) != len(ids):
            raise ValueError("Workflow requires 1..24 uniquely named nodes")
        bounds = []
        for node in nodes:
            if not node.get("label"):
                raise ValueError("Each node needs a label")
            x, y, w, h = (float(node.get(k, default)) for k, default in (("x", np.nan),("y",np.nan),("w",1.6),("h",0.75)))
            if not np.isfinite([x,y,w,h]).all() or w <= 0 or h <= 0 or x < 0 or y < 0 or x+w > 10 or y+h > 6:
                raise ValueError("Workflow bounds must fit 10x6 coordinate canvas")
            for a,b,c,d in bounds:
                if x < a+c and a < x+w and y < b+d and b < y+h:
                    raise ValueError("Workflow nodes overlap; revise layout")
            bounds.append((x,y,w,h))
        for edge in data.get("edges", []):
            if edge.get("source") not in ids or edge.get("target") not in ids:
                raise ValueError("Workflow edge references unknown node")
            if edge["source"] == edge["target"]:
                raise ValueError("Self-edges require a separate feedback node in v0.1")


def pareto_mask(x, y, directions):
    points = np.column_stack((x,y)) * np.array([1 if d == "min" else -1 for d in directions])
    return np.array([not np.any(np.all(points <= p, axis=1) & np.any(points < p, axis=1)) for p in points])


def _draw(spec, data):
    kind = spec["kind"]
    fig, ax = plt.subplots(figsize=(spec.get("width", 7.2), spec.get("height", 4.5)))
    fig.subplots_adjust(left=.28 if kind == "sensitivity" else .14, right=.94, top=.82, bottom=.22)
    fig.suptitle(spec["title"], x=.14, y=.96, ha="left", fontsize=14, weight="bold", color="#18334B")
    status = "DEMO DATA" if spec["data_status"] == "demo" else spec["data_status"].upper()
    # Long provenance stays in the manifest; caption is deliberately concise.
    note = spec["source_note"]
    if len(note) > 110:
        note = note[:107] + "..."
    fig.text(.14, .055, status + " | " + note, fontsize=8, color="#526779", wrap=True)
    metrics = {}
    if kind in {"line", "forecast"}:
        ax.plot(data["x"], data["y"], color=COLORS[0], lw=1.8, label=spec.get("y_legend", "Observed"))
        if kind == "line" and "y2" in data:
            ax.plot(data["x"], data["y2"], color=COLORS[1], lw=1.6, ls="--", label=spec.get("y2_legend", "Comparison"))
        if kind == "forecast":
            ax.plot(data["x"], data["predicted"], color=COLORS[1], ls="--", label="Prediction (supplied)")
            if "lower" in data:
                ax.fill_between(data["x"], data["lower"], data["upper"], color=COLORS[1], alpha=.16, label=spec["interval_label"])
            if "split_x" in spec:
                ax.axvline(spec["split_x"], color="#687B86", ls=":", label="Train / test split")
        ax.legend(frameon=False, fontsize=8)
    elif kind in {"scatter", "pareto"}:
        x, y = vector(data,"x"), vector(data,"y")
        ax.scatter(x, y, color=COLORS[0], s=34, alpha=.7, linewidths=.5, edgecolors="white")
        if kind == "pareto":
            directions = spec.get("directions", ["min","min"])
            mask = pareto_mask(x,y,directions)
            order = np.argsort(x[mask])
            ax.plot(x[mask][order], y[mask][order], "o--", color=COLORS[1], label="Non-dominated candidates")
            ax.legend(frameon=False, fontsize=8)
            metrics = {"directions":directions, "pareto_indices":np.flatnonzero(mask).tolist()}
    elif kind == "residual":
        actual, predicted = vector(data,"observed"), vector(data,"predicted")
        residual = actual - predicted
        ax.scatter(predicted, residual, color=COLORS[0], alpha=.7, s=32)
        ax.axhline(0, color=COLORS[1], lw=1.3)
        metrics = {"n":len(actual), "mae":float(np.abs(residual).mean()), "rmse":float(np.sqrt((residual**2).mean())), "residual_definition":"observed - predicted"}
        ax.text(.03, .96, f"RMSE {metrics['rmse']:.3g}  |  MAE {metrics['mae']:.3g}", transform=ax.transAxes, va="top", fontsize=9)
    elif kind == "sensitivity":
        base = float(data["baseline"])
        lo, hi = vector(data,"low"), vector(data,"high")
        order = np.argsort(np.maximum(abs(lo-base),abs(hi-base)))
        for i, idx in enumerate(order):
            ax.plot([lo[idx],hi[idx]],[i,i],color="#AFC3CA",lw=3)
        ax.scatter(lo[order],range(len(lo)),color=COLORS[0],label="Low-parameter scenario",zorder=3)
        ax.scatter(hi[order],range(len(hi)),color=COLORS[1],label="High-parameter scenario",zorder=3)
        ax.set_yticks(range(len(lo)),[data["labels"][i] for i in order])
        ax.axvline(base,color="#536D7A",ls=":",label="Baseline")
        ax.legend(frameon=False,fontsize=7,loc="best")
    elif kind == "heatmap":
        values = np.asarray(data["values"],dtype=float)
        limit = max(float(abs(values).max()), 1e-12)
        cmap_args = {"cmap":"RdBu_r","vmin":-1,"vmax":1} if spec.get("correlation") else {"cmap":"viridis"}
        if spec.get("center_zero") and not spec.get("correlation"):
            cmap_args = {"cmap":"RdBu_r","vmin":-limit,"vmax":limit}
        field = ax.imshow(values,aspect="auto",**cmap_args)
        ax.set_xticks(range(values.shape[1]),data["columns"],rotation=35,ha="right")
        ax.set_yticks(range(values.shape[0]),data["rows"])
        fig.colorbar(field,ax=ax,shrink=.8,label=spec.get("color_label","Value"))
        if max(values.shape) <= 10:
            for (r,c),v in np.ndenumerate(values):
                rgba=field.cmap(field.norm(v))
                luminance=.2126*rgba[0]+.7152*rgba[1]+.0722*rgba[2]
                ax.text(c,r,f"{v:.2g}",ha="center",va="center",fontsize=8,color="black" if luminance>.55 else "white")
    else:
        ax.set(xlim=(0,10),ylim=(0,6))
        ax.axis("off")
        nodes = {n["id"]:n for n in data["nodes"]}
        for edge in data.get("edges",[]):
            a,b=nodes[edge["source"]],nodes[edge["target"]]
            ca=np.array([a["x"]+a.get("w",1.6)/2,a["y"]+a.get("h",.75)/2])
            cb=np.array([b["x"]+b.get("w",1.6)/2,b["y"]+b.get("h",.75)/2])
            delta=cb-ca
            def endpoint(center,node,d):
                factors=[node.get("w",1.6)/2/abs(d[0]) if d[0] else np.inf,node.get("h",.75)/2/abs(d[1]) if d[1] else np.inf]
                return center+d*min(factors)
            start,end=endpoint(ca,a,delta),endpoint(cb,b,-delta)
            ax.annotate("",xy=end,xytext=start,arrowprops={"arrowstyle":"->","color":"#748C99","lw":1.2,"shrinkA":3,"shrinkB":3},zorder=1)
            if edge.get("label"):
                mid=(start+end)/2
                ax.text(*mid,edge["label"],fontsize=7,ha="center",va="bottom",backgroundcolor="white")
        for i,node in enumerate(nodes.values()):
            x,y,w,h=node["x"],node["y"],node.get("w",1.6),node.get("h",.75)
            box=FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.025,rounding_size=0.10",facecolor="#EEF5F7",edgecolor=COLORS[i%len(COLORS)],linewidth=1.2,zorder=2)
            ax.add_patch(box)
            label=ax.text(x+w/2,y+h/2,node["label"],ha="center",va="center",fontsize=9,zorder=3)
            label._atlas_node = (x,y,w,h)
        metrics = {"nodes":len(nodes),"edges":len(data.get("edges",[]))}
    if kind != "workflow":
        ax.set_xlabel(spec["x_label"])
        ax.set_ylabel(spec["y_label"])
        ax.spines[["top","right"]].set_visible(False)
        if kind != "heatmap":
            ax.grid(axis="y",alpha=.18,lw=.6)
            ax.set_axisbelow(True)
    return fig, metrics


def render(spec, output_root, base_dir="."):
    data, provenance = resolve_data(spec, base_dir)
    validate(spec,data)
    run_id = slug(spec.get("id",spec["kind"]))+"-"+uuid4().hex[:12]
    output = Path(output_root).resolve()/run_id
    output.mkdir(parents=True,exist_ok=False)
    normalized={**spec,"data":data}
    normalized.pop("data_file",None)
    normalized.pop("columns",None)
    with RENDER_LOCK, matplotlib.rc_context({"svg.fonttype":"none","pdf.fonttype":42,"font.size":10,
            "font.family":"sans-serif","font.sans-serif":["DejaVu Sans","Microsoft YaHei","SimHei"],"axes.unicode_minus":False}):
        fig=None
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                fig,metrics=_draw(normalized,data)
                fig.canvas.draw()
                renderer=fig.canvas.get_renderer()
                failures=[]
                texts = list(fig.texts)
                for axes in fig.axes:
                    texts.extend(axes.texts)
                    texts.extend([axes.xaxis.label, axes.yaxis.label, axes.title])
                for text in texts:
                    if not text.get_visible() or not text.get_text():
                        continue
                    bb=text.get_window_extent(renderer)
                    if bb.x0 < -2 or bb.y0 < -2 or bb.x1 > fig.bbox.x1+2 or bb.y1 > fig.bbox.y1+2:
                        failures.append("Text outside canvas: "+text.get_text()[:70])
                    if hasattr(text,"_atlas_node"):
                        x,y,w,h=text._atlas_node
                        left,bottom=text.axes.transData.transform((x,y))
                        right,top=text.axes.transData.transform((x+w,y+h))
                        if bb.x0<left or bb.x1>right or bb.y0<bottom or bb.y1>top:
                            failures.append("Node label does not fit: "+text.get_text())
                for extension in ("png","svg","pdf"):
                    fig.savefig(output/f"figure.{extension}",dpi=220,facecolor="white")
                messages=sorted({str(w.message) for w in caught if "Glyph" in str(w.message)})
                failures.extend(messages)
        finally:
            if fig is not None:
                plt.close(fig)
    write_json(output/"spec.json",normalized)
    write_json(output/"data.json",data)
    (output/"prompt.md").write_text(f"# {spec['title']}\n\nFigure claim: {spec['claim']}\n\nRecipe: {spec['kind']}\n\nSource: {spec['source_note']}\n\nThe exact numerical binding and layout are in spec.json.\n",encoding="utf-8")
    audit={"passed":not failures,"findings":failures,"scope":"data validation, canvas text and node text fit; human review remains pending",
           "visual_review":"pending","data_status":spec["data_status"],"metrics":metrics}
    write_json(output/"audit.json",audit)
    record={"id":run_id,"title":spec["title"],"kind":spec["kind"],"created_at":now(),"directory":str(output),
            "source_ids":spec.get("source_ids",[]),"data_status":spec["data_status"],"input_file":provenance,
            "version":__version__,"python":platform.python_version(),"matplotlib":matplotlib.__version__,
            "numpy":np.__version__,"audit_passed":audit["passed"],"visual_review":"pending",
            "files":{p.name:digest(p) for p in output.iterdir() if p.is_file()}}
    write_json(output/"manifest.json",record)
    return record


def verify_bundle(directory):
    directory=Path(directory).resolve()
    manifest=read_json(directory/"manifest.json")
    failures=[]
    mandatory={"spec.json","data.json","prompt.md","audit.json","figure.png","figure.svg","figure.pdf"}
    recorded=manifest.get("files",{})
    failures.extend("Missing manifest entry: "+name for name in sorted(mandatory-set(recorded)))
    for name,expected in recorded.items():
        target=(directory/name).resolve()
        if target.parent!=directory or not target.is_file() or digest(target)!=expected:
            failures.append("Missing/changed artifact: "+name)
    if not failures:
        try:
            spec=read_json(directory/"spec.json")
            validate(spec,spec["data"])
            if spec["data"]!=read_json(directory/"data.json"):
                failures.append("Spec/data snapshot mismatch")
        except (KeyError,ValueError) as error:
            failures.append(str(error))
    return {"passed":not failures,"findings":failures,"id":manifest.get("id"),"scope":"bundle integrity, not scientific correctness or human approval"}
