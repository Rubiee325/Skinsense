from dataclasses import dataclass
from io import BytesIO
from typing import Any, Dict, List, Optional

import base64
import torch
import torch.nn as nn
from PIL import Image, ImageEnhance
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

from .preprocessing import preprocess_image_bytes, load_image_from_bytes, IMG_SIZE


TIMEPOINTS = ["30d", "6mo", "1yr"]


@dataclass
class PredictorConfig:
    feature_dim: int = 576  # mobilenet_v3_small final feature dim
    hidden_dim: int = 256
    num_layers: int = 1


class TemporalHead(nn.Module):
    def __init__(self, cfg: PredictorConfig):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=cfg.feature_dim,
            hidden_size=cfg.hidden_dim,
            num_layers=cfg.num_layers,
            batch_first=True,
        )
        self.out_risk = nn.Linear(cfg.hidden_dim, len(TIMEPOINTS) * 3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h, _ = self.lstm(x)
        last = h[:, -1, :]
        return self.out_risk(last)


class SkinMorphPredictor:
    def __init__(self, cfg: Optional[PredictorConfig] = None) -> None:
        self.cfg = cfg or PredictorConfig()
        self.device = torch.device("cpu")
        self.backbone = self._build_feature_extractor().to(self.device)
        self.head = TemporalHead(self.cfg).to(self.device)
        self.backbone.eval()
        self.head.eval()

    def _build_feature_extractor(self) -> nn.Module:
        weights = MobileNet_V3_Small_Weights.DEFAULT
        backbone = mobilenet_v3_small(weights=weights)
        backbone.classifier = nn.Identity()
        return backbone

    def _extract_feature(self, img_bytes: bytes) -> torch.Tensor:
        x = preprocess_image_bytes(img_bytes).to(self.device)
        with torch.no_grad():
            feat = self.backbone(x)
        return feat.squeeze(0)

    def _generate_future_visuals(self, last_image_bytes: bytes) -> Dict[str, str]:
        """
        Simple fallback visualizations: apply small synthetic changes over time.
        This is a placeholder for a U-Net style generator.
        Returns base64 PNGs keyed by timepoint.
        """
        base_img = load_image_from_bytes(last_image_bytes).resize((IMG_SIZE, IMG_SIZE))
        visuals: Dict[str, str] = {}
        factors = {"30d": 1.05, "6mo": 1.1, "1yr": 1.15}

        for tp, factor in factors.items():
            # Slight darkening/contrast to mimic pigmentation/wrinkle changes
            img_mod = ImageEnhance.Brightness(base_img).enhance(1.0)
            img_mod = ImageEnhance.Contrast(img_mod).enhance(factor)
            buffer = BytesIO()
            img_mod.save(buffer, format="PNG")
            visuals[tp] = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return visuals

    def predict_sequence_bytes(
        self,
        images: List[bytes],
        metadata_json: Optional[str] = None,
        timestamps: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not images:
            raise ValueError("At least one image is required")

        feats = [self._extract_feature(b) for b in images]
        seq = torch.stack(feats, dim=0).unsqueeze(0)  # (1, T, F)
        with torch.no_grad():
            out = self.head(seq)

        out = out.squeeze(0).cpu().numpy().tolist()
        # out is length len(TIMEPOINTS)*3; map to risk scores
        preds: Dict[str, Dict[str, float]] = {}
        for i, tp in enumerate(TIMEPOINTS):
            base = i * 3
            preds[tp] = {
                "pigmentation_risk": float(out[base]),
                "acne_risk": float(out[base + 1]),
                "wrinkle_risk": float(out[base + 2]),
            }

        # Generate simple future visuals as a placeholder for a true generator.
        visuals = self._generate_future_visuals(images[-1])

        return {
            "timepoints": TIMEPOINTS,
            "risks": preds,
            "future_visuals_png_b64": visuals,
            "notes": "Demo predictor head with synthetic visuals; not medically meaningful.",
        }


