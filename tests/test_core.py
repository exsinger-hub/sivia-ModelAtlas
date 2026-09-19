import copy
import json
from pathlib import Path
import sqlite3
from unittest.mock import Mock

import numpy as np
import pytest

from modelatlas.common import read_json
from modelatlas.figures import pareto_mask, render, resolve_data, validate, verify_bundle
from modelatlas.library import Library
from modelatlas.search import AnySearch

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture
def spec():
    return read_json(ROOT/"examples/forecast.json")


def test_library_seed_is_idempotent(tmp_path):
    db=Library(tmp_path)
    first=db.seed()
    assert first==db.seed()
    assert first["cards"]==10
    assert db.search("网球 动量")[0]["id"]=="mcm-c-match-flow"
    assert Library(tmp_path).stats()==first


def test_import_text_evidence_and_reimport(tmp_path):
    paper=tmp_path/"paper.md"
    paper.write_text("# Model\nObserved values are compared with predictions.\n",encoding="utf-8")
    db=Library(tmp_path/"library")
    record=db.ingest(paper)
    assert record["status"]=="text_imported"
    assert db.evidence(record["id"],"predictions")[0]["page"]==1
    assert db.ingest(paper)["id"]==record["id"]
    assert db.stats()["sources"]==1
    assert db.evidence("missing")==[]


def test_card_requires_registered_source_and_locator(tmp_path):
    db=Library(tmp_path)
    db.seed()
    card=copy.deepcopy(db.all("cards")[0])
    card["id"]="new-card"
    card["source_ids"]=["not-registered"]
    with pytest.raises(ValueError,match="Unknown source"):
        db.add_card(card)
    card["source_ids"]=["comap-2024-c"]
    card.pop("locator")
    with pytest.raises(ValueError,match="locator"):
        db.add_card(card)
    card["locator"]="p1"
    assert db.add_card(card)["status"]=="curated"
    with pytest.raises(sqlite3.IntegrityError):
        db.add_card(card)


@pytest.mark.parametrize("filename", sorted(p.name for p in (ROOT/"examples").glob("*.json")))
def test_actual_render_bundle(tmp_path,filename):
    spec=read_json(ROOT/"examples"/filename)
    result=render(spec,tmp_path)
    directory=Path(result["directory"])
    assert result["audit_passed"],read_json(directory/"audit.json")
    assert verify_bundle(directory)["passed"]
    assert (directory/"figure.png").read_bytes().startswith(b"\x89PNG")
    assert (directory/"figure.pdf").read_bytes().startswith(b"%PDF")
    assert "<text" in (directory/"figure.svg").read_text(encoding="utf-8")
    if spec["data_status"]=="demo":
        assert "DEMO DATA" in (directory/"figure.svg").read_text(encoding="utf-8")


def test_nonfinite_rejected_without_output(tmp_path,spec):
    spec["data"]["y"][0]=float("nan")
    with pytest.raises(ValueError,match="finite"):
        render(spec,tmp_path)
    assert not list(tmp_path.iterdir())


def test_unsorted_time_and_mismatched_shapes(spec):
    spec["data"]["x"][0]=3
    with pytest.raises(ValueError,match="increasing"):
        validate(spec,spec["data"])
    spec["data"]["x"].pop()
    with pytest.raises(ValueError,match="equal lengths"):
        validate(spec,spec["data"])


def test_uncertainty_semantics(spec):
    del spec["interval_label"]
    with pytest.raises(ValueError,match="interval_label"):
        validate(spec,spec["data"])
    spec["interval_label"]="supplied range"
    spec["data"]["lower"][0]=99
    with pytest.raises(ValueError,match="Interval"):
        validate(spec,spec["data"])


def test_mixed_pareto_directions_and_ties():
    x=np.array([1,2,3,2,4])
    y=np.array([2,4,3,4,1])
    assert pareto_mask(x,y,["min","max"]).tolist()==[True,True,False,True,False]


def test_residual_metrics_are_computed(tmp_path):
    spec=read_json(ROOT/"examples/residual.json")
    spec["data"]={"observed":[2,4,6],"predicted":[1,4,8]}
    result=render(spec,tmp_path)
    metrics=read_json(Path(result["directory"])/"audit.json")["metrics"]
    assert metrics["mae"]==1
    assert metrics["rmse"]==pytest.approx(np.sqrt(5/3))


def test_tamper_detected(tmp_path,spec):
    result=render(spec,tmp_path)
    directory=Path(result["directory"])
    (directory/"data.json").write_text("{}",encoding="utf-8")
    assert not verify_bundle(directory)["passed"]


def test_csv_mapping_and_missing_values(tmp_path):
    csv=tmp_path/"input.csv"
    csv.write_text("day,score\n1,2\n2,3\n",encoding="utf-8")
    spec={"data_file":"input.csv","columns":{"x":"day","y":"score"}}
    data,source=resolve_data(spec,tmp_path)
    assert data=={"x":[1.,2.],"y":[2.,3.]}
    assert len(source["sha256"])==64
    csv.write_text("day,score\n1,\n",encoding="utf-8")
    with pytest.raises(ValueError,match="Missing/non-numeric"):
        resolve_data(spec,tmp_path)


def test_workflow_rejects_broken_edges_and_overlap():
    spec=read_json(ROOT/"examples/workflow.json")
    spec["data"]["edges"][0]["target"]="missing"
    with pytest.raises(ValueError,match="unknown node"):
        validate(spec,spec["data"])
    spec["data"]["nodes"][1]["x"]=.5
    with pytest.raises(ValueError,match="overlap"):
        validate(spec,spec["data"])


def test_anysearch_discovers_domain_and_saves_no_envelope_secret():
    session=Mock()
    discovery=Mock()
    discovery.json.return_value={"code":0,"data":{"domains":[{"sub_domains":[{"sub_domain":"academic.search","params":{}}]}]}}
    search=Mock()
    search.json.return_value={"code":0,"api_key":"DO-NOT-SAVE","data":{"results":[{"title":"Momentum","url":"https://example.org/paper","snippet":"Evidence"}]}}
    session.request.side_effect=[discovery,search]
    records=AnySearch(session).search("tennis")
    assert records[0]["status"]=="discovered"
    assert "DO-NOT-SAVE" not in json.dumps(records)
    assert session.request.call_args_list[0].args[1].endswith("/v1/sub-domains")
    assert session.request.call_args_list[1].kwargs["json"]["tag"]=="academic.search"


def test_anysearch_failure_not_empty_success():
    session=Mock()
    response=Mock()
    response.json.return_value={"code":429,"data":{"api_key":"secret"}}
    session.request.return_value=response
    with pytest.raises(RuntimeError,match="service error"):
        AnySearch(session).search("tennis")
