from fastapi.testclient import TestClient

from app_fastapi import app


def test_static_scripts_served():
    client = TestClient(app)
    resp = client.get("/static/scripts/site.js")
    assert resp.status_code == 200
    content_type = resp.headers.get("content-type", "")
    assert "javascript" in content_type or "text/plain" in content_type
    text = resp.text
    # known function string from the JS file
    assert "enableCopyButton" in text
