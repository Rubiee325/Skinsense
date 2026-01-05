"""
Small sanity check script that:
- Starts the FastAPI app (if not already running) is assumed running on localhost:8000
- Sends demo images to /predict
"""

from pathlib import Path

import httpx


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






