"""
Evaluation script for detector on a labeled dataset.

Computes per-class precision/recall/F1 and (placeholder) skin-tone-stratified metrics.
"""

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from sklearn.metrics import classification_report
from torchvision.datasets import ImageFolder
import torchvision.transforms as T

from app.ml.detector import DetectorModel, CLASS_NAMES
from app.ml.preprocessing import IMG_SIZE


def evaluate_detector(
    data_dir: str = "data/demo_detector/val",
    metadata_csv: Optional[str] = None,
) -> None:
    """
    Evaluate detector on an ImageFolder dataset.
    If metadata_csv is provided, it is expected to contain columns:
      - filepath: relative path to image within data_dir
      - fitzpatrick: categorical label like I, II, III, IV, V, VI
    and stratified metrics will be printed per Fitzpatrick group.
    """
    model = DetectorModel()

    ds = ImageFolder(
        data_dir,
        transform=T.Compose(
            [
                T.Resize((IMG_SIZE, IMG_SIZE)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        ),
    )

    y_true: List[int] = []
    y_pred: List[int] = []
    paths: List[str] = []

    for img, label in ds:
        logits = model.model(img.unsqueeze(0))
        pred = int(logits.argmax(dim=1).item())
        y_true.append(label)
        y_pred.append(pred)

    # sklearn classification report (overall)
    report = classification_report(
        y_true, y_pred, target_names=CLASS_NAMES, digits=3, zero_division=0
    )
    print("=== Overall metrics ===")
    print(report)

    # Optional: tone-stratified metrics
    if metadata_csv and Path(metadata_csv).exists():
        print("\n=== Fitzpatrick-stratified metrics ===")
        meta = pd.read_csv(metadata_csv)
        # Expect ds.samples give (path, class_idx)
        paths = [p for (p, _) in ds.samples]
        df_eval = pd.DataFrame(
            {"filepath": [Path(p).relative_to(data_dir).as_posix() for p in paths],
             "y_true": y_true,
             "y_pred": y_pred}
        )
        merged = df_eval.merge(meta, on="filepath", how="left")
        for group, sub in merged.groupby("fitzpatrick"):
            if pd.isna(group):
                continue
            print(f"\n--- Fitzpatrick {group} ---")
            print(
                classification_report(
                    sub["y_true"],
                    sub["y_pred"],
                    target_names=CLASS_NAMES,
                    digits=3,
                    zero_division=0,
                )
            )
    else:
        print(
            "\nNOTE: To enable skin-tone-stratified metrics, provide a metadata CSV "
            "with filepath and fitzpatrick columns."
        )


if __name__ == "__main__":
    evaluate_detector()


