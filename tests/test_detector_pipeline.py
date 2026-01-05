import io

from PIL import Image

from app.ml.detector import DetectorModel


def _dummy_image_bytes() -> bytes:
  img = Image.new("RGB", (128, 128), color=(100, 120, 140))
  buf = io.BytesIO()
  img.save(buf, format="PNG")
  return buf.getvalue()


def test_detector_predict_image_bytes_runs():
  model = DetectorModel()
  data = _dummy_image_bytes()
  out = model.predict_image_bytes(data)
  assert "top_class" in out
  assert "all_classes" in out
  assert isinstance(out["all_classes"], list)






