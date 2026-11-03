"""健康检查接口测试。"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "乡音守护者" in data["app"]


def test_module_status():
    for path in ["/api/v1/asr/status", "/api/v1/tts/status",
                 "/api/v1/llm/status", "/api/v1/rag/status",
                 "/api/v1/kg/status"]:
        r = client.get(path)
        assert r.status_code == 200
        assert r.json()["status"] == "placeholder"
