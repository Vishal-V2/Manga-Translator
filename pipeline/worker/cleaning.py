from PySide6.QtCore import (
    QObject, Signal, Slot
)
import numpy as np
from PIL import Image

from pipeline.core.utility import convert_image
from pipeline.core.cleaning import text_masking
from pipeline.core.cleaning.base import CleaningBase
from pipeline.core.box_data import TextCluster



class CleaningWorker(QObject):
    finished = Signal(Image.Image)

    def __init__(self, cleaning_config: dict, text_clusters_data: list[TextCluster], image_cv2: np.ndarray, image_pil: Image.Image):
        super().__init__()
        self.cleaning_config = cleaning_config
        self.text_clusters_data = text_clusters_data
        self.image_cv2 = image_cv2
        self.image_pil = image_pil
        self.cleaning_process = CleaningBase(self.cleaning_config)

        self.image_mask = None
        self.image_cleaned = None


    @Slot()
    def run(self):
        self._text_masking()
        self._text_cleaning()

        self.finished.emit(self.image_cleaned)
    

    def _text_masking(self):
        self.inpainter = self.cleaning_config.get("model")
        self.mask_canvas = convert_image.blank_canvas(self.image_cv2)
        mask_np = self.mask_canvas.copy()
        for text_cluster_data in self.text_clusters_data:
            if text_cluster_data.bounding_image is None:
                continue
            mask_np = text_masking.apply_text_mask(mask_np, text_cluster_data)

         
        # SimpleLama/ONNX expect 255 where we want to inpaint.
        # apply_text_mask currently draws text regions in black (0) on a white canvas (255),
        # so we need to invert here so that text becomes 255 and background 0.
        if not np.array_equal(mask_np, self.mask_canvas):
            mask_np = 255 - mask_np
        else:
            # If no text was drawn, use an all-black mask (no inpaint)
            mask_np = np.zeros_like(mask_np)
           
        
        self.image_mask = Image.fromarray(mask_np)
        self.image_mask.save("output/image_mask.png")

    def _text_cleaning(self):
        self.image_cleaned = self.cleaning_process.batch_cleaning(self.image_pil, self.image_mask)