import io

from fastapi.testclient import TestClient
from PIL import Image

from app.main import app


client = TestClient(app)


def _make_dummy_image() -> bytes:
    img = Image.new("RGB", (64, 64), color=(128, 64, 64))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_predict_endpoint_runs():
    img_bytes = _make_dummy_image()
    files = {"file": ("dummy.png", io.BytesIO(img_bytes), "image/png")}
    resp = client.post("/predict", files=files)
    assert resp.status_code == 200
    data = resp.json()
    assert "prediction" in data
    assert "top_class" in data["prediction"]






