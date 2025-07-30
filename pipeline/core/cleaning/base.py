from pipeline.core.cleaning.lama_inpainter import LamaInpainter
from pipeline.core.cleaning.migan_inpainter import MiganInpainter
import numpy as np
from PIL import Image



class CleaningBase:
    def __init__(self, cleaning_config: dict):
        self.selected_inpainter = cleaning_config.get("model")

        if self.selected_inpainter == "lama":
            self.inpainter = LamaInpainter()
        elif self.selected_inpainter == "migan":
            self.inpainter = MiganInpainter()
    

    def batch_cleaning(self, image_pil: Image.Image, image_mask: Image.Image) -> Image.Image:
        return self.inpainter.inpaint(image_pil, image_mask)



