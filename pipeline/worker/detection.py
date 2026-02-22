from PySide6.QtCore import (
    QObject, Signal, Slot
)
from ultralytics import YOLO
import numpy as np
import cv2
from pipeline.core.box_data import SpeechBubble, TextCluster
import constants

from pipeline.core.detection.speech_bubble import SpeechBubbleDetection
from pipeline.core.detection.text_cluster import TextClusterDetection



class DetectionWorker(QObject):
    finished = Signal(list)

    def __init__(self, detection_config: dict, speech_bubble_model: YOLO, text_cluster_model: YOLO, image_cv2: np.ndarray):
        super().__init__()
        self.detection_config = detection_config or {}

        sb_thresh = None
        tc_thresh = None
        try:
            sb_thresh = float(self.detection_config.get("speech_bubble", {}).get("confidence_threshold"))
        except Exception:
            pass
        try:
            tc_thresh = float(self.detection_config.get("text_cluster", {}).get("confidence_threshold"))
        except Exception:
            pass
        # Persist thresholds with sane fallbacks
        self.sb_threshold = sb_thresh if sb_thresh is not None else constants.SPEECH_BUBBLE_THRESHOLD
        self.tc_threshold = tc_thresh if tc_thresh is not None else constants.TEXT_CLUSTER_THRESHOLD

        self.speech_bubble_detection = SpeechBubbleDetection(speech_bubble_model, threshold=self.sb_threshold)
        self.text_cluster_detection = TextClusterDetection(text_cluster_model, threshold=self.tc_threshold)
        self.image_cv2 = image_cv2
        
        self.speech_bubbles_data = []


    @Slot()
    def run(self):
        self._speech_bubble_detection()
        print("[DETECTION] speech_bubbles:", len(self.speech_bubbles_data), [(sb.class_name, sb.confidence) for sb in self.speech_bubbles_data])
        self._text_cluster_detection()
        try:
            counts = [len(sb.text_clusters or []) for sb in self.speech_bubbles_data]
            print("[DETECTION] clusters_per_bubble:", counts)
        except Exception:
            pass
        self.visualize_detection(self.image_cv2, self.speech_bubbles_data)
        
        self.finished.emit(self.speech_bubbles_data)
    

    def _speech_bubble_detection(self):
        # Try with configured threshold; if none found, progressively lower until we find something or hit 0.25
        attempts = []
        attempts.append(self.sb_threshold)
        for t in (0.50, 0.40, 0.35, 0.30, 0.25):
            if t not in attempts and t < self.sb_threshold:
                attempts.append(t)
        for t in attempts:
            self.speech_bubble_detection.threshold = t
            result = self.speech_bubble_detection.detect(self.image_cv2)
            if result:
                self.speech_bubbles_data = result
                break
        else:
            self.speech_bubbles_data = []
    

    def _text_cluster_detection(self):
        if not self.speech_bubbles_data:
            return
        # First pass in batch
        bubbles = self.text_cluster_detection.detect(self.speech_bubbles_data)
        # Per-bubble recovery: if a particular bubble has zero clusters, retry with lower thresholds for that bubble only
        for idx, sb in enumerate(bubbles):
            if not (sb.text_clusters and len(sb.text_clusters) > 0):
                for t in (self.tc_threshold, 0.45, 0.35, 0.30, 0.25):
                    self.text_cluster_detection.threshold = t
                    clusters = self.text_cluster_detection.detect(sb)  # returns list[TextCluster]
                    if clusters:
                        sb.text_clusters = clusters
                        break
        self.speech_bubbles_data = bubbles


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