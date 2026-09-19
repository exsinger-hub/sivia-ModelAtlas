"""AnySearch REST adapter matching skill 3.1.1, without copying credentials."""
import os
import hashlib
import requests

from .common import now


class AnySearch:
    BASE = "https://api.anysearch.com"

    def __init__(self, session=None):
        self.session = session or requests.Session()

    def request(self, method, path, **kwargs):
        headers = {"X-Anysearch-Client": "sivia-modelatlas/0.2.0"}
        key = os.environ.get("ANYSEARCH_API_KEY")
        if key:
            headers["Authorization"] = "Bearer " + key
        try:
            response = self.session.request(method, self.BASE + path, headers=headers, timeout=30, **kwargs)
            response.raise_for_status()
            body = response.json()
        except (requests.RequestException, ValueError) as error:
            raise RuntimeError(f"AnySearch request failed ({type(error).__name__}); check network/key/quota") from None
        if not isinstance(body, dict) or body.get("code", 0) != 0:
            raise RuntimeError("AnySearch returned a service error; nothing was imported")
        # Never persist the response envelope: it can include credentials.
        return body.get("data") or {}

    def search(self, query, limit=5, mode="academic"):
        if not query.strip() or not 1 <= limit <= 10:
            raise ValueError("Query required; limit must be 1..10")
        if mode not in ("academic", "web"):
            raise ValueError("AnySearch mode must be academic or web")
        # Discover academic capability even for an explicit web query; contest papers
        # often need exact team/official-site searches in addition to the academic index.
        discovery = self.request("GET", "/v1/sub-domains", params={"domain": "academic"})
        domains = discovery.get("domains", [])
        available = [s for d in domains for s in d.get("sub_domains", []) if s.get("sub_domain") == "academic.search"]
        if not available and mode == "academic":
            raise RuntimeError("AnySearch academic.search currently unavailable")
        payload = {"query": query, "max_results": limit}
        if mode == "academic":
            payload["tag"] = "academic.search"
            params = {name: "" for name, info in available[0].get("params", {}).items() if info.get("required")}
            if params:
                payload["params"] = params
        data = self.request("POST", "/v1/search", json=payload)
        result = []
        for item in data.get("results", []):
            url = item.get("url")
            if not url or not url.startswith(("https://", "http://")):
                continue
            result.append({"id": "search-" + hashlib.sha256(url.encode()).hexdigest()[:16],
                           "title": item.get("title") or url, "url": url,
                           "snippet": item.get("content") or item.get("snippet") or "",
                           "status": "discovered", "provider": "AnySearch", "search_mode": mode, "query": query, "checked_at": now()})
        return result
