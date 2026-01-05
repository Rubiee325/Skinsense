"""
Training script for the skin disease detector using PyTorch Lightning.

This is a lightweight template and is configured to run on a tiny demo dataset
for sanity checking. For real training on ISIC/HAM10000, update the dataset path,
batch size, and number of epochs.
"""

from pathlib import Path
from typing import Optional

import pytorch_lightning as pl
import torch
import torch.nn as nn
from pytorch_lightning.callbacks import ModelCheckpoint
from torch.utils.data import DataLoader, Dataset
from torchvision.datasets import ImageFolder
import torchvision.transforms as T

from app.ml.detector import DetectorConfig, CLASS_NAMES
from app.ml.preprocessing import IMG_SIZE


class DermDataset(Dataset):
    def __init__(self, root: Path, train: bool = True) -> None:
        tfm_list = [
            T.Resize((IMG_SIZE, IMG_SIZE)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
        if train:
            tfm_list.insert(0, T.RandomHorizontalFlip())
        self.ds = ImageFolder(str(root), transform=T.Compose(tfm_list))

    def __len__(self) -> int:
        return len(self.ds)

    def __getitem__(self, idx: int):
        return self.ds[idx]


class LightningDetector(pl.LightningModule):
    def __init__(self, num_classes: int, lr: float = 1e-4):
        super().__init__()
        from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

        weights = MobileNet_V3_Small_Weights.DEFAULT
        self.model = mobilenet_v3_small(weights=weights)
        in_features = self.model.classifier[3].in_features
        self.model.classifier[3] = nn.Linear(in_features, num_classes)
        self.lr = lr
        self.criterion = nn.CrossEntropyLoss()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = self.criterion(logits, y)
        self.log("val_loss", loss, prog_bar=True)

    def configure_optimizers(self):
        return torch.optim.Adam(self.parameters(), lr=self.lr)


def main(
    data_dir: str = "data/demo_detector",
    out_dir: str = "models/demo_weights",
    max_epochs: int = 1,
) -> None:
    cfg = DetectorConfig()
    num_classes = len(CLASS_NAMES)

    train_ds = DermDataset(Path(data_dir) / "train", train=True)
    val_ds = DermDataset(Path(data_dir) / "val", train=False)

    train_loader = DataLoader(train_ds, batch_size=4, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=4, shuffle=False, num_workers=0)

    model = LightningDetector(num_classes=num_classes)
    ckpt_cb = ModelCheckpoint(
        dirpath=out_dir, filename="detector_mobilenetv3_demo", save_top_k=1, monitor="val_loss"
    )
    trainer = pl.Trainer(max_epochs=max_epochs, callbacks=[ckpt_cb])
    trainer.fit(model, train_loader, val_loader)

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    torch.save(model.model.state_dict(), Path(out_dir) / cfg.weights_name)


if __name__ == "__main__":
    main()






