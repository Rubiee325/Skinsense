from io import BytesIO
from typing import Tuple

from PIL import Image
import torchvision.transforms as T
import torch


IMG_SIZE: int = 224


def get_base_transform() -> T.Compose:
    return T.Compose(
        [
            T.Resize((IMG_SIZE, IMG_SIZE)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def get_augmentation_transform() -> T.Compose:
    # Hook for training data augmentation
    return T.Compose(
        [
            T.Resize((IMG_SIZE, IMG_SIZE)),
            T.RandomHorizontalFlip(),
            T.ColorJitter(brightness=0.1, contrast=0.1),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )


def load_image_from_bytes(data: bytes) -> Image.Image:
    return Image.open(BytesIO(data)).convert("RGB")


def preprocess_image_bytes(data: bytes) -> torch.Tensor:
    img = load_image_from_bytes(data)
    transform = get_base_transform()
    return transform(img).unsqueeze(0)






