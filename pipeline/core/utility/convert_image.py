import cv2
import numpy as np
from PIL import Image



def to_cv2(image_path: str) -> np.ndarray:
    return cv2.imread(image_path)


def to_pil(image_path: str) -> Image.Image:
    return Image.open(image_path).convert("RGB")


def cv2_to_pil(image_cv2: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))


def blank_canvas(image_cv2: np.ndarray) -> np.ndarray:
    return np.ones_like(image_cv2, dtype=np.uint8) * 255