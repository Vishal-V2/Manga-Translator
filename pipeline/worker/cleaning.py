from PySide6.QtCore import (
    QObject, Signal, Slot
)
import numpy as np
from PIL import Image

from pipeline.core.utility import convert_image
from pipeline.core.cleaning import text_masking
from pipeline.core.cleaning.migan_inpainter import MiganInpainter
from pipeline.core.cleaning.lama_inpainter import LamaInpainter
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
        self.image_mask = text_masking.batch_apply_text_mask(self.inpainter, self.mask_canvas, self.text_clusters_data)
    

    def _text_cleaning(self):
        self.image_cleaned = self.cleaning_process.batch_cleaning(self.image_pil, self.image_mask)