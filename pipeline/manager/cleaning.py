from PySide6.QtCore import (
    Signal, QObject
)
from PIL import Image

from pipeline.worker.worker_utility import run_in_thread
from pipeline.worker.cleaning import CleaningWorker
from pipeline.core.box_data import TranslationPage



class CleaningManager(QObject):
    data = Signal(Image.Image)

    def __init__(self, cleaning_config: dict):
        super().__init__()
        self.cleaning_config = cleaning_config


    def start(self, page_data: TranslationPage):
        image_cv2 = page_data.image_cv2
        image_pil = page_data.image_pil
        text_clusters_data = [cluster for bubble in page_data.speech_bubbles for cluster in bubble.text_clusters]

        self.worker, self.run_in_thread = run_in_thread(
            CleaningWorker,
            self.cleaning_config,
            text_clusters_data,
            image_cv2,
            image_pil,
            on_finished=self._complete
        )
    

    def _complete(self, cleaned_image: Image.Image):
        self.data.emit(cleaned_image)