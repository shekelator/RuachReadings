from fastapi.testclient import TestClient

from app_fastapi import app


def test_root_renders_and_contains_static_url():
    client = TestClient(app)
    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.text
    # assert that the script tag for the static JS file is present
    assert "scripts/site.js" in html
    # assert that favicon is referenced
    assert "favicon-32x32.png" in html
    # response should be HTML
    assert "text/html" in resp.headers.get("content-type", "")
