import base64
from io import BytesIO
from typing import Optional

import torch
import torch.nn as nn
from PIL import Image
import numpy as np

from .preprocessing import load_image_from_bytes, IMG_SIZE


class GradCAMGenerator:
    def __init__(self, model: nn.Module, target_layer_name: str) -> None:
        self.model = model
        self.model.eval()
        self.target_layer_name = target_layer_name
        self.gradients: Optional[torch.Tensor] = None
        self.activations: Optional[torch.Tensor] = None
        self._register_hooks()

    def _register_hooks(self) -> None:
        layer = dict(self.model.named_modules()).get(self.target_layer_name)
        if layer is None:
            return

        def forward_hook(_, __, output):
            self.activations = output

        def backward_hook(_, grad_in, grad_out):
            self.gradients = grad_out[0]

        layer.register_forward_hook(forward_hook)
        layer.register_backward_hook(backward_hook)

    def _compute_cam(self, class_idx: int) -> np.ndarray:
        if self.activations is None or self.gradients is None:
            raise RuntimeError("No activations/gradients captured for Grad-CAM")

        grads = self.gradients
        activations = self.activations
        weights = grads.mean(dim=(2, 3), keepdim=True)
        cam = (weights * activations).sum(dim=1, keepdim=True)
        cam = torch.relu(cam)
        cam = cam.squeeze().detach().cpu().numpy()
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        cam = np.uint8(255 * cam)
        cam = np.array(Image.fromarray(cam).resize((IMG_SIZE, IMG_SIZE)))
        return cam

    def generate_overlay_b64(self, image_bytes: bytes) -> str:
        # Minimal single-class Grad-CAM: assume max-probability class
        img = load_image_from_bytes(image_bytes)
        img_resized = img.resize((IMG_SIZE, IMG_SIZE))
        x = torch.from_numpy(np.array(img_resized)).float() / 255.0
        x = x.permute(2, 0, 1).unsqueeze(0)

        x.requires_grad = True
        logits = self.model(x)
        score, class_idx = torch.max(logits, dim=1)
        self.model.zero_grad()
        score.backward()

        cam = self._compute_cam(int(class_idx.item()))
        heatmap = Image.fromarray(cam).resize(img_resized.size)
        heatmap = heatmap.convert("RGBA")

        overlay = img_resized.convert("RGBA")
        alpha = 0.4
        blended = Image.blend(overlay, heatmap, alpha=alpha)

        buffer = BytesIO()
        blended.save(buffer, format="PNG")
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return b64






