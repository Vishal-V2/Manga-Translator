from PySide6.QtCore import (
    Signal, QObject
)
from ultralytics import YOLO

from pipeline.worker.worker_utility import run_in_thread
from pipeline.worker.detection import DetectionWorker
from pipeline.core.box_data import SpeechBubble, TextCluster

import numpy as np


class DetectionManager(QObject):
    data = Signal(list)

    def __init__(self, api_config: dict, speech_bubble_model: YOLO, text_cluster_model: YOLO):
        super().__init__()
        self.speech_bubble_model = speech_bubble_model
        self.text_cluster_model = text_cluster_model


    def start(self, image_cv2: np.ndarray):
        self.worker, self.run_in_thread = run_in_thread(
            DetectionWorker,
            self.speech_bubble_model,
            self.text_cluster_model,
            image_cv2,
            on_finished=self._complete
        )
    

    def _complete(self, speech_bubbles_data: list[SpeechBubble]):
        self.data.emit(speech_bubbles_data)