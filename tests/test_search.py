import json
from unittest.mock import Mock

import pytest

from modelatlas.search import AnySearch


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
