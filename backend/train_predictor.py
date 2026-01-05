"""
Training script for the SkinMorph temporal risk predictor.

Uses frozen MobileNetV3 features and a small LSTM head.
Configured for tiny demo runs; extend for real datasets.
"""

from pathlib import Path
from typing import List, Tuple

import pytorch_lightning as pl
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from app.ml.predictor import PredictorConfig, TemporalHead, TIMEPOINTS
from app.ml.preprocessing import preprocess_image_bytes


class DemoSequenceDataset(Dataset):
    """
    Minimal dataset for demo: expects directory structure:
    data/demo_predictor/
        seq1/
            t0.png
            t1.png
        seq2/
            ...
    Targets are synthetic random risk vectors for illustration only.
    """

    def __init__(self, root: Path):
        self.root = root
        self.seqs: List[Path] = [p for p in root.iterdir() if p.is_dir()]

    def __len__(self) -> int:
        return len(self.seqs)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor]:
        seq_dir = self.seqs[idx]
        images = sorted(seq_dir.glob("*.png"))
        feats: List[torch.Tensor] = []
        for img_path in images:
            data = img_path.read_bytes()
            x = preprocess_image_bytes(data).squeeze(0)
            feats.append(x.mean(dim=(1, 2)))  # crude stand-in for backbone features

        seq = torch.stack(feats, dim=0)  # (T, F)
        target = torch.zeros(len(TIMEPOINTS) * 3)
        return seq, target


class LightningPredictor(pl.LightningModule):
    def __init__(self, cfg: PredictorConfig):
        super().__init__()
        self.cfg = cfg
        self.head = TemporalHead(cfg)
        self.loss_fn = nn.MSELoss()

    def forward(self, seq: torch.Tensor) -> torch.Tensor:
        return self.head(seq)

    def training_step(self, batch, batch_idx):
        seq, y = batch
        logits = self(seq)
        loss = self.loss_fn(logits, y)
        self.log("train_loss", loss)
        return loss

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)


def collate_fn(batch):
    # Simple collate assuming equal length sequences
    seqs, ys = zip(*batch)
    seqs_t = torch.stack(seqs, dim=0)
    ys_t = torch.stack(ys, dim=0)
    return seqs_t, ys_t


def main(
    data_dir: str = "data/demo_predictor",
    max_epochs: int = 1,
):
    cfg = PredictorConfig()
    ds = DemoSequenceDataset(Path(data_dir))
    loader = DataLoader(ds, batch_size=2, shuffle=True, collate_fn=collate_fn)

    model = LightningPredictor(cfg)
    trainer = pl.Trainer(max_epochs=max_epochs)
    trainer.fit(model, loader)


if __name__ == "__main__":
    main()






