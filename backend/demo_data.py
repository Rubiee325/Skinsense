"""
Utility to generate a tiny synthetic demo dataset so the pipeline can be tested
without downloading real medical images.
"""

from pathlib import Path

from PIL import Image, ImageDraw


def _make_square(path: Path, color: tuple[int, int, int]) -> None:
    img = Image.new("RGB", (224, 224), color)
    draw = ImageDraw.Draw(img)
    draw.ellipse((60, 60, 160, 160), outline=(255, 255, 255), width=4)
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path)


def create_demo_detector_dataset(base: str = "data/demo_detector") -> None:
    base_path = Path(base)
    for split in ["train", "val"]:
        _make_square(base_path / split / "benign_nevus" / "img1.png", (80, 120, 200))
        _make_square(base_path / split / "acne" / "img2.png", (160, 80, 80))


def create_demo_predictor_dataset(base: str = "data/demo_predictor") -> None:
    base_path = Path(base)
    seq1 = base_path / "seq1"
    seq2 = base_path / "seq2"
    _make_square(seq1 / "t0.png", (80, 120, 200))
    _make_square(seq1 / "t1.png", (70, 110, 190))
    _make_square(seq2 / "t0.png", (160, 80, 80))
    _make_square(seq2 / "t1.png", (150, 70, 70))


if __name__ == "__main__":
    create_demo_detector_dataset()
    create_demo_predictor_dataset()
    print("Demo datasets created under data/demo_detector and data/demo_predictor.")






