from PySide6.QtCore import (
    QObject, Signal, Slot
)
from ultralytics import YOLO
import numpy as np
import cv2
from pipeline.core.box_data import SpeechBubble, TextCluster

from pipeline.core.detection.speech_bubble import SpeechBubbleDetection
from pipeline.core.detection.text_cluster import TextClusterDetection



class DetectionWorker(QObject):
    finished = Signal(list)

    def __init__(self, speech_bubble_model: YOLO, text_cluster_model: YOLO, image_cv2: np.ndarray):
        super().__init__()
        self.speech_bubble_detection = SpeechBubbleDetection(speech_bubble_model)
        self.text_cluster_detection = TextClusterDetection(text_cluster_model)
        self.image_cv2 = image_cv2
        
        self.speech_bubbles_data = []


    @Slot()
    def run(self):
        self._speech_bubble_detection()
        self._text_cluster_detection()
        self.visualize_detection(self.image_cv2, self.speech_bubbles_data)
        
        self.finished.emit(self.speech_bubbles_data)
    

    def _speech_bubble_detection(self):
        self.speech_bubbles_data = self.speech_bubble_detection.detect(self.image_cv2)
    

    def _text_cluster_detection(self):
        if not self.speech_bubbles_data:
            return
        
        self.speech_bubbles_data = self.text_cluster_detection.detect(self.speech_bubbles_data)


    def visualize_detection(
            self, 
            image_cv2: np.ndarray,
            speech_bubbles_data: list[SpeechBubble]
    ):
        image_copy = image_cv2.copy()

        for speech_bubble_data in speech_bubbles_data:
            SBx_min, SBy_min, SBx_max, SBy_max = speech_bubble_data.position
            cv2.rectangle(image_copy, (SBx_min, SBy_min), (SBx_max, SBy_max), (255, 0, 0), 4)
        
            for text_cluster_data in speech_bubble_data.text_clusters:
                TCx_min, TCy_min, TCx_max, TCy_max = text_cluster_data.position
                cv2.rectangle(image_copy, (TCx_min, TCy_min), (TCx_max, TCy_max), (0, 255, 0), 4)
        
        cv2.imwrite("output/visualized_detection.png", image_copy)