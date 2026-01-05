"""
Data preprocessing utilities for SkinMorph.

Includes:
- download stubs for ISIC/HAM10000 (URLs only, no automatic bulk download here)
- hooks for ethnicity/skin-tone stratification.
"""

from pathlib import Path
from typing import List

import pandas as pd


def ensure_data_dirs(base: str = "data") -> None:
    for sub in ["raw", "processed", "demo_detector", "demo_predictor"]:
        Path(base, sub).mkdir(parents=True, exist_ok=True)


def download_isic_metadata(out_csv: str = "data/raw/isic_metadata.csv") -> None:
    """
    Download ISIC metadata CSV.
    NOTE: this uses public URLs; adjust for authentication as needed.
    """
    # TODO: implement actual download with requests if acceptable for your env.
    Path(out_csv).write_text(
        "# TODO: Download ISIC metadata here. See https://isic-archive.com/\n"
    )


def stratify_by_fitzpatrick(metadata_csv: str, out_csv: str) -> None:
    """
    Placeholder for Fitzpatrick skin-type stratification.
    """
    df = pd.read_csv(metadata_csv)
    # TODO: map to Fitzpatrick I–VI using provided annotations or custom classifier.
    df.to_csv(out_csv, index=False)


if __name__ == "__main__":
    ensure_data_dirs()
    download_isic_metadata()






