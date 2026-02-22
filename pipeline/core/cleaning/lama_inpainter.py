import os
os.environ.setdefault("PYTORCH_ALLOC_CONF", "expandable_segments:True")

from PIL import Image
import torch
from simple_lama_inpainting import SimpleLama
from pipeline.core.cleaning.migan_inpainter import MiganInpainter


class LamaInpainter:
    def __init__(self):
        self.model = SimpleLama()
    

    def inpaint(self, image_pil: Image.Image, image_mask: Image.Image) -> Image.Image:
        # SimpleLama expects an RGB image and a single-channel mask
        rgb_image = image_pil.convert("RGB")
        grayscale_mask = image_mask.convert("L")

        try:
            result = self.model(rgb_image, grayscale_mask)
        except RuntimeError as e:
            msg = str(e)
            if ("CUDA out of memory" in msg) or ("out of memory" in msg and "CUDA" in msg):
                try:
                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                except Exception:
                    pass
                # Fallback to MiGAN (CPU/ONNX) to proceed without crashing
                migan = MiganInpainter()
                result = migan.inpaint(rgb_image, grayscale_mask)
            else:
                raise

        result.save("output/image_cleaned.png")
        return result
