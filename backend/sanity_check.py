"""
Small sanity check script that:
- Starts the FastAPI app (if not already running) is assumed running on localhost:8000
- Sends demo images to /predict
"""

from pathlib import Path

import httpx
# sanity_check.py
import cv2
import numpy as np


def run_sanity_check():
    demo_dir = Path("data/demo_detector/val")
    if not demo_dir.exists():
        print("Demo directory data/demo_detector/val not found; create a few sample images.")
        return

    client = httpx.Client(base_url="http://localhost:8000")

    for img_path in demo_dir.rglob("*.png"):
        print(f"Sending {img_path} to /predict")
        with img_path.open("rb") as f:
            files = {"file": (img_path.name, f, "image/png")}
            resp = client.post("/predict", files=files)
        print(resp.status_code, resp.json())


if __name__ == "__main__":
    run_sanity_check()


def is_skin_image(image):
    """
    Checks whether uploaded image contains human skin
    Returns True if skin image, else False
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([0, 40, 60], dtype="uint8")
    upper = np.array([20, 150, 255], dtype="uint8")

    skin_mask = cv2.inRange(hsv, lower, upper)
    skin_ratio = np.sum(skin_mask > 0) / skin_mask.size

    return skin_ratio > 0.15
def is_skin_image_from_bytes(image_bytes: bytes) -> bool:
    """
    Checks whether uploaded image bytes contain human skin.
    Used by FastAPI /predict endpoint.
    """
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        return False

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Skin color range
    lower = np.array([0, 40, 60], dtype="uint8")
    upper = np.array([20, 150, 255], dtype="uint8")

    skin_mask = cv2.inRange(hsv, lower, upper)
    skin_ratio = np.sum(skin_mask > 0) / skin_mask.size

    return skin_ratio > 0.15







