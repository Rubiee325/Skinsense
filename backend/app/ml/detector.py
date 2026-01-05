from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch
import torch.nn as nn
from torchvision.models import mobilenet_v3_small, MobileNet_V3_Small_Weights

from .preprocessing import preprocess_image_bytes
from .explainability import GradCAMGenerator


CLASS_NAMES: List[str] = [
    "benign_nevus",
    "melanoma_suspect",
    "seborrheic_keratosis",
    "acne",
    "eczema",
    "psoriasis",
    "rosacea",
]


@dataclass
class DetectorConfig:
    num_classes: int = len(CLASS_NAMES)
    weights_dir: Path = Path("/models/demo_weights")
    weights_name: str = "detector_mobilenetv3_demo.pt"


class DetectorModel:
    def __init__(self, config: Optional[DetectorConfig] = None) -> None:
        self.config = config or DetectorConfig()
        self.device = torch.device("cpu")
        self.model = self._build_model().to(self.device)
        self.gradcam = GradCAMGenerator(self.model, target_layer_name="features.12")

    def _build_model(self) -> nn.Module:
        weights = MobileNet_V3_Small_Weights.DEFAULT
        backbone = mobilenet_v3_small(weights=weights)
        in_features = backbone.classifier[3].in_features
        backbone.classifier[3] = nn.Linear(in_features, self.config.num_classes)

        weights_path = self.config.weights_dir / self.config.weights_name
        if weights_path.exists():
            state = torch.load(weights_path, map_location="cpu")
            backbone.load_state_dict(state)

        backbone.eval()
        return backbone

    def predict_image_bytes(
        self, data: bytes, metadata: Optional[str] = None
    ) -> Dict[str, Any]:
        x = preprocess_image_bytes(data).to(self.device)
        with torch.no_grad():
            logits = self.model(x)
            probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

        predictions = [
            {"label": label, "probability": float(prob)}
            for label, prob in zip(CLASS_NAMES, probs)
        ]
        predictions.sort(key=lambda p: p["probability"], reverse=True)
        top = predictions[0]

        heatmap_png_b64 = self.gradcam.generate_overlay_b64(data)

        return {
            "top_class": top,
            "all_classes": predictions,
            "gradcam_overlay_png_b64": heatmap_png_b64,
            "metadata_echo": metadata,
        }






